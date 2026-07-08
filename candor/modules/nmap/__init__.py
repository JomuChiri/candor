# candor/modules/nmap/__init__.py
import subprocess

class NmapModule:
    NAME = "nmap"
    DESCRIPTION = "Network mapper for port and service discovery"
    CATEGORY = "Discovery"
    RISK = "Medium"
    REQUIRES = ["nmap"]

    ACTIONS = {
        "scan-fast": {
            "description": "Quick scan of common ports",
            "command": ["nmap", "-F", "{target}"]
        },
        "scan-service": {
            "description": "Service/version detection",
            "command": ["nmap", "-sV", "{target}"]
        },
        "scan-os": {
            "description": "OS detection",
            "command": ["nmap", "-O", "{target}"]
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
            "actions": cls.ACTIONS
        }

    @classmethod
    def help(cls):
        lines = [f"{cls.NAME} — {cls.DESCRIPTION}"]
        for action, info in cls.ACTIONS.items():
            lines.append(f"  {action}: {info['description']}")
        return "\n".join(lines)

    @classmethod
    def build(cls, intent):
        action = intent.action
        if action not in cls.ACTIONS:
            raise ValueError(f"Unsupported action: {action}")
        cmd_template = cls.ACTIONS[action]["command"]
        cmd = [c.format(target=intent.target) for c in cmd_template]
        return {
            "tool": cls.NAME,
            "action": action,
            "target": intent.target,
            "command": cmd
        }

    @classmethod
    def execute(cls, plan):
        result = subprocess.run(plan["command"], capture_output=True, text=True)
        return type("Result", (), {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "success" if result.returncode == 0 else "error"
        })()

