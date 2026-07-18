from candor.modules.base import BaseModule
from candor.core.intent import Intent, Plan, ExecutionResult
from candor.shell.execute import run_command

class DigModule(BaseModule):
    name = "dig"
    aliases = ["dig", "dns"]
    description = "DNS lookups with dig"
    supported_targets = ["hostname", "domain"]

    actions = {
        "lookup": "basic DNS lookup",
        "axfr": "zone transfer attempt",
    }

    def build(self, intent: Intent) -> Plan:
        if intent.action == "axfr":
            args = ["dig", "AXFR", intent.target]
        else:
            args = ["dig", intent.target]
        return Plan(tool=self.name, action=intent.action, target=intent.target, command=args)

    def execute(self, plan: Plan) -> ExecutionResult:
        return run_command(plan.command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
