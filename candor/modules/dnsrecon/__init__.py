import subprocess

class DnsreconModule:
    NAME = "dnsrecon"
    DESCRIPTION = "DNS enumeration and brute forcing"
    CATEGORY = "DNS"
    RISK = "Medium"
    REQUIRES = ["dnsrecon"]

    DEFAULT_ACTION = "basic"

    ACTIONS = {
        "basic": {
            "description": "Basic DNS enumeration",
            "command": ["dnsrecon", "-d", "{target}"]
        },
        "brute": {
            "description": "Brute force subdomains",
            "command": [
                "dnsrecon", "-d", "{target}",
                "-D", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
                "-t", "brt"
            ]
        },
        "axfr": {
            "description": "Attempt zone transfer",
            "command": ["dnsrecon", "-d", "{target}", "-t", "axfr"]
        }
    }

    aliases = ["dnsrecon"]

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
        if action not in cls.ACTIONS:
            raise ValueError(f"Unknown action '{action}' for {cls.NAME}")
        cmd_template = cls.ACTIONS[action]["command"]
        return [arg.replace("{target}", target) for arg in cmd_template]

    @classmethod
    def analyze(cls, result):
        if "A" in result.stdout or "MX" in result.stdout:
            return "DNS records discovered — potential attack surface."
        return None
