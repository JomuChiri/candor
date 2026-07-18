from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class RpcclientModule(BaseModule):
    name = "rpcclient"
    aliases = ["rpcclient", "rpc"]
    description = "RPC enumeration of users, groups, and policies"
    supported_targets = ["ip", "hostname"]

    actions = {
        "enum-users": "Enumerate users",
        "enum-groups": "Enumerate groups",
        "enum-domains": "Enumerate domains",
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for rpcclient based on intent.
        """
        if intent.action == "enum-users":
            args = ["rpcclient", "-U", "", intent.target, "-c", "enumdomusers"]
        elif intent.action == "enum-groups":
            args = ["rpcclient", "-U", "", intent.target, "-c", "enumdomgroups"]
        elif intent.action == "enum-domains":
            args = ["rpcclient", "-U", "", intent.target, "-c", "enumdomains"]
        else:
            args = ["rpcclient", "-U", "", intent.target, "-c", "enumdomusers"]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("rpcclient", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
