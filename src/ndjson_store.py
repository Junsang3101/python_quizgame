import json
from pathlib import Path
from typing import Type, Any

JsonObject = dict[str, object]

def _as_list(data: JsonObject | list[JsonObject]) -> list[JsonObject]:
    return data if isinstance(data, list) else [data]

def find_in_root(directory_path: str | Path, filename: str) -> Path | None:
    dir_path = Path(directory_path)
    file_path = dir_path / filename
    
    if file_path.is_file():
        return file_path
    return None

def go_or_create_in_root(directory_path: str | Path, filename: str, default_data = None) -> Path:
    if default_data is None:
        default_data = []
    dir_path = Path(directory_path)
    file_path = find_in_root(dir_path, filename)
    if file_path is None:
        file_path = dir_path / filename
    if not file_path.is_file():
        write_items(file_path, default_data)
    return file_path

def load_items(path: Path, target_type: Type[Any]) -> list[JsonObject]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    items = []
    with open(path, "r", encoding="utf-8") as source:
        for line_num, line in enumerate(source, 1):
            line = line.strip()
            if not line: # 빈 줄은 무시
                continue

            try:
                # 한 줄 꺼냄 
                data = json.loads(line)

                # 타겟이 아니면 스킵
                if not isinstance(data, target_type) or data == None:
                    print(
                        f"경고: {path}의 {line_num}번째 줄 데이터 타입이"
                        f" {type(data).__name__}입니다. ({target_type.__name__}이"
                        " 필요하여 무시합니다)"
                    )
                    continue

                items.append(data)
            except json.JSONDecodeError:
                # 특정 줄이 깨졌다면 그 줄만 조용히 버림 (셀프 힐링)
                print(f"경고: {path}의 {line_num}번째 줄 데이터가 손상되어 무시합니다.")
    return items


def write_items(path: Path, data: JsonObject | list[JsonObject]) -> None:
    items = _as_list(data)
    with open(path, "w", encoding="utf-8") as target:
        #json.dump(items, target, ensure_ascii=False, indent=None, default=str)
        for item in items:
            # 객체면 __dict__로, 딕셔너리뷰면 그대로 JSON 문자열로 변환 후 줄바꿈 추가
            data = item.__dict__ if hasattr(item, "__dict__") else item
            target.write(json.dumps(data, ensure_ascii=False) + "\n")

def add_items(path: Path, data: JsonObject | list[JsonObject]) -> None:
    new_items = _as_list(data)
    existing_items = load_items(path, dict) if path.exists() else []
    existing_items.extend(new_items)
    write_items(path, existing_items)

def remove_item(path: Path, index: int) -> None:
    items = load_items(path)
    items.pop(index)
    write_items(path, items)
