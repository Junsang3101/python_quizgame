# QuizGame 클래스

퀴즈와 점수의 `dataclass`인 `Quiz` 와 `Score`를 만들어서 `QuizGame`현재 퀴즈 게임 상태를 저장하고,  
메소드로 `cli`에서 조작하게 하였습니다.

`QuizGame` 인스턴스는 `QuizGameManager` 를 통해 받습니다.

``` python 
class QuizGame:
    '''퀴즈 게임의 상태 저장, 문제 수를 요청받음 입력이 없으면 모든 문제
    퀴즈 리스트에 직접 접근하게 하지 않고 index 필드와 next()메소드를 통해 다음 문제로 가는 방식으로 설계함'''
    def __init__(self, quizzes: list[Quiz], request: int = 0):
        self.quizzes: list[Quiz]
        self.correct = 0
        self.index = 0
        self.hint = False
        self.hint_counter = 0
        if request == 0:
            self.quizzes = quizzes
        elif isinstance(request, int) and request <= self.end:
            self.quizzes = random.sample(quizzes)
        print(len(quizzes), request, self.end)

    @property
    def is_finished(self):
        '''문제가 더 있으면 True'''
        return self.end == self.index
    
    @property
    def number(self):
        '''문제 수'''
        return len(self.quizzes)

    @property
    def end(self):
        '''마지막 문제 index'''
        return self.number - 1

    @property
    def quiz(self) -> str:
        '''퀴즈 문자열로 리턴'''
        return self.quizzes[self.index].to_string(self.index + 1, self.hint, False)

    @property
    def score(self) -> Score:
        '''현재 실시간 점수 계산해서 Score 객체로 돌려줌'''
        if self.hint_counter:
            new_score = Score( round(( (self.correct - (self.hint_counter / 2) ) / self.number) * 100, 2), self.number, self.correct, self.hint_counter,  now.isoformat())
        else: 
            new_score = Score(int((self.correct / self.number) * 100), self.number, self.correct, self.hint_counter,  now.isoformat()) 
        return new_score

    def shuffle(self):
        '''퀴즈 섞기'''
        random.shuffle(self.quizzes)

    def next(self):
        '''다음 문제 (다음 quiz() 호출 시)'''
        self.index += 1
        self.hint = False

    def submit(self, submit: str | int):
        '''정답 제출'''
        if self.hint == True:
            self.hint_counter += 1

        if isinstance(submit, int):
            submit -= 1
            if submit > len(self.quizzes[self.index].choices):
                return False
            print(submit, len(self.quizzes[self.index].choices))
            result = self.quizzes[self.index].is_correct(self.quizzes[self.index].choices[submit])
        else:
            result = self.quizzes[self.index].is_correct(submit)

        if result:
            self.correct += 1
            return True
        
        return False
```