from quizgame import QuizGame, Quiz
from data_storage import DEFAULT_QUIZZES_PATH
from data_storage import add_json, load_json, remove_json

class QuizGameCLI:
    def __init__(self):
        self.path = DEFAULT_QUIZZES_PATH
        self.quizzes = []
        self.quizzes_update()

    def print_quiz(self, i: int, quiz: Quiz):
        print(f"{i}) {quiz.question}")
        for i, choice in enumerate(quiz.choices, start=1):
            print(f"    {i}. {choice}")

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
        index = 1
        while not quizgame.is_finished:
            quiz = quizgame.current_quiz
            self.print_quiz(index, quiz)
            user_answer = input("선택: ")
            quizgame.submit(quiz.choices[int(user_answer) - 1])
            index += 1
            print("\n")
            
        print(f"점수: {quizgame.score}/{len(quizgame.quizzes)}")        
        return self.main_menu()
        
    def quiz_list(self):
        print("\n=== 퀴즈 목록 ===")
        for i, quiz in enumerate(self.quizzes, start=1):
            self.print_quiz(i, quiz)
        print("\n1. 퀴즈 추가")
        print("2. 퀴즈 삭제")
        print("3. 퀴즈 전부 삭제")
        print("4. 퀴즈 초기화")
        print("5. 메인 메뉴")

        user_choice = input("선택:")
        if user_choice == '1':
            self.quiz_add()
        elif user_choice == '2':
            self.quiz_remove()
        elif user_choice == '3':
            pass
        elif user_choice == '4':
            pass
        elif user_choice == '5':
            return self.main_menu()

    def quiz_add(self):
        print("=== 퀴즈 추가===")
        question = input("문제: ")
        choices = []
        choices.append(input("1. "))
        choices.append(input("2. "))
        choices.append(input("3. "))
        choices.append(input("4. "))
        answer = choices[int(input("정답 번호: ")) - 1]
        add_json(self.path, {"question": question, "choices": choices, "answer": answer})
        self.quizzes_update()
        return self.quiz_list()

    def quiz_remove(self):
        print("=== 퀴즈 삭제 ===")
        self.quizzes_update()
        for i, quiz in enumerate(self.quizzes, start=1):
            print(f"{i}) {quiz.question}")
        choice = int(input("선택: "))
        remove_json(self.path, choice - 1)
        self.quiz_list()

    def quizzes_update(self):
        self.quizzes = [Quiz.from_dict(quiz) for quiz in load_json(self.path)]

    def run(self):
            self.main_menu()

# 그냥 이 모듈 실행시 퀴즈 게임을 시작하도록 함
if __name__ == "__main__":
    quiz_cli = QuizGameCLI()
    quiz_cli.run()