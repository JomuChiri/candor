# candor/core/case.py
import json
from pathlib import Path

class Case:
    def __init__(self, name: str, base_dir="candor/cases"):
        self.name = name
        self.base_dir = Path(base_dir) / name
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.base_dir / "case.json"

        if self.file.exists():
            with open(self.file) as f:
                self.data = json.load(f)
        else:
            self.data = {"name": name, "investigations": []}
            self.save()

    def add_investigation(self, target: str):
        if target not in self.data["investigations"]:
            self.data["investigations"].append(target)
            self.save()

    def list_investigations(self):
        return self.data["investigations"]

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)
