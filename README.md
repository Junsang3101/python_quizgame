# python_quizgame

## 0. 프로젝트 개요

본 프로젝트는 '코디세이 입학 연수 미션 1-2:파이썬 배우기'로  
파이썬으로 퀴즈게임을 만드는 것입니다.

**목적**: 프로그래밍 배우기의 일환으로 Python 과 Git 을 활용하여 프로그램을 만들기 기록하고 내가 만든 프로그램이 왜 이렇게 동작하는지 설명할 수 있게 되는 것입니다.

## 1. 파일 구조

```text
python_quizgame
│   .gitignore          # git 무시할 파일/디렉토리
│   README.md
│
└── src
    │   cli.py          # CLI 메뉴와 사용자 입력·출력
    │   quizgame.py     # 게임 로직
    │   quizgame.py     # 퀴즈 모델, 로더, 게임 로직 및 데이터 경로 상수
    │   __init__.py     # src 패키지 표시
    │   __main__.py     # CLI 실행 진입점
    │
    └── data
            default_quizzes.json    # 기본 퀴즈 데이터
            quizzes.json            # 사용자 정의 퀴즈 데이터
            scores.json             # 점수 기록
            highest.json            # 점수 기록
```

## 2. 프로그램 구조

`cli <- quizgame  <- ndjson_store `     
화살표 방향대로 모듈을 사용하고 있습니다.  
`ndjson_store` 에서 데이터 읽기 쓰기만, `quizgame`에선 퀴즈게임 로직만, `cli`에는 사용자 ui만 구현하였고,
`/data` 경로에 `default_quizzes`, `quizzes`, `scores`, `highest`란 이름으로  
기본 퀴즈, 퀴즈, 점수 기록, 최고 점수를 기록하였습니다.

- [세부 설명](evidence/모듈%20세부%20설명.md)

소스 코드
- [ndjson_store](src/ndjson_store.py)
- [quizgame](src/quizgame.py)
- [cli](src/cli.py)

## 3. 실행 방법

메인 프로젝트 경로 `python_quizgame/` 에서 `python -m src`를 해주세요.

## 4. 수행 목록

### 4-1. 필수 

- [x] Git 저장소 설정
- [x] 메뉴 기능
- [x] 공통 입력 및 예외 처리
- [x] 퀴즈 클래스
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
- [ ] 문제 수 선택
- [x] 힌트 기능
- [x] 퀴즈 삭제 기능
- [x] 점수 기록 히스토리