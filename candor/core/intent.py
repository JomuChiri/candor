from dataclasses import dataclass, field
from typing import Optional

from candor.core.errors import IntentParseError
from candor.modules.registry import MODULES

import shlex


@dataclass
class Intent:
    tool: str
    action: str
    target: Optional[str] = None
    parameters: dict[str, str] = field(default_factory=dict)


def parse_intent(query: str) -> Intent:
    """
    Convert user input into an Intent.

    Examples
    --------
    nmap scan 10.0.0.5

    bloodhound collect \
        --username admin \
        --password Pass123 \
        --domain corp.local \
        --dc dc01.corp.local
    """

    parts = shlex.split(query)

    if not parts:
        raise IntentParseError("Empty query.")

    #
    # Resolve tool
    #
    tool_token = parts[0].lower()

    tool = None
    module = None

    for name, mod in MODULES.items():
        aliases = getattr(mod, "aliases", [])

        if tool_token == name or tool_token in aliases:
            tool = name
            module = mod
            break

    if not module:
        raise IntentParseError(f"Unknown tool '{tool_token}'.")

    #
    # Module metadata
    #
    meta = module.metadata()

    actions = meta["actions"]
    default_action = meta["default_action"]

    #
    # Resolve action
    #
    if len(parts) >= 2:

        action_token = parts[1].lower()

        if action_token not in actions:

            available = "\n".join(f"  • {a}" for a in actions)

            raise IntentParseError(
                f"Unknown action '{action_token}' for {tool}.\n\n"
                f"Available actions:\n{available}"
            )

        action = action_token

    else:

        if not default_action:
            raise IntentParseError(f"{tool} has no default action.")

        action = default_action

    #
    # Remaining arguments
    #
    target = None
    parameters = {}

    i = 2

    while i < len(parts):

        token = parts[i]

        #
        # Named parameter
        #
        if token.startswith("--"):

            key = token[2:]

            if i + 1 >= len(parts):
                raise IntentParseError(f"Missing value for '--{key}'.")

            parameters[key] = parts[i + 1]
            i += 2
            continue

        #
        # Short flag
        #
        if token.startswith("-"):

            key = token[1:]

            if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                parameters[key] = parts[i + 1]
                i += 2
            else:
                parameters[key] = True
                i += 1

            continue

        #
        # Positional target
        #
        if target is None:
            target = token
        else:
            raise IntentParseError(f"Unexpected argument '{token}'.")

        i += 1

    return Intent(
        tool=tool,
        action=action,
        target=target,
        parameters=parameters,
    )