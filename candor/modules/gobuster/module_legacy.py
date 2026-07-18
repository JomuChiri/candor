from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class GobusterModule(BaseModule):
    name = "gobuster"
    aliases = ["gobuster", "dirbust"]
    description = "Directory and DNS brute forcing with Gobuster"
    supported_targets = ["ip", "hostname", "url"]

    actions = {
        "dir": "dir",   # directory brute force
        "dns": "dns",   # DNS subdomain brute force
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for Gobuster based on intent.
        """
        if intent.action == "dir":
            args = [
                "gobuster", "dir",
                "-u", f"http://{intent.target}",
                "-w", "/usr/share/wordlists/dirb/common.txt"
            ]
        elif intent.action == "dns":
            args = [
                "gobuster", "dns",
                "-d", intent.target,
                "-w", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
            ]
        else:
            args = ["gobuster", "dir", "-u", f"http://{intent.target}", "-w", "/usr/share/wordlists/dirb/common.txt"]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("gobuster", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
