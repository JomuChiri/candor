from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class Enum4LinuxModule(BaseModule):
    name = "enum4linux"
    aliases = ["enum4linux", "smb-enum"]
    description = "SMB enumeration with enum4linux"
    supported_targets = ["ip", "hostname"]

    actions = {
        "enum": "-a",   # full enumeration
        "shares": "-S", # list shares
        "users": "-U",  # list users
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for enum4linux based on intent.
        """
        if intent.action == "shares":
            args = ["enum4linux", "-S", intent.target]
        elif intent.action == "users":
            args = ["enum4linux", "-U", intent.target]
        else:  # default full enumeration
            args = ["enum4linux", "-a", intent.target]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("enum4linux", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
