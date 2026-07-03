# candor/core/plan.py
from dataclasses import dataclass

@dataclass
class Plan:
    command: list[str] 
