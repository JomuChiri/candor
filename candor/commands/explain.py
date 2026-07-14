# candor/commands/explain.py
from candor.explain import explain

def matches(query: str) -> bool:
    return query.lower().startswith("explain")

def handle(query: str, console):
    _, *args = query.split()
    if not args:
        console.print("[bold red]Usage: explain <action>[/]")
        return
    console.print(explain(args[0]))
