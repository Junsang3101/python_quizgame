from pathlib import Path
import json

'''
    quiz structure:
    [{
        "question": str,
        "choices": [str],
        "answer": str
    }]

'''


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    # 정답 확인 메서드
    def check_answer(self, user_answer):
        return user_answer.lower() == self.answer.lower()

    # 클래스 메서드: 딕셔너리로부터 Quiz 인스턴스를 생성
    @classmethod
    def from_dict(cls, data):
        return cls(data['question'], data['choices'], data['answer'])

# json 파일을 읽어서 Quiz 인스턴스 리스트로 변환하는 기능을 제공
class QuizLoader:
    @staticmethod
    def load_quizzes_from_json(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Quiz.from_dict(item) for item in data]

class QuizGame:
    def __init__(self, quizzes):
        self.quizzes = quizzes
        self.score = 0

    def start(self):
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"Question {idx}: {quiz.question}")
            for i, choice in enumerate(quiz.choices, start=1):
                print(f"{i}. {choice}")
            user_answer = input("답: ")
            if quiz.check_answer(user_answer):
                print("정답!")
                self.score += 1
            else:
                print(f"땡! 정답은: {quiz.answer}")

    # start 메소드 랩퍼로 바로 QuizGame.start(quizzes) 형태로 호출 가능하게 함
    @classmethod
    def play(cls, quizzes):
        game = cls(quizzes)
        game.start()

# 그냥 이 모듈 실행시 퀴즈 게임을 시작하도록 함
if __name__ == "__main__":
    DATA_PATH = Path(__file__).parent.parent / 'data' / 'default_quizzes.json'
    quizzes = QuizLoader.load_quizzes_from_json(DATA_PATH)
    QuizGame.play(quizzes)