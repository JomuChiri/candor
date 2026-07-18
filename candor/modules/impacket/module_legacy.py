from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class ImpacketModule(BaseModule):
    name = "impacket"
    aliases = ["impacket", "smbexec", "psexec", "wmiexec"]
    description = "SMB/RPC/LDAP exploitation and interaction with Impacket"
    supported_targets = ["ip", "hostname"]

    actions = {
        "smbexec": "Execute commands via SMB",
        "psexec": "Execute commands via PsExec",
        "wmiexec": "Execute commands via WMI",
        "secretsdump": "Dump secrets from target",
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for Impacket based on intent.
        """
        if intent.action == "smbexec":
            args = ["impacket-smbexec", f"{intent.target}", "user:password"]
        elif intent.action == "psexec":
            args = ["impacket-psexec", f"{intent.target}", "user:password"]
        elif intent.action == "wmiexec":
            args = ["impacket-wmiexec", f"{intent.target}", "user:password"]
        elif intent.action == "secretsdump":
            args = ["impacket-secretsdump", f"{intent.target}", "user:password"]
        else:
            args = ["impacket-smbexec", f"{intent.target}", "user:password"]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("impacket", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
