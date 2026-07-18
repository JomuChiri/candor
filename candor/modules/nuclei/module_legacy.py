from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class NucleiModule(BaseModule):
    name = "nuclei"
    aliases = ["nuclei", "cve-scan"]
    description = "Template-based vulnerability scanning with Nuclei"
    supported_targets = ["ip", "hostname", "url"]

    actions = {
        "scan": "-u",   # basic scan against a URL/host
        "tags": "-tags", # run specific template tags
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for Nuclei based on intent.
        """
        if intent.action == "scan":
            args = ["nuclei", "-u", intent.target]
        elif intent.action == "tags":
            # Example: nuclei -u target -tags cve
            args = ["nuclei", "-u", intent.target, "-tags", "cve"]
        else:
            args = ["nuclei", "-u", intent.target]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("nuclei", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
