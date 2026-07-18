import subprocess

class SmbclientModule:
    NAME = "smbclient"
    DESCRIPTION = "SMB share access and enumeration"
    CATEGORY = "Enumeration"
    RISK = "Medium"
    REQUIRES = ["smbclient"]

    DEFAULT_ACTION = "list"

    ACTIONS = {
        "list": {
            "description": "List available SMB shares (anonymous by default)",
            "command": ["smbclient", "-L", "{target}", "-N"]
        },
        "connect": {
            "description": "Connect to a specific share (anonymous by default)",
            "command": ["smbclient", "//{target}/{share}", "-N"]
        },
        "auth-list": {
            "description": "List shares with credentials",
            "command": ["smbclient", "-L", "{target}", "-U", "{username}%{password}"]
        },
        "auth-connect": {
            "description": "Connect to a share with credentials",
            "command": ["smbclient", "//{target}/{share}", "-U", "{username}%{password}"]
        }
    }

    aliases = ["smbclient"]

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
    def build(cls, action, target, **kwargs):
        if action not in cls.ACTIONS:
            raise ValueError(f"Unsupported action: {action}")
        cmd_template = cls.ACTIONS[action]["command"]
        cmd = []
        for arg in cmd_template:
            if arg.startswith("{") and arg.endswith("}"):
                key = arg.strip("{}")
                value = kwargs.get(key, target if key == "target" else None)
                if not value:
                    raise ValueError(f"Missing required argument '{key}' for {cls.NAME}")
                cmd.append(value)
            else:
                cmd.append(arg)
        return cmd

    @classmethod
    def analyze(cls, result):
        if "Sharename" in result.stdout or "Disk" in result.stdout:
            return "Shares discovered via smbclient."
        if "NT_STATUS_LOGON_FAILURE" in result.stderr:
            return "Authentication failed — invalid credentials."
        return None
