from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class FfufModule(BaseModule):
    name = "ffuf"
    aliases = ["ffuf", "fuzz"]
    description = "Fast web fuzzer for directories, parameters, and vhosts"
    supported_targets = ["url", "hostname"]

    actions = {
        "dir": "directory fuzzing",
        "param": "parameter fuzzing",
        "vhost": "virtual host fuzzing",
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for ffuf based on intent.
        """
        if intent.action == "dir":
            args = [
                "ffuf",
                "-u", f"http://{intent.target}/FUZZ",
                "-w", "/usr/share/wordlists/dirb/common.txt"
            ]
        elif intent.action == "param":
            args = [
                "ffuf",
                "-u", f"http://{intent.target}/?FUZZ=test",
                "-w", "/usr/share/wordlists/seclists/Fuzzing/parameters.txt"
            ]
        elif intent.action == "vhost":
            args = [
                "ffuf",
                "-u", f"http://{intent.target}",
                "-H", "Host: FUZZ",
                "-w", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"
            ]
        else:
            args = ["ffuf", "-u", f"http://{intent.target}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("ffuf", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
