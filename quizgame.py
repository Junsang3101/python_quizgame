from __future__ import annotations

from datetime import datetime, timezone, timedelta   # 시간
import json
import shutil
from dataclasses import dataclass, asdict   # dataclass 및 객체 전환(asdict)
from pathlib import Path        # 경로
import random                   # 무작위
# 만든 json i/o
from .json_store import load_json, save_json

kst = timezone(timedelta(hours=9))
now = datetime.now(kst)
'''
한국 기준 시간, zoneinfo 사용시 QuizGame.score 내부 주석처리된 코드를 풀고 글로벌 now 주석처리 바람
kst = timezone(timedelta(hour=9))
now = datetime(kst)
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
        return cls(**quiz)

    def is_correct(self, user_answer: str | int):
        '''점답 확인'''
        if isinstance(user_answer, int):
            if user_answer > len(self.choices):
                return False
            return self.answer == self.choices[user_answer]
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
        if isinstance(score_dict.get("time"), str):
            score_dict["time"] = datetime.fromisoformat(score_dict["time"])
        return cls(**score_dict)

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
        self.state_data: dict["quizzes": list[dict], "scores": list[dict], "highest": dict] = {}
        self.quizzes: list[Quiz] = []
        self.scores: list[Score] = []
        self.highest: Score = None

        if not root_path.exists():  # 파일이 없는 경우 만듦
            root_path.parent.mkdir(parents=True, exist_ok=True)
            save_json(root_path, None)

        try:
            self.data = load_json(self.root_path)
        except json.decoder.JSONDecodeError:    # 파일 읽기 실패할 경우 기존 파일 백업
            backup_path = self.root_path.parent / "backup"
            backup_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{now.isoformat().replace(':', '-')}.json"
            shutil.copy2(root_path, backup_path / file_name)
            self.data = None

        self.state_data = self.data or {}
        if self.state_data is not None: # 비어있을경우 필드 초기화
            temp_quizzes = self.state_data.get("quizzes") or []
            temp_scores = self.state_data.get("scores") or []
            temp_highest = self.state_data.get("highest")
            self.quizzes = [Quiz.from_dict(quiz) for quiz in temp_quizzes]
            self.scores = [Score.from_dict(score) for score in temp_scores]
            self.highest = Score.from_dict(self.state_data.get("highest")) if temp_highest is not None else None

        if not len(self.quizzes):   # 퀴즈가 하나도 없으면 기본 퀴즈 불러옴
            default_quizzes = self.root_path.parent/"default_quizzes.json"
            if not default_quizzes.exists():
                print("기본 퀴즈가 존재하지 않습니다.")
                return
            self.quizzes = [Quiz.from_dict(quiz) for quiz in load_json(default_quizzes)]
            print("기본 퀴즈를 가져왔습니다.")

    def quiz_add(self, quiz: Quiz):
        '''퀴즈 추가'''
        self.quizzes.append(quiz)

    def quiz_remove(self, index: int):
        '''퀴즈 제거'''
        try:
            self.quizzes.pop(index)
        except IndexError:
            raise IndexError

    def save_score(self, score: Score):
        '''점수 저장'''
        self.scores.append(score)
        if self.highest is None or self.highest < score:
            self.highest = score

    def scores_reset(self):
        '''점수 기록 초기화'''
        self.scores = []
        self.highest = None
        print(self.highest)

    def save(self):
        '''상태 정보 파일로 저장'''
        self.state_data["quizzes"] = [asdict(quiz) for quiz in self.quizzes]
        if self.scores is not None:
            for score in self.scores:
                score.time = score.time.isoformat()
            self.state_data["scores"] = [asdict(score) for score in self.scores]
        if isinstance(self.highest, Score):
            self.highest.time = self.highest.time.isoformat()
            self.state_data["highest"] = asdict(self.highest)
        self.state_data["highest"] = self.highest
        save_json(self.root_path, self.state_data)

    def start(self, request: int = 0) -> QuizGame:
        '''게임 시작 -> quizgame 리턴, request 만큼 문제를 냄'''
        if not self.quizzes:
            raise EmptyQuizzesError("퀴즈가 하나도 없습니다.")
        if request == 0: request = len(self.quizzes)
        return QuizGame(self.quizzes, request)

class QuizGame:
    '''퀴즈 게임의 상태 저장, 문제 수를 요청받음 입력이 없으면 모든 문제
    퀴즈 리스트에 직접 접근하게 하지 않고 index 필드와 next()메소드를 통해 다음 문제로 가는 방식으로 설계함'''
    def __init__(self, quizzes: list[Quiz], request: int = 0):
        self.quizzes: list[Quiz]
        self.correct = 0
        self.index = 0
        self.hint = False
        self.hint_counter = 0
        if request == 0:
            self.quizzes = quizzes
        elif isinstance(request, int) and request <= self.end:
            self.quizzes = random.sample(quizzes)
        print(len(quizzes), request, self.end)

    @property
    def is_finished(self):
        '''문제가 더 있으면 True'''
        return self.end == self.index
    
    @property
    def number(self):
        '''문제 수'''
        return len(self.quizzes)

    @property
    def end(self):
        '''마지막 문제 index'''
        return self.number - 1

    @property
    def quiz(self) -> str:
        '''퀴즈 문자열로 리턴'''
        return self.quizzes[self.index].to_string(self.index + 1, self.hint, False)

    @property
    def score(self) -> Score:
        '''현재 실시간 점수 계산해서 Score 객체로 돌려줌'''
        if self.hint_counter:
            new_score = Score( round(( (self.correct - (self.hint_counter / 2) ) / self.number) * 100, 2), self.number, self.correct, self.hint_counter,  now.isoformat())
        else: 
            new_score = Score(int((self.correct / self.number) * 100), self.number, self.correct, self.hint_counter,  now.isoformat()) 
        return new_score

    def shuffle(self):
        '''퀴즈 섞기'''
        random.shuffle(self.quizzes)

    def next(self):
        '''다음 문제 (다음 quiz() 호출 시)'''
        self.index += 1
        self.hint = False

    def submit(self, submit: str | int):
        '''정답 제출'''
        if self.hint == True:
            self.hint_counter += 1

        if isinstance(submit, int):
            submit -= 1
            if submit > len(self.quizzes[self.index].choices):
                return False
            print(submit, len(self.quizzes[self.index].choices))
            result = self.quizzes[self.index].is_correct(self.quizzes[self.index].choices[submit])
        else:
            result = self.quizzes[self.index].is_correct(submit)

        if result:
            self.correct += 1
            return True
        
        return False
        