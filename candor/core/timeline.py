# candor/core/timeline.py
import time
from pathlib import Path
import json

class Timeline:
    def __init__(self, target):
        self.target = target
        self.events = []

    def add_event(self, action):
        self.events.append({
            "time": time.strftime("%H:%M:%S"),
            "action": action
        })

    def save(self):
        path = Path(f"candor/investigations/{self.target}/timeline.json")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.events, f, indent=2)
