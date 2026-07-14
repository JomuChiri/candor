# candor/core/plan.py
from dataclasses import dataclass

@dataclass
class Plan:
    """
    Execution plan for a single tool action.
    Self-contained: carries tool, action, target, and command string.
    """

    def __init__(self, tool: str, action: str, target: str, command: str):
        self.tool = tool
        self.action = action
        self.target = target
        self.command = command

    def __repr__(self):
        return f"<Plan tool={self.tool} action={self.action} target={self.target}>"

    def run(self):
        """
        Placeholder for execution logic.
        In v0.6, execution is delegated to executor.py.
        """
        raise NotImplementedError("Plan.run() should be executed via executor")
