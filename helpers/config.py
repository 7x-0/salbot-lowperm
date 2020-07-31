import json
from pathlib import Path

DATAPATH = Path() / "data"
if not DATAPATH.exists():
    DATAPATH.mkdir()


class ConfigUtil:
    def __init__(self, data_name: str, default=None):
        self.path: Path = DATAPATH / (data_name + ".json")
        if not self.path.exists():
            self.data = default
            with self.path.open("w+") as f:
                json.dump(self.data, f)
        else:
            with self.path.open() as f:
                self.data = json.load(f)

    def read(self):
        return self.data

    def write(self, data):
        self.data = data
        with self.path.open("w") as f:
            json.dump(self.data, f)

    def save(self):
        with self.path.open("w") as f:
            json.dump(self.data, f)

