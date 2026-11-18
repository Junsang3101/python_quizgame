# python_quizgame

## 0. 프로젝트 개요

본 프로젝트는 '코디세이 입학 연수 미션 1-2:파이썬 배우기'로  
파이썬으로 퀴즈게임을 만드는 것입니다.

**목적**: 프로그래밍 배우기의 일환으로 Python 과 Git 을 활용하여 프로그램을 만들기 기록하고 내가 만든 프로그램이 왜 이렇게 동작하는지 설명할 수 있게 되는 것입니다.

**기능 목록**:  

- 메인 메뉴
  - 퀴즈 풀기
    - 퀴즈 섞어짐
    - 퀴즈 수 선택
  - 퀴즈 목록 보기
    - 퀴즈 추가
    - 퀴즈 삭제
  - 점수 기록 보기
  - 점수 기록 초기화

## 1. 파일 구조

본래 `/python_quizgame/src/data` 구조로 바꾸었으나, 미션에서 외부 파일에 상태를 저장하라 한 부분에서  
미션 저장소가 퀴즈게임 모듈로써 사용할 수 있게 하라고 이해해 단순하게 해봤습니다.

```powershell
└─python_quizgame
    │  .gitignore
    │  cli.py
    │  default_quizzes.json
    │  json_store.py
    │  quizgame.py
    │  README.md
    │  state.json
    │  __init__.py
    └─ __main__.py
```

## 2. 프로그램 구조

`cli`: 사용자 인터페이스 모듈  
- 메인 메뉴, 퀴즈 목록 및 추가/삭제, 점수 기록, 퀴즈 시작 (무작위 순서 및 퀴즈 수 선택)

`quizgame`: 퀴즈게임 로직 모듈  
- `Score`, `Quiz`: 점수와 퀴즈 `dataclass`로 상태 정보를 저장한다  
- `QuizGameManager`로 데이터 저장/삭제를 하고 시작하면 퀴즈게임을 생성해 리턴한다  
- `QuizGame` 에 현재 게임 상태 정보를 저장하고 진행한다.

`json_store`: json 저장 모듈  
- `load_json`, `save_json`, `s_load_json`: 전자 둘은 `with open` 및 `json` 를 결합한 래퍼 함수고, 후자는 파일이 깨졌을 경우에 백업한다

[데이터 구조](evidence/데이터%20구조.md)

소스 코드
- [ndjson_store](json_store.py)
- [quizgame](quizgame.py)
- [cli](cli.py)

## 3. 실행 방법

메인 프로젝트 경로 `python_quizgame/`의 이전 경로에서 `python -m python_quizgame`를 해주세요.

## 4. 수행 목록

### 4-1. 필수 

- [실행 화면 및 `git log --oneline --graph` 출력물](evidence/실행%20화면%20및%20gitlog%20출력물.md)

- [x] [Git 저장소 설정](/evidence/Git%20저장소%20설정.md)
- [x] [메뉴 기능](evidence/메뉴%20설명.md)
- [x] [공통 입력 및 예외 처리](evidence/공통%20입력%20및%20예외%20처리.md)
- [x] [퀴즈 클래스](/evidence/퀴즈%20클래스.md)
- [x] [기본 퀴즈 데이터](evidence/기본%20퀴즈%20데이터.md)
- [x] [퀴즈 풀기 (브랜치 merge 실습)](evidence/브랜치%20실습.md)
- [x] [퀴즈 저장](evidence/퀴즈%20저장.md)
- [x] [퀴즈 목록](evidence/퀴즈%20목록.md)
- [x] [점수 확인](evidence/점수%20확인.md)
- [x] [QuizGame 클래스](evidence/QuizGame%20클래스.md)
- [x] [파일 저장/불러오기](evidence/파일%20저장%20및%20불러오기.md)
- [x] [Git 저장소 복제 실습](evidence/Git%20복제%20실습.md)

### 5-1. 선택

- [x] 랜덤 출제
`QuizGame` 메소드에 섞기를 구현하였고, `cli`에서 실행하기 전에 섞도록 하였습니다.
``` python
    def shuffle(self):
        '''퀴즈 섞기'''
        random.shuffle(self.quizzes)
```
- [x] 문제 수 선택
`cli`에서 시작하면 퀴즈를 고르고, 예외처리 해주었습니다.
``` python
    try:
        request = int(input("문제 수(0 = 전부):"))
        quizgame = manager.start(request)
    except EmptyQuizzesError:
        print("퀴즈가 하나도 없습니다.")
        return main_menu(manager)
    except ValueError:
        print("다시 입력해주세요.")
        return start_menu(manager)
    except (KeyboardInterrupt, EOFError):
        manager.save()
        print("게임을 종료합니다.\n")
```
- [x] 힌트 기능
`Quiz`에 `hint` 필드를 만들어 `.tostring()`할 때 인자로 받을지 안 받을지 선택하게 했습니다.
``` python
    def to_string(self, index, get_hint: bool, get_answer: bool):
        '''퀴즈 정보를 문자열로 리턴'''
        result = [f"{index}) {self.question}"]
        if get_hint is True:
            result.append(f"(힌트: {self.hint})")
        for j, choice in enumerate(self.choices, start=1):
            result.append(f"    {j}. {choice}")
        if get_answer is True:
            result.append(f"    정답: {self.answer}")
        return "\n".join(result)
```
- [x] 퀴즈 삭제 기능
`quizgame` 모듈의 `QuizGameManager` 에서 퀴즈 데이터를 관리하기 때문에 `.remove()` 메소드를 구현해
`cli`모듈에서 퀴즈 목록 화면의 상호작용에 퀴즈 삭제를 항목을 넣었습니다.
``` python
    def quiz_remove(self, index: int):
        '''퀴즈 제거'''
        try:
            self.quizzes.pop(index)
        except IndexError:
            raise IndexError
```  

``` python
def remove_menu(manager: QuizGameManager):
    '''퀴즈 삭제'''
    try:
        choice = int(input("삭제 (0 = 취소): ")) - 1
        if choice == -1:
            return list_menu(manager)
        manager.quiz_remove(choice)
    except (TypeError, IndexError, ValueError):
        print("다시 입력해주세요 (0 = 취소): ")
        return remove_menu(manager)
    except (KeyboardInterrupt, EOFError):
        manager.save()
        print("게임을 종료합니다.\n")
    
    return list_menu(manager)
```
- [x] 점수 기록 히스토리
퀴즈에 `to_string`메소드를 퀴즈처럼 구현하고 `quizgame` 모듈에 `QuizGameManager`의 점수 데이터를 `cli` 모듈에서 읽도록 `score_list`를 만들었습니다.
``` python
def score_list(manager: QuizGameManager):
    '''기록 보기'''
    print("\n=== 기록 ===")
    for score in manager.scores:
        print(f"{score.to_string}\n")
    if manager.highest != None:
        print(f"\n=== 최고 점수 ===\n{manager.highest.to_string}")
    return main_menu(manager)
```

# 6. 느낀점

**어떻게 문제를 해결할 것인가**  
- 처음에는 전 미션 도커를 활용해볼까? 하고 도커로도 만들어 보고  
미션 세부 요구사항을 읽지 않고 설계 없이 퀴즈 게임을 만들기 시작해 자주 뜯어 고치고  
ndjson 은 셀프 힐링이 간단하다 하여 ndjson으로 모듈 다 만들었다가 json 으로 다시 고치고,  
중간의 메소드/함수/클래스 이름 등 마음에 안 드는 부분이 생길 때마다 자주 바꿔 스스로 할 일을 만드는 등 굉장히 많은 시간이 들었습니다. 

- 현재는 저장소를 바로 파이썬 모듈로 사용하고싶어 도커를 떼버렸는데, 도커가 있으면 환경 설정이 편해 나쁘지 않았을 것 같습니다.

- 결과적으로 이번 미션을 하면서 미션이 있으면 먼저 미션의 요구사항이 뭔지 분석을 하고 어떤식으로 구현할지 
ai 를 통해 디자인 패턴 등 조언을 구해가며 스텁을 활용해서 탑다운 방식으로 만드는 걸 지향할 것 같습니다.  

- 이번 미션은 대부분 의도하지 않고 우연히 디자인 패턴을 사용해 내 코드를 제대로 이해하지 않고있다는 느낌을 받았습니다.

**커밋을 언제 하는가**  
- 작업 중간 중간 언제 커밋을 해야할지 헤매 보통 vscode 를 끄기 전이나 커밋을 하였는데, 요구사항에 있었던대로 클래스 함수 등 실행 가능한 단위가 완성이 되면 하면 되겠다고 느끼기도 꼇습니다.