# candor/core/intent.py
from dataclasses import dataclass, field
from typing import Optional
import shlex

from candor.core.errors import IntentParseError
from candor.modules.registry import registry


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

    # --- Resolve tool via registry ---
    tool_token = parts[0].lower()
    try:
        module = registry.resolve(tool_token)
    except KeyError:
        raise IntentParseError(f"Unknown tool '{tool_token}'.")

    meta = module.metadata()
    actions = meta["actions"]
    default_action = meta.get("default_action")

    # --- Resolve action ---
    if len(parts) >= 2:
        action_token = parts[1].lower()
        if action_token not in actions:
            available = "\n".join(f"  • {a}" for a in actions)
            raise IntentParseError(
                f"Unknown action '{action_token}' for {tool_token}.\n\n"
                f"Available actions:\n{available}"
            )
        action = action_token
    else:
        if not default_action:
            raise IntentParseError(f"{tool_token} has no default action.")
        action = default_action

    # --- Remaining arguments ---
    target = None
    parameters = {}
    i = 2
    while i < len(parts):
        token = parts[i]

        if token.startswith("--"):
            key = token[2:]
            if i + 1 >= len(parts):
                raise IntentParseError(f"Missing value for '--{key}'.")
            parameters[key] = parts[i + 1]
            i += 2
            continue

        if token.startswith("-"):
            key = token[1:]
            if i + 1 < len(parts) and not parts[i + 1].startswith("-"):
                parameters[key] = parts[i + 1]
                i += 2
            else:
                parameters[key] = True
                i += 1
            continue

        if target is None:
            target = token
        else:
            raise IntentParseError(f"Unexpected argument '{token}'.")
        i += 1

    module = registry.resolve(tool_token)
    
    return Intent(
        tool=module.name,
        action=action,
        target=target,
        parameters=parameters,
    )
