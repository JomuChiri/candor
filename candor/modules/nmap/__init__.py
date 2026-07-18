class NmapModule:
    NAME = "nmap"
    DESCRIPTION = "Network discovery and port scanning"
    CATEGORY = "Scanning"
    RISK = "Medium"
    REQUIRES = ["nmap"]

    DEFAULT_ACTION = "scan"

    ACTIONS = {
        "scan": {
            "description": "Basic port scan",
            "command": ["nmap", "{target}"]
        },
        "scan-service": {
            "description": "Service/version detection",
            "command": ["nmap", "-sV", "{target}"]
        },
        "scan-os": {
            "description": "OS detection",
            "command": ["nmap", "-O", "{target}"]
        },
        "scan-all": {
            "description": "Aggressive full scan",
            "command": ["nmap", "-A", "{target}"]
        }
    }

    aliases = ["nmap"]

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
            raise ValueError(f"Unknown action '{action}' for {cls.NAME}")
        cmd_template = cls.ACTIONS[action]["command"]
        return [arg.replace("{target}", target) for arg in cmd_template]

    # Optional analysis hook
    @classmethod
    def analyze(cls, result):
        if "open" in result.stdout:
            return "Open ports detected — potential attack surface."
        return None
