# candor/commands/report.py
from candor.reporting import generate_investigation_report, generate_case_report

def matches(query: str) -> bool:
    return query.lower().startswith("report")

def handle(query: str, console, current_investigation=None):
    _, *args = query.split()

    if args and args[0] == "case":
        if len(args) < 2:
            console.print("[bold red]Usage: report case <case_name>[/]")
            return
        case_name = args[1]
        fmt = "html" if len(args) > 2 and args[2] == "html" else "markdown"
        path = generate_case_report(case_name, fmt=fmt)
        console.print(f"[bold green]Case report generated:[/] {path}")
        return

    target = current_investigation.target if current_investigation else None
    if not target:
        console.print("[bold red]No active investigation.[/]")
        return

    fmt = "html" if len(args) > 0 and args[0] == "html" else "markdown"
    path = generate_investigation_report(target, fmt=fmt)
    console.print(f"[bold green]Investigation report generated:[/] {path}")
