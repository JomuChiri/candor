# candor/modules/whois/__init__.py
import subprocess
from candor.modules.base import BaseModule
from .summary import summarize_whois


class WhoisModule(BaseModule):
    name = "whois"
    description = "Domain registration lookup"
    aliases = ["whois"]
    actions = {"lookup": "Retrieve domain registration details"}
    supported_targets = ["domain"]
    summarizer = summarize_whois  # default analyze() will call this

    def build(self, intent):
        """
        Build the command list for the given intent.
        """
        if intent.action not in self.actions:
            raise ValueError(f"Unsupported action: {intent.action}")
        return ["whois", intent.target]

    def execute(self, plan):
        """
        Execute the plan using subprocess and return a Result object.
        """
        result = subprocess.run(plan, capture_output=True, text=True)
        return type("Result", (), {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "success" if result.returncode == 0 else "error"
        })()

    # Optional: override analyze if you want richer AnalysisResult
    # Otherwise BaseModule.analyze() will call summarize_whois()
    # def analyze(self, result):
    #     return super().analyze(result)
