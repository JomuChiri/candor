# candor/core/intent.py
from dataclasses import dataclass, field

@dataclass
class Intent:
    tool: str
    target: str
    args: str = ""
    action: str = ""
    options: dict = field(default_factory=dict)
