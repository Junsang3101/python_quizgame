from quizgame import QuizGameManager, Quiz, Score
from pathlib import Path

PATH = Path(__file__).parent / 'data'

def run():
    manager = QuizGameManager(PATH)
    main_menu(manager)

def main_menu(manager: QuizGameManager):
    quizzes = manager.quizzes
    print("\n=== 메인 메뉴 ====")
    print("1. 퀴즈 시작")
    print("2. 퀴즈 목록")
    print("3. 기록")
    print("4. 종료")
    try:
        choice = int(input("선택: "))
        if choice == 1:
            return start_menu(manager)
        elif choice == 2:
            return list_menu(manager)
        elif choice == 3:
            return score_list(manager)
        elif choice == 4:
            print("게임을 종료합니다.\n")
        else:
            print("숫자를 입력하세요.")
    except ValueError:
        print("잘못된 값.")

def start_menu(manager: QuizGameManager):
    quizgame = manager.start()
    #quizgame.shuffle()
    quizzes = quizgame.quizzes
    while True:
        index = quizgame.index
        print(f"\n{quizzes[index].to_string(index + 1, False)}")
        choice = int(input("선택: "))
        quizgame.submit(choice)
        if quizgame.is_finished:
            break
        quizgame.next()
    score = quizgame.score
    manager.score_save(score)
    print(f"\n{score.to_string}\n")
    return main_menu(manager)

def list_menu(manager: QuizGameManager):
    print("\n=== 퀴즈 목록 ===")
    for i, quiz in enumerate(manager.quizzes, start=1):
        print(quiz.to_string(i, True))
    print("\n1. 퀴즈 추가")
    print("2. 퀴즈 삭제")
    print("3. 메인 메뉴")
    try:
        choice = int(input("선택: "))
        if choice == 1:
            add_menu(manager)
        elif choice == 2:
            remove_menu(manager)
        elif choice == 3:
            return main_menu(manager)
        else:
            print("숫자를 입력하세요.")
    except ValueError:
        print("잘못된 값.")

def add_menu(manager: QuizGameManager):
    new_quiz = Quiz(input("질문: "), [], None)
    for i in range(0, 4, 1):
        new_quiz.choices.append(input(f"보기 {i}: "))
    new_quiz.answer = input("정답: ")
    
    manager.quiz_add(new_quiz)
    return list_menu(manager)

def remove_menu(manager: QuizGameManager):
    choice = int(input("삭제: ")) - 1
    manager.quiz_remove(choice)
    return list_menu(manager)

def score_list(manager: QuizGameManager):
    print("\n=== 기록 ===")
    for score in manager.scores:
        print(score.to_string)
    print(f"\n=== 최고 점수 ===\n{manager.highest_score.to_string}")

# 그냥 이 모듈 실행시 퀴즈 게임을 시작하도록 함
if __name__ == "__main__":
    run()