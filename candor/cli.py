# candor/cli.py
import click
import json

from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from candor.parser.intent import parse_intent
from candor.parser.planner import build_plan
from candor.modules import registry
from candor.core.history import record_job, list_jobs, load_job
from candor.core.logger import log_execution
from candor.config import load_config
from candor.progress import staged_progress
from candor.reporting import save_report
from candor.doctor import doctor
from candor.modules.nmap.summary import summarize_nmap
from candor.modules.whois.summary import summarize_whois
from candor.core.investigation import Investigation
from candor.analysis.assess import assess_ports
from candor.parser.confidence import assess_confidence
from candor.core.timeline import Timeline
from candor.core.findings import FindingsDB
from candor.analysis.recommendations import explain_recommendation

console = Console()

@click.command()
def main():
    global current_investigation
    current_investigation = None
    config = load_config()
    console.print("[bold cyan]Candor SOC Assistant v0.4[/]")
    console.print(f"[yellow]Loaded config:[/] {config}")
    console.print("Type 'exit' to quit, or 'jobs' to list history.\n")

    while True:
        query = Prompt.ask("[bold yellow]>[/]")

        # Exit
        if query.lower() in ("exit", "quit"):
            console.print("[bold red]Exiting... Goodbye![/]")
            break

        # Jobs
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

        # Help
        if query.lower().startswith("help"):
            _, *args = query.split()
            if not args:
                console.print("[bold magenta]Available modules by category:[/]")
                categories = registry.list_by_category()
                for cat, mods in categories.items():
                    console.print(f"\n[bold cyan]{cat}[/]")
                    for meta in mods:
                        console.print(f" - {meta['name']}: {meta['description']} (Risk: {meta['risk']})")
            else:
                module = registry.get(args[0])
                console.print(module.help() if module else f"[bold red]No such module: {args[0]}[/]")
            continue

        # Findings
        if query.lower().startswith("findings"):
            db = FindingsDB()
            console.print("\n[bold magenta]Findings Database[/]")
            for severity, items in db.list_findings().items():
                console.print(f"\n[bold cyan]{severity}[/]")
                for item in items:
                    console.print(f"- {item['description']} "
                          f"(Target: {item['target']}, Source: {item['source']}, MITRE: {item['mitre']})")
            continue

        # Explain Mode
        if query.lower().startswith("explain"):
            _, *args = query.split()
            if not args:
                console.print("[bold red]Usage: explain <action>[/]")
                continue
            from candor.explain import explain
            console.print(explain(args[0]))
            continue

        # Metadata
        if query.lower().startswith("metadata"):
            _, *args = query.split()
            if not args:
                console.print("[bold magenta]Available modules:[/]")
                for module in registry.MODULES.values():
                    console.print(f" - {module.name}")
            else:
                module = registry.get(args[0])
                if module:
                    console.print(json.dumps(module.metadata(), indent=2))
                else:
                    console.print(f"[bold red]No such module: {args[0]}[/]")
            continue

        # Report
        if query.lower().startswith("report"):
            _, *args = query.split()
            target = current_investigation.target if current_investigation else None
            if not target:
                console.print("[bold red]No active investigation.[/]")
                continue
            fmt = "html" if len(args) > 0 and args[0] == "html" else "markdown"
            from candor.reporting.rich import generate_report
            path = generate_report(target, fmt=fmt)
            console.print(f"[bold green]Report generated:[/] {path}")
            continue    

        # Doctor
        if query.lower().startswith("doctor"):
            _, *args = query.split()
            results = doctor(args[0] if args else None)
            console.print("\n[bold magenta]System Health Check[/]")
            for name, info in results.items():
                if info["installed"]:
                    console.print(f"✓ {name} installed")
                    console.print(f"   Path   : {info['path']}")
                    console.print(f"   Version: {info['version']}")
                else:
                    console.print(f"✗ {name} missing")
            continue

        # Workflow
        if query.lower().startswith("workflow"):
            _, wf_name, *args = query.split()
            target = args[0] if args else (current_investigation.target if current_investigation else None)
            if not target:
                console.print("[bold red]No target specified or active investigation.[/]")
                continue

            from candor.workflows import WORKFLOWS
            if wf_name not in WORKFLOWS:
                console.print(f"[bold red]No such workflow:[/] {wf_name}")
                continue

            console.print(f"\n[bold magenta]Workflow:[/] {wf_name}")
            console.print("────")
            for i, step in enumerate(WORKFLOWS[wf_name], 1):
                console.print(f"{i}. {step['tool']} {step['action']} {target}")

            answer = Prompt.ask("\nExecute workflow? (y/n)", default="n")
            if answer.lower() != "y":
                continue

        # Case management
        if query.lower().startswith("case"):
            _, action, *args = query.split()
            from candor.core.case import Case

            if action == "create":
                case = Case(args[0])
                console.print(f"[bold green]Case created:[/] {args[0]}")
            elif action == "add":
                if not current_investigation:
                    console.print("[bold red]No active investigation to add.[/]")
                else:
                    case = Case(args[0])
                    case.add_investigation(current_investigation.target)
                    console.print(f"[bold green]Investigation {current_investigation.target} added to case {args[0]}")
            elif action == "list":
                case = Case(args[0])
                console.print(f"\n[bold magenta]Case {args[0]} Investigations[/]")
                for inv in case.list_investigations():
                    console.print(f"- {inv}")
            continue

        # Parallel workflows
        if "&" in query.lower():
            workflows = [wf.strip() for wf in query.lower().split("&")]
            _, *args = workflows[0].split()
            target = args[0] if args else (current_investigation.target if current_investigation else None)
            if not target:
                console.print("[bold red]No target specified or active investigation.[/]")
                continue

            from candor.workflows.parallel import run_parallel
            results = run_parallel(workflows, target, current_investigation)

            console.print("\n[bold magenta]Parallel Workflow Results[/]")
            for wf_name, wf_results in results.items():
                console.print(f"\nWorkflow: {wf_name}")
                if isinstance(wf_results, dict) and "error" in wf_results:
                    console.print(f"[bold red]{wf_results['error']}[/]")
                else:
                    for step in wf_results:
                        console.print(f"- {step['tool']} {step['action']} → {step['status']}")
            continue


            # Run workflow sequentially
            for step in WORKFLOWS[wf_name]:
                step["target"] = target
                module = registry.get(step["tool"])
                result = module.execute(step)

                # Evidence storage
                if current_investigation:
                    evidence_file = f"candor/investigations/{target}/{step['tool']}-{step['action']}.txt"
                    Path(evidence_file).parent.mkdir(parents=True, exist_ok=True)
                    with open(evidence_file, "w") as f:
                        f.write(result.stdout or "")
                    current_investigation.add_command(f"{step['tool']}-{step['action']}", evidence_file, summary="...")
                    current_investigation.save()
            continue


        # Parse intent
        try:
            intent = parse_intent(query)
        except ValueError as e:
            console.print(f"[bold red]{e}[/]")
            continue

        plan = build_plan(intent)

        # Smarter planner: multi-step
        if isinstance(plan, list) and len(plan) > 1:
            console.print(f"\n[bold magenta]Planner[/]")
            console.print("────")
            for i, step in enumerate(plan, 1):
                console.print(f"{i}. {step['tool']} {step['action']} {step['target']}")
            answer = Prompt.ask("\nExecute sequentially? (y/n)", default="n")
            if answer.lower() != "y":
                continue

            for step in plan:
                module = registry.get(step["tool"])
                result = module.execute(step)
                # Record evidence
                if current_investigation:
                    evidence_file = f"candor/investigations/{step['target']}/{step['tool']}-{step['action']}.txt"
                    Path(evidence_file).parent.mkdir(parents=True, exist_ok=True)
                    with open(evidence_file, "w") as f:
                        f.write(result.stdout or "")
                    current_investigation.add_command(f"{step['tool']}-{step['action']}", evidence_file, summary="...")
                    current_investigation.save()
        else:
            # Single-step plan (existing logic)
            if not intent:
                console.print("[bold red]I don't understand.[/]")
                continue

        #confidence
        candidates = intent.candidates if hasattr(intent, "candidates") else []
        confidence = assess_confidence(intent, candidates)

        if confidence["status"] == "low":
            console.print("[bold yellow]Did you mean:[/]")
            for i, cand in enumerate(confidence["candidates"], 1):
                console.print(f"{i}. {cand['action']} ({cand['tool']})")
            choice = Prompt.ask("Choice", default="1")
            intent.action = confidence["candidates"][int(choice)-1]["action"]

        # Session awareness
        if intent.tool == "whois":
            current_investigation = Investigation(intent.target)
            console.print(f"[bold green]Investigation started:[/] {intent.target}")

        elif intent.tool in ["nmap", "dig", "dnsrecon"]:
            if not intent.target and current_investigation:
                intent.target = current_investigation.target
                console.print(f"[bold yellow]Using previous target:[/] {intent.target}")

        plan = build_plan(intent)
        console.print(f"\n[bold magenta]Plan[/]")
        console.print("────")
        console.print(f"Tool    : {intent.tool}")
        console.print(f"Action  : {intent.action}")
        console.print(f"Target  : {intent.target}")
        console.print(f"Command : {' '.join(plan.command)}")

        answer = Prompt.ask("\nExecute? (y/n)", default="n")
        if answer.lower() != "y":
            continue

        module = registry.get(intent.tool)
        result = None

        def run_stage(stage):
            nonlocal result
            if stage == "Executing":
                result = module.execute(plan)
                job = record_job(intent, plan, result)
                log_execution(job)

        staged_progress(["Planning", "Executing", "Collecting output"], run_stage)

        # Evidence storage
        if current_investigation:
            evidence_dir = f"candor/investigations/{intent.target}"
            Path(evidence_dir).mkdir(parents=True, exist_ok=True)
            evidence_file = f"{evidence_dir}/{intent.tool}-{intent.action}.txt"
            with open(evidence_file, "w") as f:
                f.write(result.stdout or "")
            current_investigation.add_command(f"{intent.tool}-{intent.action}", evidence_file, summary="...")
            current_investigation.save()
            if not hasattr(current_investigation, "timeline"):
                current_investigation.timeline = Timeline(current_investigation.target)
            current_investigation.timeline.add_event(f"{intent.tool}-{intent.action}")
            current_investigation.timeline.save()

        # Status
        if result.status == "success":
            console.print("[bold green]✓ Success[/]")
        elif result.status == "warning":
            console.print("[bold yellow]⚠ Completed with warnings[/]")
        else:
            console.print("[bold red]✗ Failed[/]")

        # Summary  
        if intent.tool == "whois":
            console.print("[bold blue]Summary:[/]")
            console.print(summarize_whois(result.stdout))

        if intent.tool == "nmap":
            console.print("[bold blue]Summary:[/]")
            summary = summarize_nmap(result.stdout)
            console.print(summary)

            # Extract open ports from summary (assuming summary returns list or parse it)
            open_ports = summary.get("open_ports", [])
            assessment = assess_ports(open_ports)

            # Map risk to severity
            severity_map = {"LOW": "Informational", "MEDIUM": "Medium", "HIGH": "High"}
            severity = severity_map.get(assessment["risk"], "Informational")

            db = FindingsDB()
            for f in assessment["assessment"]:
                db.add_finding(severity, f, f"{intent.tool}-{intent.action}", intent.target)

            console.print("\n[bold magenta]Assessment[/]")
            console.print(f"Risk: {assessment['risk']}")
            for f in assessment["assessment"]:
                console.print(f"- {f}")
            console.print("\n[bold magenta]Recommendations[/]")
            for r in assessment["recommendations"]:
                console.print(explain_recommendation(r))

        # Raw output
        if result.stdout:
            console.print("\n[bold blue]Raw Output:[/]")
            console.print(result.stdout)
        if result.stderr:
            console.print("[bold red]Errors:[/]")

            console.print(result.stderr)

if __name__ == "__main__":
    main()
