import json
from pathlib import Path
from dataclasses import dataclass

# 데이터 파일 경로
DATA_DIR = Path(__file__).parent / 'data'
DEFAULT_QUIZZES_PATH = DATA_DIR / 'default_quizzes.json'
QUIZZES_PATH = DATA_DIR / 'quizzes.json'
SCORE_PATH = DATA_DIR / 'score.json'

@dataclass
class Score:
    _score: int
    number: int
    correct: int

    @classmethod
    def from_dict(cls, score: dict):
        return cls(**score)

    @property
    def score(self) -> float:
        return round(self.correct / self.number, 2)

    @property
    def __repr__(self):
        return Score(self.score, self.number, self.correct)
    
JsonObject = dict[str, object]

# json 내용물을 리스트화 한다
def _as_list(data: JsonObject | list[JsonObject]) -> list[JsonObject]:
    return data if isinstance(data, list) else [data]

# json 파일 읽기
def load_json(path: Path) -> list[JsonObject]:
    with open(path, "r", encoding="utf-8") as source:
        data = json.load(source)
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError(f"Expected a JSON object or array of objects in {path}")

    return data

# json 덮어쓰기
def write_json(path: Path, data: JsonObject | list[JsonObject]) -> None:
    items = _as_list(data)
    with open(path, "w", encoding="utf-8") as target:
        json.dump(items, target, ensure_ascii=False, indent=2)

# json 읽고 + data
def add_json(path: Path, data: JsonObject | list[JsonObject]) -> None:
    items = _as_list(data)
    if path.exists():
        serialized = load_json(path)
    else:
        serialized = []
    serialized.extend(items)
    write_json(path, serialized)

def remove_json(path: Path, index: int) -> None:
    items = load_json(path)
    items.pop(index)
    write_json(path, items)


if __name__ == "__main__":
    '''
    add_json(
        SCORE_PATH,
        asdict(Score(_score=100, number=10, correct=10))
    )
    '''
    remove_json(
        SCORE_PATH,
        0
    )