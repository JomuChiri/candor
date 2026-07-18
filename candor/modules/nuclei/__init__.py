import subprocess

class NucleiModule:
    NAME = "nuclei"
    DESCRIPTION = "Template-based vulnerability scanner"
    CATEGORY = "Web"
    RISK = "High"
    REQUIRES = ["nuclei"]

    DEFAULT_ACTION = "scan"

    ACTIONS = {
        "scan": {
            "description": "Run default Nuclei templates",
            "command": ["nuclei", "-u", "{target}"]
        },
        "tags": {
            "description": "Run templates by tag (e.g. CVE)",
            "command": ["nuclei", "-u", "{target}", "-tags", "cve"]
        }
    }

    aliases = ["nuclei"]

    @classmethod
    def metadata(cls):
        return {
            "name": cls.NAME,
            "description": cls.DESCRIPTION,
            "category": cls.CATEGORY,
            "risk": cls.RISK,
            "requires": cls.REQUIRES,
            "default_action": cls.DEFAULT_ACTION,
            "actions": cls.ACTIONS
        }

    @classmethod
    def help(cls):
        lines = [f"{cls.NAME} — {cls.DESCRIPTION}"]
        lines.append(f"Default action: {cls.DEFAULT_ACTION}")
        for action, info in cls.ACTIONS.items():
            lines.append(f"  {action}: {info['description']}")
        return "\n".join(lines)

    @classmethod
    def build(cls, action, target):
        """Return the command list for the given action and target."""
        if action not in cls.ACTIONS:
            raise ValueError(f"Unsupported action: {action}")
        cmd_template = cls.ACTIONS[action]["command"]
        return [c.replace("{target}", target) for c in cmd_template]

    @classmethod
    def execute(cls, plan):
        result = subprocess.run(plan, capture_output=True, text=True)
        return type("Result", (), {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "success" if result.returncode == 0 else "error"
        })()

    @classmethod
    def analyze(cls, result):
        """Optional analysis hook to highlight findings."""
        if "CVE-" in result.stdout:
            return "Nuclei detected vulnerabilities tagged with CVE identifiers."
        return None
