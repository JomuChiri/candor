# candor/progress.py
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

console = Console()

def staged_progress(stages: list[str], run_stage_callback):
    """
    Show staged progress reporting.
    stages: list of stage names (e.g. ["Planning", "Executing", "Collecting output"])
    run_stage_callback: function(stage_name) -> None
    """
    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        for stage in stages:
            task = progress.add_task(stage, total=100)
            # simulate staged progress
            progress.update(task, advance=30)
            run_stage_callback(stage)
            progress.update(task, advance=70)
            progress.remove_task(task)
