from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class NetexecModule(BaseModule):
    name = "netexec"
    aliases = ["netexec", "cme"]
    description = "Active Directory and SMB enumeration with NetExec"
    supported_targets = ["ip", "hostname"]

    actions = {
        "smb-enum": "Enumerate SMB shares and users",
        "smb-auth": "Test SMB authentication",
        "ldap-enum": "Enumerate LDAP information",
        "winrm-auth": "Test WinRM authentication",
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for NetExec based on intent.
        """
        if intent.action == "smb-enum":
            args = ["netexec", "smb", intent.target, "--shares", "--users"]
        elif intent.action == "smb-auth":
            args = ["netexec", "smb", intent.target, "-u", "user", "-p", "password"]
        elif intent.action == "ldap-enum":
            args = ["netexec", "ldap", intent.target, "--users", "--groups"]
        elif intent.action == "winrm-auth":
            args = ["netexec", "winrm", intent.target, "-u", "user", "-p", "password"]
        else:
            args = ["netexec", "smb", intent.target]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("netexec", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
