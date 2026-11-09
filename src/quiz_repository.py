import json
from pathlib import Path
from quizgame import Quiz

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent / 'data'
DEFAULT_QUIZZES_PATH = DATA_DIR / 'default_quizzes.json'
CUSTOM_QUIZZES_PATH = DATA_DIR / 'custom_quizzes.json'
SCORE_HISTORY_PATH = DATA_DIR / 'score_history.json'

# 인자(경로)의 파일 로드해서 돌려줌
def load_quizzes(path):
    with open(path, "r", encoding="utf-8") as source:
        data = json.load(source)
        return [Quiz.from_dict(item) for item in data]