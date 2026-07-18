import subprocess

class NetExecModule:
    NAME = "netexec"
    DESCRIPTION = "Network exploitation and enumeration tool"
    CATEGORY = "Enumeration"
    RISK = "High"
    REQUIRES = ["nxc"]

    DEFAULT_ACTION = "smb-enum"

    ACTIONS = {
        "smb-enum": {
            "description": "Enumerate SMB shares",
            "command": [
                "nxc", "smb", "{target}", "-u", "{username}", "-p", "{password}"
            ]
        },
        "smb-auth": {
            "description": "Test SMB authentication",
            "command": [
                "nxc", "smb", "{target}", "-u", "{username}", "-p", "{password}"
            ]
        },
        "ldap-enum": {
            "description": "Enumerate LDAP",
            "command": [
                "nxc", "ldap", "{target}", "-u", "{username}", "-p", "{password}"
            ]
        },
        "winrm-auth": {
            "description": "Test WinRM authentication",
            "command": [
                "nxc", "winrm", "{target}", "-u", "{username}", "-p", "{password}"
            ]
        }
    }

    aliases = ["netexec", "nxc"]

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
