import subprocess

class SearchsploitModule:
    NAME = "searchsploit"
    DESCRIPTION = "Exploit database search utility"
    CATEGORY = "Exploitation"
    RISK = "High"
    REQUIRES = ["searchsploit"]

    DEFAULT_ACTION = "lookup"

    ACTIONS = {
        "lookup": {
            "description": "Search ExploitDB for a given service/version",
            "command": ["searchsploit", "{target}"]
        }
    }

    aliases = ["searchsploit"]

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
    def analyze(cls, result):
        """Optional analysis hook to highlight findings."""
        if "Exploit:" in result.stdout or "EDB-ID:" in result.stdout:
            return "Searchsploit found potential exploits in ExploitDB."
        return None
