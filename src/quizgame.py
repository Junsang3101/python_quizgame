from datetime import datetime
from zoneinfo import ZoneInfo
from dataclasses import dataclass, asdict
from pathlib import Path
import random
from ndjson_store import go_or_create_in_root, load_items, add_item, remove_item, write_item

@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: str
    hint: str

    @classmethod
    def from_dict(cls, quiz):
        try:
            return cls(**quiz)
        except (TypeError, KeyError, ValueError):
            return None

    def is_correct(self, user_answer: str):
        return self.answer == user_answer

    def to_string(self, index, get_hint: bool, get_answer: bool):
        result = [f"{index}) {self.question}"]
        if get_hint is True:
            result.append(f"(힌트: {self.hint})")
        for j, choice in enumerate(self.choices, start=1):
            result.append(f"    {j}. {choice}")
        if get_answer is True:
            result.append(f"    정답: {self.answer}")
        return "\n".join(result)

@dataclass
class Score:
    score: float
    number: int
    correct: int
    hint: int
    time: datetime

    @classmethod
    def from_dict(cls, score_dict: dict):
        try:
            if isinstance(score_dict.get("time"), str):
                score_dict["time"] = datetime.fromisoformat(score_dict["time"])
            return cls(**score_dict)
        except (TypeError, KeyError, ValueError, AttributeError):
            return None

    @property
    def to_string(self):
        result = [f"점수: {self.score}점 {self.correct}/{self.number} | 힌트: {self.hint}/{self.number}"]
        result.append(f"날짜: {self.time}")
        return "\n".join(result)

    def __eq__(self, other: Score):
        if not isinstance(other, Score):
            return NotImplemented
        return self.score == other.score
    
    def __lt__(self, other: Score):
        if not isinstance(other, Score):
            return NotImplemented
        return self.score < other.score

class EmptyQuizzesError(Exception):
    def __init__(self, path: Path):
        super().__init__(f"퀴즈가 하나도 없습니다. {path}")
        self.path = path

class QuizGameManager:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.quizzes: list[Quiz] = []
        self.scores: list[Score] = []
        self.highest_score: Score = None
        self.update()

    def update(self):
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
        add_item(self._quizzes_path, asdict(quiz))
        self.update()

    def quiz_remove(self, index: int):
        remove_item(self._quizzes_path, index, dict)
        self.update()

    def save_score(self, score: Score):
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
        write_item(self._scores_path, None)
        write_item(self._highest_path, None)
        self.update()

    def start(self) -> QuizGame:
        self.update()
        if not self.quizzes:
            raise EmptyQuizzesError("퀴즈가 하나도 없습니다.")
        return QuizGame(self._quizzes_path)

class QuizGame:
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
        return self.end == self.index
    
    @property
    def number(self):
        return len(self.quizzes)

    @property
    def end(self):
        return self.number - 1

    def update(self):
        self.quizzes = [Quiz.from_dict(quiz) for quiz in load_items(self.quizzes_path, dict)]

    @property
    def question(self) -> str:
        return self.quizzes[self.index].to_string(self.index + 1, self.hint, False)

    @property
    def score(self) -> Score:
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        if self.hint_counter != 0:
            new_score = Score( round(( (self.correct - (self.hint_counter / 2) ) / self.number) * 100, 2), self.number, self.correct, self.hint_counter,  now.isoformat())
            return new_score
        new_score = Score(int((self.correct / self.number) * 100), self.number, self.correct, self.hint_counter,  now.isoformat())
        return new_score

    def shuffle(self):
        random.shuffle(self.quizzes)

    def next(self):
        self.index += 1
        self.hint = False

    def submit(self, submit: str | int):
        if self.hint == True:
            self.hint_counter += 1
        if self.quizzes[self.index].is_correct(submit) or \
            self.quizzes[self.index].is_correct(self.quizzes[self.index].choices[submit - 1]):
            self.correct +=1 
            return True
        else:
            return False 
