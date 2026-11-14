import json
from pathlib import Path

JsonObject = dict[str, object]

def _as_list(data: JsonObject | list[JsonObject]) -> list[JsonObject]:
    return data if isinstance(data, list) else [data]

def find_in_root(directory_path: str | Path, filename: str) -> Path | None:
    dir_path = Path(directory_path)
    file_path = dir_path / filename
    
    if file_path.is_file():
        return file_path
    return None

def go_or_create_in_root(directory_path: str | Path, filename: str, default_data = None) -> Path:
    if default_data is None:
        default_data = []
    dir_path = Path(directory_path)
    file_path = find_in_root(dir_path, filename)
    if file_path is None:
        file_path = dir_path / filename
    if not file_path.is_file():
        write_items(file_path, default_data)
    return file_path

def load_items(path: Path) -> list[JsonObject]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with open(path, "r", encoding="utf-8") as source:
        data = json.load(source)

    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ValueError(f"Expected a JSON object or array of objects in {path}")

    return data


def write_items(path: Path, data: JsonObject | list[JsonObject]) -> None:
    items = _as_list(data)
    with open(path, "w", encoding="utf-8") as target:
        json.dump(items, target, ensure_ascii=False, indent=2, default=str)

def add_items(path: Path, data: JsonObject | list[JsonObject]) -> None:
    new_items = _as_list(data)
    existing_items = load_items(path) if path.exists() else []
    existing_items.extend(new_items)
    write_items(path, existing_items)

def remove_item(path: Path, index: int) -> None:
    items = load_items(path)
    items.pop(index)
    write_items(path, items)
