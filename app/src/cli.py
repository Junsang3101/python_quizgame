import json
from pathlib import Path
from quizgame import QuizGame, QuizLoader

# 기본 퀴즈 파일 경로
DATA_PATH = Path(__file__).parent.parent / 'data' / 'default_quizzes.json'

class QuizGameCLI:
    def __init__(self):
        pass

    def main_menu(self):
        while True:
            print("\n=== 퀴즈 게임 ===")
            print("1. 퀴즈 시작")
            print("2. 종료")
            choice = input("선택: ")

            if choice == '1':
                self.start_quiz()
            elif choice == '2':
                print("게임을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

    def start_quiz(self):
        quizzes = QuizLoader.load_quizzes_from_json(DATA_PATH)
        QuizGame.play(quizzes)


# 그냥 이 모듈 실행시 퀴즈 게임을 시작하도록 함
if __name__ == "__main__":
    quiz_cli = QuizGameCLI()
    quiz_cli.main_menu()