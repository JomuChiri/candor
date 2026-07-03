from candor.modules.base import BaseModule
from candor.parser.planner import Plan
from candor.shell.execute import run_command

class WhoisModule(BaseModule):
    name = "whois"

    def build(self, intent):
        target = intent.get("target")
        return Plan(f"whois {target}")

    def execute(self, plan):
        return run_command(plan.command)
