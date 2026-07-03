from dataclasses import dataclass
from datetime import datetime
from candor.core.intent import Intent
from candor.core.result import ExecutionResult

@dataclass
class Job:
    id: int
    intent: Intent
    started: datetime
    finished: datetime
    result: ExecutionResult
