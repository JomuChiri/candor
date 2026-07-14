# candor/commands/help.py
from candor.modules import registry

def matches(query: str) -> bool:
    return query.lower().startswith("help")

def handle(query: str, console):
    _, *args = query.split()
    if not args:
        console.print("[bold magenta]Available modules by category:[/]")
        categories = registry.list_by_category()
        for cat, mods in categories.items():
            console.print(f"\n[bold cyan]{cat}[/]")
            for meta in mods:
                console.print(f" - {meta['name']}: {meta['description']} (Risk: {meta['risk']})")
    else:
        module = registry.get(args[0])
        if module:
            console.print(module.help())
        else:
            console.print(f"[bold red]No such module: {args[0]}[/]")
