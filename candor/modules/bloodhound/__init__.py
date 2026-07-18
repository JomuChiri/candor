import subprocess


class BloodhoundModule:

    NAME = "bloodhound"
    DESCRIPTION = "Active Directory graph analysis"

    CATEGORY = "Active Directory"

    RISK = "High"

    REQUIRES = [
        "bloodhound-python",
        "bloodhound"
    ]

    DEFAULT_ACTION = "collect"

    ACTIONS = {

        "collect": {
            "description": "Collect Active Directory information",
            "command": [
                "bloodhound-python",
                "-u", "{username}",
                "-p", "{password}",
                "-d", "{domain}",
                "-dc", "{dc}",
                "-c", "All",
            ],
        },

        "analyze": {
            "description": "Open or analyze collected data",
            "command": [
                "bloodhound",
                "--analyze",
                "{dataset}",
            ],
        },
    }

    REQUIRED_PARAMETERS = {

        "collect": [
            "username",
            "password",
            "domain",
            "dc",
        ],

        "analyze": [
            "dataset",
        ],
    }

    aliases = [
        "bloodhound",
        "ad-graph",
    ]

    @classmethod
    def metadata(cls):
        return {
            "name": cls.NAME,
            "description": cls.DESCRIPTION,
            "category": cls.CATEGORY,
            "risk": cls.RISK,
            "requires": cls.REQUIRES,
            "default_action": cls.DEFAULT_ACTION,
            "actions": cls.ACTIONS,
        }

    @classmethod
    def build(cls, intent):

        required = cls.REQUIRED_PARAMETERS.get(intent.action, [])

        missing = [
            p
            for p in required
            if p not in intent.parameters
        ]

        if missing:

            raise ValueError(
                "Missing required parameters:\n"
                + "\n".join(f"  --{m}" for m in missing)
            )

        template = cls.ACTIONS[intent.action]["command"]

        command = []

        for item in template:

            if item.startswith("{") and item.endswith("}"):

                key = item[1:-1]
                command.append(intent.parameters[key])

            else:

                command.append(item)

        return command

    @classmethod
    def execute(cls, command):

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return type(
            "Result",
            (),
            {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "status": (
                    "success"
                    if result.returncode == 0
                    else "error"
                ),
            },
        )()

    @classmethod
    def analyze(cls, result):

        findings = []

        if "Domain Admins" in result.stdout:
            findings.append(
                "Domain Admins group identified."
            )

        if "High Value" in result.stdout:
            findings.append(
                "High-value targets identified."
            )

        return findings