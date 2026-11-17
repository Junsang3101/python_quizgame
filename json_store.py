import json
import shutil 
from pathlib import Path
from typing import Any
from datetime import datetime, timezone, timedelta

kst = timezone(timedelta(hours=9))
now = datetime.now(kst)

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

def s_load_json(file_path: Path | str) -> Any:
    '''josn 데이터 접근하나, 꺠졌다면 백업합니다.'''
    path: Path = Path(file_name)
    data = None

    try:
        data = load_json(path)
    except json.decoder.JSONDecodeError:    # 파일 읽기 실패할 경우 기존 파일 백업한 후 작성
        backup_path = path.parent / "backup"
        backup_path.mkdir(parents=True, exist_ok=True)
        file_name = f"{now.isoformat().replace(':', '-')}.json"
        shutil.copy2(path, backup_path / file_name)

    return data