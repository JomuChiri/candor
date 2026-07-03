# candor/core/result.py
from dataclasses import dataclass

@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    returncode: int
    elapsed: float
