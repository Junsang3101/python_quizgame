from dataclasses import dataclass

@dataclass
class Quiz:
    question: str
    choices: list[str]
    answer: str

    # 클래스 메서드: 딕셔너리로부터 Quiz 인스턴스를 생성
    @classmethod
    def from_dict(cls, quiz: Quiz):
        return cls(**quiz)

    def get_question(self):
        return self.question

    def get_choices(self):
        return self.choices

    def is_correct(self, user_answer: str):
        return self.answer == user_answer


# json 파일을 읽어서 Quiz 인스턴스 리스트로 변환하는 기능을 제공

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
