# candor/commands/case.py
from candor.core.case import Case

def matches(query: str) -> bool:
    return query.lower().startswith("case")

def handle(query: str, console, current_investigation=None):
    _, action, *args = query.split()

    if action == "create":
        if not args:
            console.print("[bold red]Usage: case create <case_name>[/]")
            return
        case = Case(args[0])
        console.print(f"[bold green]Case created:[/] {args[0]}")

    elif action == "add":
        if not args:
            console.print("[bold red]Usage: case add <case_name>[/]")
            return
        if not current_investigation:
            console.print("[bold red]No active investigation to add.[/]")
            return
        case = Case(args[0])
        case.add_investigation(current_investigation.target)
        console.print(
            f"[bold green]Investigation {current_investigation.target} added to case {args[0]}[/]"
        )

    elif action == "list":
        if not args:
            console.print("[bold red]Usage: case list <case_name>[/]")
            return
        case = Case(args[0])
        console.print(f"\n[bold magenta]Case {args[0]} Investigations[/]")
        for inv in case.list_investigations():
            console.print(f"- {inv}")

    else:
        console.print(f"[bold red]Unknown case action:[/] {action}")
