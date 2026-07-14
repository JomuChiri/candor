# candor/modules/nmap/module.py
from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class NmapModule(BaseModule):
    name = "nmap"
    aliases = ["scan", "nmap"]
    description = "Network scanning with Nmap"
    supported_targets = ["ip", "hostname"]

    # Advertised actions → Nmap flags
    actions = {
        "scan-fast": "-T4 -F",       # quick scan of common ports
        "scan-service": "-sV",       # service/version detection
        "scan-os": "-O",             # OS detection
        "scan-udp": "-sU",           # UDP scan
        "scan-script": "-sC",        # default script scan
        "scan-all": "-p- -A",        # full ports + aggressive
        "service_scan": "-sV",       # legacy alias
        "os_detection": "-O",        # legacy alias
        "ping_scan": "-sn",          # host discovery
        "null_scan": "-sN",          # stealth/null scan
        "port_scan": "-p-",          # full port range
    }

    def build(self, intent):
        """
        Build execution plan for Nmap based on intent.
        """
        if intent.action == "scan-fast":
            args = ["nmap", "-F", intent.target]
        elif intent.action == "scan-service":
            args = ["nmap", "-sV", intent.target]
        elif intent.action == "scan-os":
            args = ["nmap", "-O", intent.target]
        elif intent.action == "scan-udp":
            args = ["nmap", "-sU", intent.target]
        elif intent.action == "scan-script":
            args = ["nmap", "-sC", intent.target]
        else:
            args = ["nmap", intent.target]

        return Plan(
            tool="nmap",
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("nmap", {}).get("default_args", [])
        command = ["nmap"] + default_args + plan.command[1:]
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
