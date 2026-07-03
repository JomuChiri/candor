import click
from rich.console import Console
from rich.prompt import Prompt

from candor.parser.intent import parse_intent
from candor.parser.planner import build_plan
from candor.modules import registry
from candor.core.history import record_job, list_jobs
from candor.core.logger import log_execution
from candor.modules.registry import MODULES

console = Console()

@click.command()
def main():
    console.print(f"[yellow]Loaded modules:[/] {list(MODULES.keys())}")
    console.print("[bold cyan]Candor SOC Assistant v0.3[/]")
    console.print("Type 'exit' to quit, or 'jobs' to list history.\n")

    while True:
        query = Prompt.ask("[bold yellow]>[/]")

        if query.lower() in ("exit", "quit"):
            console.print("[bold red]Exiting... Goodbye![/]")
            break

        if query.lower() == "jobs":
            jobs = list_jobs()
            if not jobs:
                console.print("[bold magenta]No jobs recorded yet.[/]")
            else:
                console.print("\n[bold magenta]Execution History[/]")
                for job in jobs:
                    console.print(
                        f"Job #{job.id} | Tool: {job.intent.tool} | "
                        f"Action: {job.intent.action} | Target: {job.intent.target} | "
                        f"Exit: {job.result.returncode} | Duration: {job.result.elapsed:.2f}s"
                    )
            continue

        intent = parse_intent(query)
        if not intent:
            console.print("[bold red]I don't understand.[/]")
            continue

        plan = build_plan(intent)
        console.print(f"\n[bold magenta]Plan:[/] {plan.command}")

        answer = Prompt.ask("\nExecute? (y/n)", default="n")
        if answer.lower() == "y":
            module = registry.get(intent.tool)
            result = module.execute(plan)

            # Record job + log to disk
            job = record_job(intent, result)
            log_execution(job)

            console.print("\n[bold magenta]Plan[/]")
            console.print("────")
            console.print(f"Tool    : {intent.tool}")
            console.print(f"Action  : {intent.action}")
            console.print(f"Target  : {intent.target}")
            console.print(f"Command : {' '.join(plan.command)}")

            if result.status == "success":
                console.print("[bold green]✓ Success[/]")
            elif result.status == "warning":
                console.print("[bold yellow]⚠ Completed with warnings[/]")
            else:
                console.print("[bold red]✗ Failed[/]")


            if result.stdout:
                console.print("[bold blue]Output:[/]")
                console.print(result.stdout)
            if result.stderr:
                console.print("[bold red]Errors:[/]")
                console.print(result.stderr)

if __name__ == "__main__":
    main()
