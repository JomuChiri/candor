# candor/commands/findings.py
from candor.core.findings import FindingsDB

def matches(query: str) -> bool:
    return query.lower().startswith("findings")

def handle(query: str, console):
    db = FindingsDB()
    console.print("\n[bold magenta]Findings Database[/]")
    for severity, items in db.list_findings().items():
        console.print(f"\n[bold cyan]{severity}[/]")
        for item in items:
            console.print(
                f"- {item['description']} "
                f"(Target: {item['target']}, Source: {item['source']}, MITRE: {item['mitre']})"
            )
