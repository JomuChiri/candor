# candor/commands/jobs.py
from candor.core.history import list_jobs

def matches(query: str) -> bool:
    return query.lower() == "jobs"

def handle(query: str, console):
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
