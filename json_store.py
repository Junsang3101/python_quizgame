import json
from pathlib import Path
from typing import Any

JsonObject = dict[str, object]

def load_json(file_path: Path | str) -> Any:
    """JSON 파일을 읽어 반환합니다."""
    path = Path(file_path)
    return json.loads(path.read_bytes())

def save_json(file_path: Path | str, data: Any):
    """JSON 데이터를 파일에 씁니다."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=4), 
        encoding="utf-8"
    )