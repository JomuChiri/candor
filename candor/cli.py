import click
from rich.console import Console
from rich.prompt import Prompt
from candor.core import controller

console = Console()

@click.command()
def main():
    console.print("[bold cyan]Candor SOC Assistant v0.6[/]")
    console.print("Type 'exit' to quit.\n")

    current_investigation = None

    while True:
        query = Prompt.ask("[bold yellow]>[/]")
        if query.lower() in ("exit", "quit"):
            console.print("[bold red]Exiting... Goodbye![/]")
            break

        controller.run(query, console, current_investigation)
