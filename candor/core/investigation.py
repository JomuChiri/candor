# candor/core/investigation.py
import json
import time
from pathlib import Path

class Investigation:
    def __init__(self, target: str):
        self.target = target
        self.resolved_ip = None
        self.commands_run = []
        self.evidence = {}
        self.start_time = time.strftime("%Y-%m-%d %H:%M:%S")

    def add_command(self, command: str, evidence_file: str = None, summary: str = None):
        self.commands_run.append(command)
        if evidence_file:
            self.evidence[command] = {
                "file": evidence_file,
                "summary": summary
            }

    def set_resolved_ip(self, ip: str):
        self.resolved_ip = ip

    def to_dict(self):
        return {
            "target": self.target,
            "resolved_ip": self.resolved_ip,
            "commands_run": self.commands_run,
            "evidence": self.evidence,
            "start_time": self.start_time
        }

    def save(self, base_dir="candor/investigations"):
        path = Path(base_dir) / self.target
        path.mkdir(parents=True, exist_ok=True)
        with open(path / "metadata.json", "w") as f:
            json.dump(self.to_dict(), f, indent=2)
