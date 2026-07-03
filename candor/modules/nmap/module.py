from candor.modules.base import BaseModule
from candor.parser.planner import Plan
from candor.shell.execute import run_command

class NmapModule(BaseModule):
    name = "nmap"

    def build(self, intent):
        target = intent.get("target")
        args = intent.get("args", "-sV")
        return Plan(f"nmap {args} {target}")

    def execute(self, plan):
        return run_command(plan.command)
