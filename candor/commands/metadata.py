# candor/commands/metadata.py
import json
from candor.modules import registry

def matches(query: str) -> bool:
    return query.lower().startswith("metadata")

def handle(query: str, console):
    _, *args = query.split()
    if not args:
        console.print("[bold magenta]Available modules:[/]")
        for module in registry.MODULES.values():
            console.print(f" - {module.name}")
    else:
        module = registry.get(args[0])
        if module:
            console.print(json.dumps(module.metadata(), indent=2))
        else:
            console.print(f"[bold red]No such module: {args[0]}[/]")
