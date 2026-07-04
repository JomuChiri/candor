# candor/modules/whois/module.py
from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command

class WhoisModule(BaseModule):
    name = "whois"
    aliases = ["whois", "lookup"]
    actions = {
        "lookup": None,  # no extra flag needed
    }

    def build(self, intent: Intent) -> Plan:
        if not intent.target:
            raise ValueError("Target is required")

        args = [self.name]
        args.append(intent.target)

        return Plan(command=args)

    def execute(self, plan: Plan) -> ExecutionResult:
        return run_command(plan.command)
