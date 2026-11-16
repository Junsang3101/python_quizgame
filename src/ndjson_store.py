import json
from pathlib import Path
from typing import Type, Any

JsonObject = dict[str, object]

'''
python-only 브랜치 84b1515 커밋 까지 데이터를 ndjson 형식으로 저장했기 때문에 ndjson 전용 함수가 많음
미션 요구사항에 맞춰 state.json 에 맞게 함수 새로 작성함
'''

def find_in_root(directory_path: str | Path, filename: str) -> Path | None:
    '''경로에 해당 파일에 접근하여 주소 리턴, 없으면 None'''
    dir_path = Path(directory_path)
    file_path = dir_path / filename
    
    if file_path.is_file():
        return file_path
    return None

def go_or_create_in_root(directory_path: str | Path, filename: str, default_data = None) -> Path:
    '''경로에 해당 파일에 접근해 주소 리턴, 생성하여 리턴'''
    if default_data is None:
        default_data = ""
    dir_path = Path(directory_path)
    file_path = find_in_root(dir_path, filename)
    if file_path is None:
        file_path = dir_path / filename
    if not file_path.is_file():
        write_items(file_path, default_data)
    return file_path

#================= NDJSON 함수 ==================

def ndload_items(path: Path, target_type: Type[Any]) -> list[JsonObject]:
    '''파일 경로에 있는 파일을 로드하여 list로 리턴, target_type을 받아 데이터가 훼손됐는지를 검사'''
    if not path.exists() or path.stat().st_size == 0:
        return []
    items = []

    # 순수 데이터로, json 형식으로 2번 한 줄씩 검사하고, 최종 결과물 list로 리턴
    with open(path, "r", encoding="utf-8") as source:
        for line_num, line in enumerate(source, 1): # 순수 데이터 검사
            line = line.strip()
            if not line:
                continue
            elif line is None:
                continue

            try:
                data = json.loads(line)

                if  data == None:   # json 형식으로 검사
                    print(
                        f"경고: {path}의 {line_num}번째 줄 데이터 타입이"
                        f" {type(data).__name__}, 비어있습니다."
                    )
                    continue
                elif not isinstance(data, target_type):
                    print(
                        f"경고: {path}의 {line_num}번째 줄 데이터 타입이"
                        f" {type(data).__name__}입니다. ({target_type.__name__}이"
                        " 필요하여 무시합니다)"
                    )
                    continue

            except json.JSONDecodeError:
                print("{path} 문법 오류.")
                return None 
            except FileNotFoundError:
                print("{path} 파일이 없습니다.")
                return None
            except PermissionError:
                print("{path} 권한이 없습니다.")
                return None
            
def ndwrite_items(path: Path, items: list[JsonObject]) -> None:
    '''해당 파일 주소에 새 datas로 덮어씌움, None 입력시 null 만 남음'''
    with open(path, "w", encoding="utf-8") as target:   # 데이터 읽기
        for item in items:
            data = item.__dict__ if hasattr(item, "__dict__") else item # 데이터가 딕셔너리가 아니면 딕셔너리로 바꿈
            target.write(json.dumps(data, ensure_ascii=False) + "\n")

def ndwrite_item(path: Path, item: JsonObject) -> None:
    '''해당 파일 주소에 새 data로 덮어씌움, None 입력시 null 만 남음'''
    # write_items 는 데이터를 list로 받아서 한줄씩 쓰는데, 단일 파일은 오류가 나 단일 데이터를 list로 감싸서 전달
    ndwrite_items(path, [item])

def ndadd_items(path: Path, items: list[JsonObject]) -> None:
    '''해당 경로에 기존 데이터 뒤에 새 items 추가'''
    with open(path, "a", encoding="utf-8") as target:
        for item in items:
            target.write(json.dumps(item, ensure_ascii=False) + "\n")

def ndadd_item(path: Path, item: JsonObject) -> None:
    '''해당 경로에 기존 데이터 뒤에 새item 추가'''
    # add_items 는 데이터를 list로 받아서 한줄씩 쓰는데, 단일 파일은 오류가 나 단일 데이터를 list로 감싸서 전달
    ndadd_items(path, [item])

def ndremove_item(path: Path, index: int, target_type: Type[Any]) -> None:
    '''해당 경로에 특정 줄 제거, 해당 파일의 타입이 필요함.'''
    items = ndload_items(path, target_type)
    items.pop(index)
    ndwrite_items(path, items)

#================= JSON 함수 ==================

def load_item(path: Path | str) -> Any | None:
    """파일 경로에서 JSON을 안전하게 읽어 반환합니다.
    파일이 없거나, 형식이 깨졌을 경우 예외를 잡고 None을 리턴합니다.
    """
    try:
        if not path.exists() or path.stat().st_size == 0:
            print("{path} 파일이 비어있습니다.")
            return None
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("{path} 문법 오류.")
        return None 
    except FileNotFoundError:
        print("{path} 파일이 없습니다.")
        return None
    except PermissionError:
        print("{path} 권한이 없습니다.")
        return None