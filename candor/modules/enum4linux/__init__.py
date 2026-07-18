import subprocess

class Enum4linuxModule:
    NAME = "enum4linux"
    DESCRIPTION = "SMB enumeration tool"
    CATEGORY = "Enumeration"
    RISK = "Medium"
    REQUIRES = ["enum4linux"]

     # Explicit default action
    DEFAULT_ACTION = "basic"   

    ACTIONS = {
         "basic": {
            "description": "Run basic enumeration",
            "command": ["enum4linux", "-U", "-S", "-G", "-P", "-r", "{target}"]
        },
        "users": {
            "description": "Enumerate users",
            "command": ["enum4linux", "-U", "{target}"]
        },
        "shares": {
            "description": "Enumerate shares",
            "command": ["enum4linux", "-S", "{target}"]
        },
        "groups": {
            "description": "Enumerate groups",
            "command": ["enum4linux", "-G", "{target}"]
        },
        "passwords": {
            "description": "Password policy enumeration",
            "command": ["enum4linux", "-P", "{target}"]
        },
        "enum": {
            "description": "Full SMB enumeration",
            "command": ["enum4linux", "-a", "{target}"]
        },
        # Alias for convenience
        "scan": {
            "description": "Alias for full enumeration",
            "command": ["enum4linux", "-a", "{target}"]
        }
    }

    aliases = ["enum4linux"]

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
    def build(cls, intent):
        if intent.action not in cls.ACTIONS:
            raise ValueError(f"Unknown action '{intent.action}' for {cls.NAME}")
        cmd_template = cls.ACTIONS[intent.action]["command"]
        cmd = []
        for arg in cmd_template:
            if arg.startswith("{") and arg.endswith("}"):
                key = arg.strip("{}")
                value = intent.get(key)
                if not value:
                    raise ValueError(f"Missing required argument '{key}' for {cls.NAME}")
                cmd.append(value)
            else:
                cmd.append(arg)
        return cmd

    @classmethod
    def analyze(cls, result):
        if "Got domain/workgroup name" in result.stdout:
            return "Enum4linux successfully enumerated domain/workgroup."
        if "Sharename" in result.stdout:
            return "Enum4linux discovered SMB shares."
        if "NT_STATUS_LOGON_FAILURE" in result.stderr:
            return "Authentication failed — invalid credentials."
        return None