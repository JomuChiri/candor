# candor/parser/intent.py
from candor.modules import registry
from candor.core.intent import Intent
from candor.core.validate import validate_target
from candor.parser.natural_map import NATURAL_MAP
from dataclasses import dataclass

@dataclass
class Intent:
    tool: str
    action: str
    target: str
    candidates: list = None
    confidence: float = 1.0   # default high confidence

DEFAULT_ACTIONS = {
    "nmap": "port_scan",
    "whois": "lookup",
    # add defaults for other tools here
}

def parse_intent(query: str) -> Intent:
    words = query.strip().split()
    if not words:
        return None

    command, *args = words
    action = None

    # First check aliases
    for module in registry.MODULES.values():
        if command in module.aliases:
            if command in module.actions:
                action = command
            elif args and args[0] in module.actions:
                action = args[0]
                args = args[1:]

            target = args[0] if args else None
            if target and not validate_target(target):
                raise ValueError(f"Invalid target: {target}")

            # Apply default if action is still None
            if not action:
                action = DEFAULT_ACTIONS.get(module.name)

            return Intent(tool=module.name, action=action, target=target)

    # If no alias matched, try natural language mapping
    for phrase, mapped_action in NATURAL_MAP.items():
        if phrase in query.lower():
            for module in registry.MODULES.values():
                if mapped_action in module.actions:
                    target = words[-1] if validate_target(words[-1]) else None
                    return Intent(tool=module.name, action=mapped_action, target=target)

    # Apply default if action is still None
    if not action:
    	action = DEFAULT_ACTIONS.get(module.name)

    return None
