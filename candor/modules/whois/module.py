from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.shell.execute import run_command

class WhoisModule(BaseModule):
    name = "whois"

    def build(self, intent: Intent) -> Plan:
        if not intent.target:
            raise ValueError("Target is required")
        return Plan(command=["whois", intent.target])

    def execute(self, plan: Plan):
        return run_command(plan.command)

