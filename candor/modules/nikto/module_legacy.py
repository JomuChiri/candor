from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class NiktoModule(BaseModule):
    name = "nikto"
    aliases = ["nikto", "webscan"]
    description = "Web vulnerability scanning with Nikto"
    supported_targets = ["ip", "hostname", "url"]

    actions = {
        "scan": "-h",   # basic scan
        "ssl": "-ssl",  # force SSL
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for Nikto based on intent.
        """
        if intent.action == "scan":
            args = ["nikto", "-h", intent.target]
        elif intent.action == "ssl":
            args = ["nikto", "-ssl", "-h", intent.target]
        else:
            args = ["nikto", "-h", intent.target]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("nikto", {}).get("default_args", [])
        command = ["nikto"] + default_args + plan.command[1:]
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
