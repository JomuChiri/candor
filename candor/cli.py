import click
from rich.console import Console
from rich.prompt import Prompt

from candor.parser.intent import parse_intent
from candor.parser.planner import build_plan
from candor.shell.execute import run_command

console = Console()

@click.command()
def main():
    console.print("[bold cyan]Candor SOC Assistant v0.1[/]")
    console.print("Type 'exit' to quit.\n")

    while True:
        query = Prompt.ask("[bold yellow]>[/]")

        if query.lower() in ("exit", "quit"):
            console.print("[bold red]Exiting... Goodbye![/]")
            break

        intent = parse_intent(query)

        if not intent:
            console.print("[bold red]I don't understand.[/]")
            continue

        plan = build_plan(intent)

        console.print("\n[bold magenta]Plan:[/]")
        console.print(f"[green]{plan.command}[/]")

        answer = Prompt.ask("\nExecute? (y/n)", default="n")

        if answer.lower() == "y":
            with console.status("[bold green]Running command..."):
                output = run_command(plan.command)

            console.print("[bold blue]Output:[/]")
            console.print(output)
