from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class SmbclientModule(BaseModule):
    name = "smbclient"
    aliases = ["smbclient", "smb"]
    description = "SMB share access and enumeration with smbclient"
    supported_targets = ["ip", "hostname"]

    actions = {
        "list": "List available shares",
        "connect": "Connect to a specific share",
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for smbclient based on intent.
        """
        if intent.action == "list":
            args = ["smbclient", "-L", intent.target, "-N"]
        elif intent.action == "connect":
            # Example: smbclient //target/share -N
            args = ["smbclient", f"//{intent.target}/share", "-N"]
        else:
            args = ["smbclient", "-L", intent.target, "-N"]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("smbclient", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
