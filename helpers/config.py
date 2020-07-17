import json
from pathlib import Path

def make_data() -> bool:
    path = Path("./data/")
    if not path.exists():
        path.mkdir()
        return True
    return False

def make_cfg(name: str, initial_data: object = []) -> bool:
    path = Path(f"./data/{name}.json")
    if not path.exists():
        with open(f"./data/{name}.json", 'w') as f:
            json.dump(initial_data, f)
        return True
    return False

def write_cfg(name: str, data: object):
    with open(f"./data/{name}.json", 'w') as f:
        json.dump(data, f)