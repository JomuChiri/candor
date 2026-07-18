from candor.modules.base import BaseModule
from .summary import summarize_enum4linux


class Enum4linuxModule(BaseModule):
    """
    Enum4linux SMB enumeration module.
    """

    name = "enum4linux"
    category = "SMB Enumeration"

    description = (
        "Enumerate SMB shares, users, groups, "
        "password policy and domain information."
    )

    aliases = [
        "enum4linux",
    ]

    actions = {
        "basic": "Basic enumeration",
        "users": "Enumerate users",
        "shares": "Enumerate shares",
        "groups": "Enumerate groups",
        "passwords": "Enumerate password policy",
        "enum": "Full enumeration",
        "scan": "Alias for full enumeration",
    }

    supported_targets = [
        "host",
    ]

    summarizer = summarize_enum4linux

    def build(self, intent):

        target = intent.target

        commands = {

            "basic": [
                "enum4linux",
                "-U",
                "-S",
                "-G",
                "-P",
                "-r",
                target,
            ],

            "users": [
                "enum4linux",
                "-U",
                target,
            ],

            "shares": [
                "enum4linux",
                "-S",
                target,
            ],

            "groups": [
                "enum4linux",
                "-G",
                target,
            ],

            "passwords": [
                "enum4linux",
                "-P",
                target,
            ],

            "enum": [
                "enum4linux",
                "-a",
                target,
            ],

            "scan": [
                "enum4linux",
                "-a",
                target,
            ],
        }

        try:
            return commands[intent.action]

        except KeyError:
            raise ValueError(
                f"Unsupported action '{intent.action}' "
                f"for {self.name}"
            )