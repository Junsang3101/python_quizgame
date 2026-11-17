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

- [x] Git 저장소 설정 [Git 저장소 설정](/evidence/Git%20저장소%20설정.md)
- [x] 메뉴 기능 [메뉴 설명](evidence/메뉴%20설명.md)
- [x] 공통 입력 및 예외 처리 [공통 입력 및 예외 처리 설명](evidence/공통%20입력%20및%20예외%20처리.md)
- [x] 퀴즈 클래스 [퀴즈 클래스 설명](/evidence/퀴즈%20클래스.md)
```
- [x] 기본 퀴즈 데이터
- [ ] 퀴즈 풀기 (브랜치 활용)
- [x] 퀴즈 저장
- [x] 퀴즈 목록
- [x] 점수 확인
- [x] QuizGame 클래스
- [x] 파일 저장/불러오기 ('src/data/'에 저장함)
- [ ] Git 저장소 복제 실습: []()

### 5-1. 선택

- [x] 랜덤 출제
- [x] 문제 수 선택
- [x] 힌트 기능
- [x] 퀴즈 삭제 기능
- [x] 점수 기록 히스토리