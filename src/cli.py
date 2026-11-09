import json
from pathlib import Path
from enum import Enum, auto
from quizgame import Quiz, QuizGame, QuizLoader, DEFAULT_QUIZZES_PATH


class QuizGameCLI:
    def __init__(self):
        self.path = DEFAULT_QUIZZES_PATH
        self.quizzes = QuizLoader.from_json(self.path)

    def main_menu(self):
        while True:
            print("\n=== 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 목록")
            print("3. 점수 확인")
            print("4. 종료")
            choice = input("선택: ")

            if choice == '1':
                return self.solve()
            elif choice == '2':
                return self.quiz_list()
            elif choice == '3':
                pass
            elif choice == '4':
                print("게임을 종료합니다.")
                return
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

    def solve(self):
        quizgame = QuizGame(self.quizzes)
        idx = 1
        while not quizgame.is_finished:
            current_quiz = quizgame.current_quiz
            print(f"{idx}) {current_quiz.question}")
            for jdx, choice in enumerate(current_quiz.choices, start=1):
                print(f"    {jdx}. {choice}")
            user_answer = input("선택: ")
            quizgame.submit(current_quiz.choices[int(user_answer) - 1])
            idx += 1
            print("\n")
            
        print(f"점수: {quizgame.score}/{len(quizgame.quizzes)}")        
        return self.main_menu()
        
    def quiz_list(self):
        for idx, quiz in enumerate(self.quizzes, start=1):
            print(f"{idx}) {quiz.question}")

        print("\n=== 퀴즈 목록 ===")
        print("1. 퀴즈 추가")
        print("2. 퀴즈 삭제")
        print("3. 퀴즈 전부 삭제")
        print("4. 퀴즈 초기화")
        print("5. 메인 메뉴")

        user_choice = input("선택:")
        if user_choice == '1':
            pass
        elif user_choice == '2':
            pass
        elif user_choice == '3':
            pass
        elif user_choice == '4':
            pass
        elif user_choice == '5':
            return self.main_menu()

    def run(self):
            self.main_menu()

# 그냥 이 모듈 실행시 퀴즈 게임을 시작하도록 함
if __name__ == "__main__":
    quiz_cli = QuizGameCLI()
    quiz_cli.run()