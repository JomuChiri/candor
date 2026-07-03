from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command

class NmapModule(BaseModule):
    name = "nmap"

    def build(self, intent: Intent) -> Plan:
        if not intent.target:
            raise ValueError("Target is required")

        # Decide command based on action
        if intent.action == "service_scan":
            return Plan(command=["nmap", "-sV", intent.target])
        elif intent.action == "os_detection":
            return Plan(command=["nmap", "-O", intent.target])
        else:
            # fallback: default args
            args = intent.args if intent.args else "-sV"
            return Plan(command=["nmap", args, intent.target])

    def execute(self, plan: Plan) -> ExecutionResult:
        return run_command(plan.command)
