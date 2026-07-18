import subprocess

class RpcclientModule:
    NAME = "rpcclient"
    DESCRIPTION = "SMB RPC enumeration tool"
    CATEGORY = "Enumeration"
    RISK = "Medium"
    REQUIRES = ["rpcclient"]

    DEFAULT_ACTION = "enum-users"

    ACTIONS = {
        "enum-users": {
            "description": "Enumerate users via RPC",
            "command": [
                "rpcclient",
                "-U", "{username}%{password}",
                "{target}"
            ]
        },
        "enum-domains": {
            "description": "Enumerate domains via RPC",
            "command": [
                "rpcclient",
                "-U", "{username}%{password}",
                "{target}"
            ]
        }
    }

    aliases = ["rpcclient"]

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
