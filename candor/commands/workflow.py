# candor/commands/workflow.py
from rich.prompt import Prompt
from candor.workflows.runner import run_workflow, run_parallel_workflows
from candor.workflows import WORKFLOWS

def matches(query: str) -> bool:
    return query.lower().startswith("workflow") or "&" in query.lower()

def handle(query: str, console, current_investigation=None):
    if "&" in query.lower():
        # Parallel workflows
        workflows = [wf.strip() for wf in query.lower().split("&")]
        _, *args = workflows[0].split()
        target = args[0] if args else (current_investigation.target if current_investigation else None)
        if not target:
            console.print("[bold red]No target specified or active investigation.[/]")
            return

        results = run_parallel_workflows(workflows, target, current_investigation)
        console.print("\n[bold magenta]Parallel Workflow Results[/]")
        for wf_name, wf_results in results.items():
            console.print(f"\nWorkflow: {wf_name}")
            if isinstance(wf_results, dict) and "error" in wf_results:
                console.print(f"[bold red]{wf_results['error']}[/]")
            else:
                for step in wf_results:
                    console.print(f"- {step['tool']} {step['action']} → {step['status']}")
        return

    # Sequential workflow
    _, wf_name, *args = query.split()
    target = args[0] if args else (current_investigation.target if current_investigation else None)
    if not target:
        console.print("[bold red]No target specified or active investigation.[/]")
        return

    if wf_name not in WORKFLOWS:
        console.print(f"[bold red]No such workflow:[/] {wf_name}")
        return

    console.print(f"\n[bold magenta]Workflow:[/] {wf_name}")
    console.print("────")
    for i, step in enumerate(WORKFLOWS[wf_name], 1):
        console.print(f"{i}. {step['tool']} {step['action']} {target}")

    answer = Prompt.ask("\nExecute workflow? (y/n)", default="n")
    if answer.lower() != "y":
        return

    results = run_workflow(wf_name, target, current_investigation)
    console.print("\n[bold magenta]Workflow Results[/]")
    for step in results:
        console.print(f"- {step['tool']} {step['action']} → {step['status']}")
