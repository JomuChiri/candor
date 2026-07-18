import subprocess

class NiktoModule:
    NAME = "nikto"
    DESCRIPTION = "Web vulnerability scanner"
    CATEGORY = "Web"
    RISK = "High"
    REQUIRES = ["nikto"]

    DEFAULT_ACTION = "scan"

    ACTIONS = {
        "scan": {
            "description": "Run a vulnerability scan against a target URL",
            "command": ["nikto", "-h", "{target}"]
        }
    }

    aliases = ["nikto"]

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

    # Optional analysis hook
    @classmethod
    def analyze(cls, result):
        if "OSVDB" in result.stdout or "vulnerabilities" in result.stdout.lower():
            return "Potential vulnerabilities detected by Nikto."
        return None

