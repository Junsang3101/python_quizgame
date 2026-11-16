from __future__ import annotations

from datetime import datetime   # 시간
from zoneinfo import ZoneInfo   # 장소
from dataclasses import dataclass, asdict   # dataclass 및 객체 전환(asdict)
from pathlib import Path        # 경로
import random                   # 무작위
# 만든 ndjson i/o
from .ndjson_store import go_or_create_in_root, load_items, add_item, remove_item, write_item

'''
해보면 좋은 것 1)
지금은 QuizGameManager클래스 내부 필드에서 퀴즈, 점수를 관리해
설계 결함으로 업데이트 메소드로 최신화 해줘야함 
저장경로나 퀴즈를 클래스에서 관리 안 하고 파일을 읽고 /temp/ 경로에 파일을 만들어준 후 그 안에서 관리하다 저장시 /data/에 복사해줘야 했음
이러면 실행중 갑자기 꺼져도 해당 상태가 유지되고, ndjson형식으로 저장되기 때문에 파손된 데이터도 쉽게 무시하고 읽어들일 수 있음
    -> 하지만 파일 i/o 작업이 많아지기 때문에 불필요하게 무거워짐 현재도 아무런 문제가 없음

해보면 좋은 것 2)
게임 시작시 QuizGame을 리턴해주는 게 아니라 _games: dict[str:QuizGame] 필드를 만들고 game_id를 생성해 
해당 QuizGame 인스턴스와 id를 연결하고, id를 리턴해준 후 그 id의 조작을 QuizGameManager에 요청
    -> 여러 인스턴스를 관리해야할 때 필요한 구조로 해보면 좋을 것 같음
'''

@dataclass
class Quiz: # 퀴즈
    question: str
    choices: list[str]
    answer: str
    hint: str

    @classmethod
    def from_dict(cls, quiz):
        '''딕셔너리를 퀴즈로 읽기'''
        try:
            return cls(**quiz)
        except (TypeError, KeyError, ValueError):
            return None

    def is_correct(self, user_answer: str):
        '''점답 확인'''
        return self.answer == user_answer

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

@dataclass
class Score:    # 점수
    score: float
    number: int
    correct: int
    hint: int
    time: datetime

    @classmethod
    def from_dict(cls, score_dict: dict):
        '''딕셔너리를 Score로 읽기'''
        try:    # 딕셔너리 속 "datatime" 키 값을 먼저 datatime으로 복구
            if isinstance(score_dict.get("time"), str):
                score_dict["time"] = datetime.fromisoformat(score_dict["time"])
            return cls(**score_dict)
        except (TypeError, KeyError, ValueError, AttributeError):   # 오류나면 None
            return None

    @property
    def to_string(self):
        '''점수 정보를 문자열로 리턴'''
        result = [f"점수: {self.score}점 {self.correct}/{self.number} | 힌트: {self.hint}/{self.number}"]
        result.append(f"날짜: {self.time}")
        return "\n".join(result)

    # 최고 점수 비교를 위해 넣은 equal, less than 던더 메소드
    def __eq__(self, other: Score):
        if not isinstance(other, Score):
            return NotImplemented
        return self.score == other.score
    
    def __lt__(self, other: Score):
        if not isinstance(other, Score):
            return NotImplemented
        return self.score < other.score

class EmptyQuizzesError(Exception):
    '''리스트 속 퀴즈가 없는 에러, 이거 안 던지면 아마 빈 리스트 참조해서 index 에러가 날 것'''
    def __init__(self, path: Path):
        super().__init__(f"퀴즈가 하나도 없습니다. {path}")
        self.path = path

class QuizGameManager:
    '''퀴즈, 점수 관리 및 게임 시작'''
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.quizzes: list[Quiz] = []
        self.scores: list[Score] = []
        self.highest_score: Score = None
        self.update()

    def update(self):
        '''내부 경로 및 퀴즈 업데이트'''
        self._quizzes_path = go_or_create_in_root(self.root_path, "quizzes.ndjson")
        self._scores_path = go_or_create_in_root(self.root_path, "scores.ndjson")
        self._highest_path = go_or_create_in_root(self.root_path, "highest.ndjson")

        self.quizzes = []
        for data in load_items(self._quizzes_path, dict):
            quiz = Quiz.from_dict(data)
            if quiz is not None:
                self.quizzes.append(quiz)

        self.scores = []
        for data in load_items(self._scores_path, dict):
            score = Score.from_dict(data)
            if score is not None:
                self.scores.append(score)

        raw_data = load_items(self._highest_path, dict)
        if raw_data != []:
            if isinstance(raw_data[0], dict):
                self.highest_score = Score.from_dict(raw_data[0])

    def quiz_add(self, quiz: Quiz):
        '''퀴즈 추가'''
        add_item(self._quizzes_path, asdict(quiz))
        self.update()

    def quiz_remove(self, index: int):
        '''퀴즈 제거'''
        remove_item(self._quizzes_path, index, dict)
        self.update()

    def save_score(self, score: Score):
        '''점수 저장'''
        if self.scores == []:
            write_item(self._scores_path, asdict(score))
            write_item(self._highest_path, asdict(score))
        else:
            add_item(self._scores_path, asdict(score))
        if self.highest_score is not None and self.highest_score < score:
            write_item(self._highest_path, score)
            self.highest_score = score
        self.update()

    def scores_reset(self):
        '''점수 기록 초기화'''
        write_item(self._scores_path, None)
        write_item(self._highest_path, None)
        self.update()

    def start(self) -> QuizGame:
        '''게임 시작, quizgame 리턴'''
        self.update()
        if not self.quizzes:
            raise EmptyQuizzesError("퀴즈가 하나도 없습니다.")
        return QuizGame(self._quizzes_path)

class QuizGame:
    '''퀴즈 게임의 상태 저장
    퀴즈 리스트에 직접 접근하게 하지 않고 index 필드와 next()메소드를 통해 다음 문제로 가는 방식으로 설계함'''
    def __init__(self, quizzes_path: Path):
        self.quizzes_path = quizzes_path
        self.quizzes: list[Quiz] = []
        self.correct = 0
        self.index = 0
        self.hint = False
        self.hint_counter = 0
        self.update()

    @property
    def is_finished(self):
        ''''''
        return self.end == self.index
    
    @property
    def number(self):   # 문제 수
        return len(self.quizzes)

    @property
    def end(self):      # 끝 index
        return self.number - 1

    def update(self):   # 퀴즈 업데이트
        self.quizzes = [Quiz.from_dict(quiz) for quiz in load_items(self.quizzes_path, dict)]

    @property
    def question(self) -> str:  # 현재 퀴즈를 문자열로 리턴
        return self.quizzes[self.index].to_string(self.index + 1, self.hint, False)

    @property
    def score(self) -> Score:   # 점수 필드를 따로 안 만들고 프로퍼티 데코레이터로 참조할 때마다 계산
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        if self.hint_counter != 0:
            new_score = Score( round(( (self.correct - (self.hint_counter / 2) ) / self.number) * 100, 2), self.number, self.correct, self.hint_counter,  now.isoformat())
            return new_score
        new_score = Score(int((self.correct / self.number) * 100), self.number, self.correct, self.hint_counter,  now.isoformat())
        return new_score

    def shuffle(self):  # 퀴즈 섞기
        random.shuffle(self.quizzes)

    def next(self): # 다음 문제(다음 question() 호출 시)
        self.index += 1
        self.hint = False

    def submit(self, submit: str | int):    # 정답 제출
        if self.hint == True:
            self.hint_counter += 1
        if self.quizzes[self.index].is_correct(submit) or \
            self.quizzes[self.index].is_correct(self.quizzes[self.index].choices[submit - 1]):
            self.correct +=1 
            return True
        else:
            return False 
