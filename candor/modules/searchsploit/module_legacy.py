from candor.modules.base import BaseModule
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult
from candor.shell.execute import run_command
from candor.config import load_config

class SearchsploitModule(BaseModule):
    name = "searchsploit"
    aliases = ["searchsploit", "exploitdb"]
    description = "Exploit database lookup with Searchsploit"
    supported_targets = ["service", "software", "version"]

    actions = {
        "lookup": "search",   # basic search
    }

    def build(self, intent: Intent) -> Plan:
        """
        Build execution plan for Searchsploit based on intent.
        """
        args = ["searchsploit", intent.target]

        return Plan(
            tool=self.name,
            action=intent.action,
            target=intent.target,
            command=args
        )

    def execute(self, plan: Plan) -> ExecutionResult:
        config = load_config()
        default_args = config.get("searchsploit", {}).get("default_args", [])
        command = plan.command + default_args
        return run_command(command)

    def self_test(self) -> dict:
        from candor.doctor import check_tool
        return check_tool(self.name)
