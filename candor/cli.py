import click
import json
from rich.console import Console
from rich.prompt import Prompt

from candor.parser.intent import parse_intent
from candor.parser.planner import build_plan
from candor.modules import registry
from candor.modules.registry import MODULES
from candor.core.history import record_job, list_jobs, load_job
from candor.core.logger import log_execution
from candor.config import load_config
from candor.progress import staged_progress
from candor.reporting import save_report
from candor.doctor import doctor

console = Console()

@click.command()
def main():
    config = load_config()
    console.print("[bold cyan]Candor SOC Assistant v0.4[/]")
    console.print(f"[yellow]Loaded config:[/] {config}")
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

        if query.lower().startswith("help"):
            _, *args = query.split()
            if not args:
                console.print("[bold magenta]Available modules:[/]")
                for module in registry.MODULES.values():
                    meta = module.metadata()
                    console.print(f" - {meta['name']}: {meta['description']}")
                continue

            module_name = args[0]
            module = registry.get(module_name)
            if not module:
                console.print(f"[bold red]No such module: {module_name}[/]")
            else:
                console.print(module.help())
            continue

        if query.lower().startswith("metadata"):
            _, *args = query.split()
            if not args:
                console.print("[bold magenta]Available modules:[/]")
                for module in registry.MODULES.values():
                    console.print(f" - {module.name}")
                continue

            module_name = args[0]
            module = registry.get(module_name)
            if not module:
                console.print(f"[bold red]No such module: {module_name}[/]")
            else:
                meta = module.metadata()
                console.print(json.dumps(meta, indent=2))
            continue

        if query.lower().startswith("report"):
            _, *args = query.split()
            if not args or args[0] == "latest":
                job = load_job("latest")
            else:
                job_id = int(args[0])
                job = load_job(job_id)

            if not job:
                console.print("[bold red]No such job found.[/]")
                continue

            fmt = "markdown"
            if len(args) > 1 and args[1] == "html":
                fmt = "html"

            path = save_report(job, fmt=fmt)
            console.print(f"[bold green]Report saved:[/] {path}")
            continue

        if query.lower().startswith("doctor"):
            _, *args = query.split()
            tool = args[0] if args else None

            results = doctor(tool)
            console.print("\n[bold magenta]System Health Check[/]")
            for name, info in results.items():
                if info["installed"]:
                    console.print(f"✓ {name} installed")
                    console.print(f"   Path   : {info['path']}")
                    console.print(f"   Version: {info['version']}")
                else:
                    console.print(f"✗ {name} missing")
            continue

        # Parse intent
        try:
            intent = parse_intent(query)
        except ValueError as e:
            console.print(f"[bold red]{e}[/]")
            continue

        if not intent:
            console.print("[bold red]I don't understand.[/]")
            continue

        plan = build_plan(intent)
        console.print(f"\n[bold magenta]Plan:[/] {plan.command}")

        answer = Prompt.ask("\nExecute? (y/n)", default="n")
        if answer.lower() == "y":
            module = registry.get(intent.tool)
            result = None  # declare in outer scope

            def run_stage(stage):
                nonlocal result  # <-- remove this line entirely
                if stage == "Planning":
                    pass  # plan already built
                elif stage == "Executing":
                    result = module.execute(plan)
                    job = record_job(intent, plan, result)
                    log_execution(job)
                elif stage == "Collecting output":
                    pass

            staged_progress(["Planning", "Executing", "Collecting output"], run_stage)

            # After progress, show results
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
