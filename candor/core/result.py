from dataclasses import dataclass, field


@dataclass
class ExecutionResult:
    returncode: int
    stdout: str
    stderr: str
    elapsed: float
    status: str = field(init=False)

    def __post_init__(self):
        if self.returncode == 0:
            if self.stderr.strip():
                self.status = "warning"
            else:
                self.status = "success"
        else:
            self.status = "failed"