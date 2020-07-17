import json
from pathlib import Path

def make_data():
    if not Path.exists("./data"):
        Path.mkdir("./data")

def make_cfg(name: str, initial_data: object = []):
    if not Path.exists(f"./data/{name}.json"):
        with open(f"./data/{name}.json", 'w') as f:
            json.dump(initial_data, f)

