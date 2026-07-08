# candor/core/findings.py
import json
from pathlib import Path
from candor.core.mitre import map_to_mitre

class FindingsDB:
    def __init__(self, base_dir="candor/findings"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.db_file = self.base_dir / "findings.json"
        if self.db_file.exists():
            with open(self.db_file) as f:
                self.data = json.load(f)
        else:
            self.data = {
                "Critical": [],
                "High": [],
                "Medium": [],
                "Informational": []
            }

    def add_finding(self, severity: str, description: str, source: str, target: str):
        tactic = map_to_mitre(source)
        if severity not in self.data:
            severity = "Informational"
        self.data[severity].append({
            "description": description,
            "source": source,
            "target": target,
            "mitre": tactic
        })
        self.save()

    def save(self):
        with open(self.db_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def list_findings(self):
        return self.data
