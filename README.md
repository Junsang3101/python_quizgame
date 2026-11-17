# python_quizgame

## 0. 프로젝트 개요

본 프로젝트는 '코디세이 입학 연수 미션 1-2:파이썬 배우기'로  
파이썬으로 퀴즈게임을 만드는 것입니다.

**목적**: 프로그래밍 배우기의 일환으로 Python 과 Git 을 활용하여 프로그램을 만들기 기록하고 내가 만든 프로그램이 왜 이렇게 동작하는지 설명할 수 있게 되는 것입니다.

## 1. 파일 구조

```text
python_quizgame
│   .gitignore              # git 무시할 파일/디렉토리
│   README.md
│
└── src
      cli.py                # CLI 메뉴와 사용자 입력·출력
      quizgame.py           # 게임 로직
      __init__.py           # src 패키지 표시
      __main__.py           # CLI 실행 진입점
      default_quizzes.json  # 기본 퀴즈
      state_json            # 상태 저장
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

소스 코드
- [ndjson_store](json_store.py)
- [quizgame](quizgame.py)
- [cli](cli.py)

## 3. 실행 방법

메인 프로젝트 경로 `python_quizgame/` 에서 `python -m python_quizgame`를 해주세요.

## 4. 수행 목록

### 4-1. 필수 

- [x] [Git 저장소 설정](/evidence/Git%20저장소%20설정.md)
- [x] [메뉴 기능](evidence/메뉴%20설명.md)
- [x] [공통 입력 및 예외 처리](evidence/공통%20입력%20및%20예외%20처리.md)
- [x] [퀴즈 클래스](/evidence/퀴즈%20클래스.md)
- [x] [기본 퀴즈 데이터](evidence/기본%20퀴즈%20데이터.md)
- [ ] [퀴즈 풀기 (브랜치 merge 실습)]()
- [x] 퀴즈 저장
- [x] 퀴즈 목록
- [x] 점수 확인
- [x] QuizGame 클래스
- [x] 파일 저장/불러오기
- [ ] [Git 저장소 복제 실습]()

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