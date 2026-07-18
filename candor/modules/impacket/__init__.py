import subprocess

class ImpacketModule:
    NAME = "impacket"
    DESCRIPTION = "SMB/RPC/LDAP exploitation toolkit"
    CATEGORY = "Exploitation"
    RISK = "High"
    REQUIRES = ["impacket"]

    DEFAULT_ACTION = "smbexec"

    ACTIONS = {
        "smbexec": {
            "description": "Execute commands via SMB",
            "command": [
                "smbexec.py",
                "{domain}/{username}:{password}@{target}"
            ]
        },
        "psexec": {
            "description": "Execute commands via PsExec",
            "command": [
                "psexec.py",
                "{domain}/{username}:{password}@{target}"
            ]
        },
        "wmiexec": {
            "description": "Execute commands via WMI",
            "command": [
                "wmiexec.py",
                "{domain}/{username}:{password}@{target}"
            ]
        },
        "secretsdump": {
            "description": "Dump secrets from target",
            "command": [
                "secretsdump.py",
                "{domain}/{username}:{password}@{target}"
            ]
        }
    }

    aliases = ["impacket"]

    @classmethod
    def build(cls, intent):
        """Build command using intent.arguments instead of a single target."""
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
        if "Dumped" in result.stdout or "NTLM" in result.stdout:
            return "Impacket successfully executed or dumped secrets."
        if "STATUS_LOGON_FAILURE" in result.stderr:
            return "Authentication failed — check credentials."
        return None
