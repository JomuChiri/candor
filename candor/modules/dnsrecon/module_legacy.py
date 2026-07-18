from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class DnsreconModule(BaseModule):
    name = "dnsrecon"
    aliases = ["dnsrecon", "dns-enum"]
    description = "DNS enumeration and brute forcing with dnsrecon"
    supported_targets = ["hostname", "domain"]

    actions = {
        "basic": "-d",   # basic enumeration
        "brute": "-d",   # brute force with wordlist
        "axfr": "-d",    # zone transfer attempt
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for dnsrecon based on intent.
        """
        if intent.action == "brute":
            args = [
                "dnsrecon", "-d", intent.target,
                "-D", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
                "-t", "brt"
            ]
        elif intent.action == "axfr":
            args = ["dnsrecon", "-d", intent.target, "-t", "axfr"]
        else:  # default basic
            args = ["dnsrecon", "-d", intent.target]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("dnsrecon", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
