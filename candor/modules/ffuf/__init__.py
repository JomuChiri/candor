import subprocess

class FfufModule:
    NAME = "ffuf"
    DESCRIPTION = "Fast web fuzzer"
    CATEGORY = "Web"
    RISK = "Medium"
    REQUIRES = ["ffuf"]

    # Explicit default action
    DEFAULT_ACTION = "dir"

    ACTIONS = {
        "dir": {
            "description": "Directory fuzzing",
            "command": ["ffuf", "-u", "http://{target}/FUZZ", "-w", "/usr/share/wordlists/dirb/common.txt"]
        },
        "param": {
            "description": "Parameter fuzzing",
            "command": ["ffuf", "-u", "http://{target}/?FUZZ=test", "-w", "/usr/share/wordlists/seclists/Fuzzing/parameters.txt"]
        },
        "vhost": {
            "description": "Virtual host fuzzing",
            "command": ["ffuf", "-u", "http://{target}", "-H", "Host: FUZZ", "-w", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"]
        },
        "dns": {
            "description": "DNS subdomain brute force",
            "command": ["ffuf", "-u", "http://{target}", "-w", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt", "-H", "Host: FUZZ.{target}"]
        }
    }

    aliases = ["ffuf"]

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
        if "Status: 200" in result.stdout or "Found" in result.stdout:
            return "ffuf discovered accessible resources."
        return None