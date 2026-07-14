# candor/core/output.py
from rich.console import Console

console = Console()

def heading(text: str, color="magenta"):
    console.print(f"\n[bold {color}]{text}[/]")
    console.print("────")

def success(msg: str):
    console.print(f"[bold green]✓ {msg}[/]")

def warning(msg: str):
    console.print(f"[bold yellow]⚠ {msg}[/]")

def error(msg: str):
    console.print(f"[bold red]✗ {msg}[/]")

def info(msg: str, color="blue"):
    console.print(f"[bold {color}]{msg}[/]")

def list_items(items, color="cyan"):
    for item in items:
        console.print(f"[bold {color}]-[/] {item}")

def show_raw_output(result, show=False):
    """
    Print raw stdout/stderr only if show=True.
    """
    if show and result.stdout:
        console.print("\n[bold blue]Raw Output:[/]")
        console.print(result.stdout)
    if show and result.stderr:
        console.print("[bold red]Errors:[/]")
        console.print(result.stderr)
