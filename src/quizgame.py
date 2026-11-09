from pathlib import Path
from dataclasses import dataclass
import json

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent / 'data'
DEFAULT_QUIZZES_PATH = DATA_DIR / 'default_quizzes.json'
CUSTOM_QUIZZES_PATH = DATA_DIR / 'custom_quizzes.json'
SCORE_HISTORY_PATH = DATA_DIR / 'score_history.json'

'''
    quiz structure:
    [{
        "question": str,
        "choices": [str],
        "answer": str
    }]

'''

@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: str

    # 클래스 메서드: 딕셔너리로부터 Quiz 인스턴스를 생성
    @classmethod
    def from_dict(cls, quiz):
        return cls(**quiz)

    def get_question(self):
        return self.question

    def get_choices(self):
        return self.choices

    def is_correct(self, user_answer:str):
        return self.answer == user_answer


# json 파일을 읽어서 Quiz 인스턴스 리스트로 변환하는 기능을 제공
class QuizLoader:
    @staticmethod
    def from_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Quiz.from_dict(item) for item in data]


class QuizGame:
    def __init__(self, quizzes: list[Quiz]):
        self.quizzes = quizzes
        self.score = 0
        self.current_index = 0

    # 마지막 인덱스인지 확인
    @property
    def is_finished(self):
        return self.current_index >= len(self.quizzes)

    # 현재 퀴즈 얻기
    @property
    def current_quiz(self) -> Quiz | None:
        if self.current_index >= len(self.quizzes):
            return None
        return self.quizzes[self.current_index]

    # 정답 확인 후 퀴즈 인덱스 증가
    def submit(self, user_answer: str) -> bool:
        if self.is_finished:
            raise ValueError("모든 퀴즈를 완료했습니다.")

        quiz = self.current_quiz
        correct = quiz.is_correct(user_answer)

        if correct:
            self.score += 1

        self.current_index += 1
        return correct

if __name__ == "__main__":
    quizgame = QuizGame(QuizLoader.from_json(DEFAULT_QUIZZES_PATH))
