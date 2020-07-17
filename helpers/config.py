import json
from pathlib import Path

def make_data() -> bool:
    if not Path.exists("./data"):
        Path.mkdir("./data")
        return True
    return False

def make_cfg(name: str, initial_data: object = []) -> bool:
    if not Path.exists(f"./data/{name}.json"):
        with open(f"./data/{name}.json", 'w') as f:
            json.dump(initial_data, f)
        return True
    return False

def write_cfg(name: str, data: object):
    with open(f"./data/{name}.json", 'w') as f:
        json.dump(data, f)