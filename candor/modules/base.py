from abc import ABC, abstractmethod
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult

class BaseModule(ABC):
    name: str = ""

    @abstractmethod
    def build(self, intent: Intent) -> Plan:
        pass

    @abstractmethod
    def execute(self, plan: Plan) -> ExecutionResult:
        pass
