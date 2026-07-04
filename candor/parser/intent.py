# candor/parser/intent.py
from candor.modules import registry
from candor.core.intent import Intent
from candor.core.validate import validate_target
from candor.parser.natural_map import NATURAL_MAP

def parse_intent(query: str):
    words = query.strip().split()
    if not words:
        return None

    command, *args = words

    # First check aliases
    for module in registry.MODULES.values():
        if command in module.aliases:
            action = None
            if command in module.actions:
                action = command
            elif args and args[0] in module.actions:
                action = args[0]
                args = args[1:]

            target = args[0] if args else None
            if target and not validate_target(target):
                raise ValueError(f"Invalid target: {target}")

            return Intent(tool=module.name, action=action, target=target)

    # If no alias matched, try natural language mapping
    for phrase, action in NATURAL_MAP.items():
        if phrase in query.lower():
            # Find which module owns this action
            for module in registry.MODULES.values():
                if action in module.actions:
                    # Extract target (last word, if valid)
                    target = words[-1] if validate_target(words[-1]) else None
                    return Intent(tool=module.name, action=action, target=target)

    return None
