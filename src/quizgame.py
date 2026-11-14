from datetime import datetime
from zoneinfo import ZoneInfo
from dataclasses import dataclass, asdict
from pathlib import Path
import random
from json_store import go_or_create_in_root, load_items, add_items, remove_item, write_items

# 퀴즈 구조체
@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: str

    @classmethod
    def from_dict(cls, quiz):
        return cls(**quiz)

    def is_correct(self, user_answer: str):
        return self.answer == user_answer

    def to_string(self, index, get_answer: bool):
        result = [f"{index}) {self.question}"]
        for j, choice in enumerate(self.choices, start=1):
            result.append(f"    {j}. {choice}")
        if get_answer is True:
            result.append(f"    정답: {self.answer}")
        return "\n".join(result)

@dataclass
class Score:
    score: int
    number: int
    correct: int
    time: datetime

    @classmethod
    def from_dict(cls, score_dict: dict):
        if isinstance(score_dict.get("time"), str):
            score_dict["time"] = datetime.fromisoformat(score_dict["time"])
        return cls(**score_dict)

    @property
    def to_string(self):
        result = [f"점수: {self.score}점 {self.correct}/{self.number}"]
        result.append(f"날자: {self.time}")
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
        self.update()

    @property
    def highest_score(self):
        if self.scores == []:
            return 0
        return max(self.scores)

    def update(self):
        self._quizzes_path = go_or_create_in_root(self.root_path, "quizzes.json")
        self._scores_path = go_or_create_in_root(self.root_path, "scores.json")
        self._highest_path = go_or_create_in_root(self.root_path, "highest_score.json")
        self.quizzes = [Quiz.from_dict(quiz) for quiz in load_items(self._quizzes_path)]
        self.scores = [Score.from_dict(score) for score in load_items(self._scores_path)]
        self._highest_path = self.highest_score

    def quiz_add(self, quiz: Quiz):
        add_items(self._quizzes_path, asdict(quiz))
        self.update()

    def quiz_remove(self, index: int):
        remove_item(self._quizzes_path, index)
        self.update()

    def score_save(self, score: Score):
        add_items(self._scores_path, asdict(score))
        self.update()

    def start(self) -> QuizGame:
        if not self.quizzes:
            raise EmptyQuizzesError("퀴즈가 하나도 없습니다.")
        return QuizGame(self._quizzes_path)

class QuizGame:
    def __init__(self, quizzes_path: Path):
        self.quizzes_path = quizzes_path
        self.quizzes: list[Quiz] = []
        self.correct = 0
        self.index = 0
        self.update()

    @property
    def is_finished(self) -> bool:
        return self.end == self.index

    def update(self) -> None:
        self.quizzes = [Quiz.from_dict(quiz) for quiz in load_items(self.quizzes_path)]

    @property
    def number(self) -> int:
        return len(self.quizzes)

    @property
    def end(self) -> int:
        return self.number - 1

    @property
    def score(self) -> Score:
        now = datetime.now(ZoneInfo("Asia/Seoul"))
        new_score = Score(int(self.correct / self.number * 100), self.number, self.correct, now.isoformat())
        return new_score

    def shuffle(self):
        random.shuffle(self.quizzes)

    def next(self) -> None:
        self.index += 1

    def questions(self):
        return self.quizzes[self.index].question

    def choices(self):
        return self.quizzes[self.index].choices

    def submit(self, submit: str | int):
        if self.quizzes[self.index].is_correct(submit) or \
            self.quizzes[self.index].is_correct(self.quizzes[self.index].choices[submit - 1]):
            self.correct +=1 
            return True
        else:
            return False 
