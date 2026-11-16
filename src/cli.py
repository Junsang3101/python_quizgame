from .quizgame import QuizGameManager, Quiz, EmptyQuizzesError
from pathlib import Path

PATH = Path(__file__).parent / 'data'

def run():
    manager = QuizGameManager(PATH)
    main_menu(manager)

def main_menu(manager: QuizGameManager):
    print("\n=== 메인 메뉴 ====")
    print("1. 퀴즈 시작")
    print("2. 퀴즈 목록")
    print("3. 기록")
    print("4. 기록 초기화")
    print("5. 종료")
    try:
        choice = int(input("선택 : "))
    except:
        print("\n--<다시 입력해주세요>--")
        return main_menu(manager)
    if choice == 1:
        return start_menu(manager)
    elif choice == 2:
        return list_menu(manager)
    elif choice == 3:
        return score_list(manager)
    elif choice == 4:
        manager.scores_reset()
        print("점수 기록이 초기화되었습니다.")
        return main_menu(manager)
    elif choice == 5:
        manager.update()
        manager.save_score
        print("게임을 종료합니다.\n")
    else:
        print("--<다시 입력해주세요>--")
        return main_menu(manager)

def start_menu(manager: QuizGameManager):
    try:
        quizgame = manager.start()
    except EmptyQuizzesError:
        print("퀴즈가 하나도 없습니다.")
        return main_menu(manager)
    quizgame.shuffle()
    while True:
        print(f"\n{quizgame.question}")
        try:
            choice = int(input("선택 (0 = 힌트): "))
        except ValueError:
            print("\n--<다시 입력해주세요>--")
            continue
        if choice == 0:
            quizgame.hint = True
            continue
        elif isinstance(choice ,int):
            quizgame.submit(choice)
        if quizgame.is_finished:
            break
        quizgame.next()
    score = quizgame.score
    manager.save_score(score)
    print(f"\n{score.to_string}\n")
    return main_menu(manager)

def list_menu(manager: QuizGameManager):
    print("\n=== 퀴즈 목록 ===")
    for i, quiz in enumerate(manager.quizzes, start=1):
        print(f"{quiz.to_string(i, True, True)}\n")
    print("1. 퀴즈 추가")
    print("2. 퀴즈 삭제")
    print("3. 메인 메뉴")
    try:
        choice = int(input("선택: "))
    except ValueError:
        print("--<다시 입력해주세요>--")
        return list_menu(manager)
              
    if choice == 1:
        add_menu(manager)
    elif choice == 2:
        remove_menu(manager)
    elif choice == 3:
        return main_menu(manager)
    else:
        print("--<다시 입력해주세요>--")
        return list_menu(manager)

def add_menu(manager: QuizGameManager):
    try:
        new_quiz = Quiz(input("질문: "), [], None, "")
        for i in range(1, 5, 1):
            new_quiz.choices.append(input(f"보기 {i}: "))
        new_quiz.hint = input("힌트: ")
        new_quiz.answer = input("정답: ")
    except ValueError:
        print("--<퀴즈 추가 취소>--")
    
    manager.quiz_add(new_quiz)
    return list_menu(manager)

def remove_menu(manager: QuizGameManager):
    try:
        choice = int(input("삭제 (0 = 취소): ")) - 1
    except (TypeError, IndexError, ValueError):
        print("다시 입력해주세요 (0 = 취소): ")
        return remove_menu(manager)
    
    if choice == -1:
        return list_menu(manager)
    manager.quiz_remove(choice)
    return list_menu(manager)

def score_list(manager: QuizGameManager):
    print("\n=== 기록 ===")
    for score in manager.scores:
        print(f"{score.to_string}\n")
    if manager.highest_score != None:
        print(f"\n=== 최고 점수 ===\n{manager.highest_score.to_string}")
    return main_menu(manager)