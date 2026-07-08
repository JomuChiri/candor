# candor/modules/whois/__init__.py

class WhoisModule:
    NAME = "whois"
    DESCRIPTION = "Domain registration lookup"
    CATEGORY = "Recon"
    RISK = "Low"
    REQUIRES = ["whois"]

    ACTIONS = {
        "lookup": {
            "description": "Retrieve domain registration details",
            "command": "whois {target}"
        }
    }

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
        # Build a plan object or dict for execution
        return {
            "tool": cls.NAME,
            "action": intent.action,
            "target": intent.target,
            "command": ["whois", intent.target]
        }

    @classmethod
    def execute(cls, plan):
        import subprocess
        result = subprocess.run(plan["command"], capture_output=True, text=True)
        return type("Result", (), {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "status": "success" if result.returncode == 0 else "error"
        })()
