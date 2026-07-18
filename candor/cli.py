import click
from rich.console import Console
from rich.prompt import Prompt
from candor.core import controller
from candor.core.investigation_manager import Investigation

console = Console()

@click.group()
def cli():
    """Candor SOC Assistant CLI"""
    pass

@cli.command()
def main():
    """
    Interactive REPL loop for Candor SOC Assistant.
    """
    console.print("[bold cyan]Candor SOC Assistant v0.7[/]")
    console.print("Type 'exit' to quit.\n")

    # Initialize investigation state
    current_investigation = None

    while True:
        query = Prompt.ask("[bold yellow]>[/]")
        if query.lower() in ("exit", "quit"):
            console.print("[bold red]Exiting... Goodbye![/]")
            break

        # Special built-in commands
        if query.lower().startswith("summarize"):
            if current_investigation:
                summary = current_investigation.summarize()
                console.print("\n[bold magenta]Current Investigation[/]")
                console.print("────")
                console.print(f"Target   : {summary['Target']}")
                console.print(f"Services : {summary['Services']}")
                console.print(f"Risk     : {summary['Risk']}")
                console.print("\n[bold magenta]Critical Findings[/]")
                console.print("────")
                if summary["Critical Findings"]:
                    for f in summary["Critical Findings"]:
                        svc = f.get("service")
                        sev = f.get("severity", "").upper()
                        desc = f.get("description", "")
                        console.print(f"• {svc} — {desc} (Severity: {sev})")
                else:
                    console.print("• None identified")
                console.print("\n[bold magenta]Completed[/]")
                console.print("────")
                if summary["Completed"]:
                    for c in summary["Completed"]:
                        console.print(f"- {c}")
                else:
                    console.print("• No actions recorded")
            else:
                console.print("[bold yellow]⚠ No active investigation.[/]")
            continue

        # Start a new investigation if none exists
        if not current_investigation and query.startswith("scan-service"):
            # Extract target from query
            parts = query.split()
            target = parts[-1] if len(parts) > 1 else "unknown"
            current_investigation = Investigation(target)

        # Pass query to controller with current investigation
        controller.run(query, console, current_investigation)
