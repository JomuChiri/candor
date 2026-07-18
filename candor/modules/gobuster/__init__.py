import subprocess

class GobusterModule:
    NAME = "gobuster"
    DESCRIPTION = "Web directory and DNS brute forcing"
    CATEGORY = "Enumeration"
    RISK = "Medium"
    REQUIRES = ["gobuster"]

    # Explicit default action
    DEFAULT_ACTION = "dir"    

    ACTIONS = {
        "dir": {
            "description": "Directory brute force",
            "command": ["gobuster", "dir", "-u", "http://{target}", "-w", "/usr/share/wordlists/dirb/common.txt"]
        },
        "dns": {
            "description": "DNS subdomain brute force",
            "command": ["gobuster", "dns", "-d", "{target}", "-w", "/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt"]
        },
        "vhost": {
            "description": "Virtual host brute force",
            "command": ["gobuster", "vhost", "-u", "http://{target}", "-w", "/usr/share/wordlists/seclists/Discovery/DNS/namelist.txt"]
        }
    }

    aliases = ["gobuster"]

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

    # Optional: analysis hook
    @classmethod
    def analyze(cls, result):
        if "Status: 200" in result.stdout:
            return "Potentially interesting directories found."
        return None