# candor/commands/execute.py
from rich.prompt import Prompt
from rich.console import Console
from candor.parser.intent import parse_intent
from candor.parser.planner import build_plan
from candor.analysis.pipeline import analyze
from candor.analysis.reporting import render_analysis
from candor.core import output
from candor.core.executor import run_plan

console = Console()

class ExecResult:
    """
    Lightweight wrapper around executor output so downstream code
    (analysis pipeline, reporting) can access attributes like
    stdout, stderr, exit_code, and status.
    """
    def __init__(self, stdout: str, stderr: str, exit_code: int):
        self.stdout = stdout or ""
        self.stderr = stderr or ""
        self.exit_code = exit_code
        if exit_code == 0:
            self.status = "success"
        elif exit_code == 2:
            self.status = "warning"
        else:
            self.status = "error"

def matches(query: str) -> bool:
    return True  # fallback handler

def _print_plan(plan):
    console.print("\n[bold magenta]Plan[/]")
    console.print("────")
    console.print(f"Tool    : {plan.tool}")
    console.print(f"Action  : {plan.action}")
    console.print(f"Target  : {plan.target}")
    console.print(f"Command : {plan.command}")

def handle(query: str, console_obj=None, current_investigation=None, show_raw=False):
    """
    Parse the query, build a plan (or plans), show the plan to the user,
    optionally execute it via the executor, run analysis on the result,
    and render the analysis.
    """
    console_local = console_obj or console

    # Parse intent
    intent = parse_intent(query)
    if not intent:
        output.error(f"Unknown command: {query}")
        return

    # Build plan (may be a single Plan or a list of Plan objects)
    plan_or_steps = build_plan(intent)

    # Normalize to list for uniform handling
    plans = plan_or_steps if isinstance(plan_or_steps, list) else [plan_or_steps]

    # Show the first plan summary (if multi-step, show first and count)
    if len(plans) == 1:
        _print_plan(plans[0])
    else:
        console_local.print("\n[bold magenta]Plan (multi-step)[/]")
        console_local.print("────")
        console_local.print(f"[dim]This will run {len(plans)} steps[/dim]")
        for i, p in enumerate(plans, start=1):
            console_local.print(f"{i}. {p.tool} {p.action} {p.target} -> {p.command}")

    # Confirm execution
    answer = Prompt.ask("\nExecute? (y/n)", default="n")
    if answer.lower() != "y":
        return

    # Execute each plan step and collect results
    last_exec_result = None
    aggregated_stdout = []
    aggregated_stderr = []
    for step in plans:
        console_local.print(f"\n[bold]Executing[/] {step.tool} {step.action} {step.target}")
        exec_out = run_plan(step)

        # run_plan returns a dict with stdout, stderr, exit_code
        stdout = exec_out.get("stdout", "")
        stderr = exec_out.get("stderr", "")
        exit_code = exec_out.get("exit_code", 1)

        # Print outputs as they come
        if stdout:
            console.print(f"[dim]{step.tool.upper()} Output data captured. Use 'Show raw output' to view full text.[/dim]")
        if stderr:
            console_local.print(f"[red]{stderr}[/red]")

        # Wrap into ExecResult for downstream compatibility
        last_exec_result = ExecResult(stdout=stdout, stderr=stderr, exit_code=exit_code)

        # Aggregate for potential raw view or combined analysis
        aggregated_stdout.append(stdout)
        aggregated_stderr.append(stderr)

        # Optionally record each step in investigation history
        if current_investigation and hasattr(current_investigation, "add_job"):
            try:
                current_investigation.add_job(intent, step, {
                    "stdout": stdout,
                    "stderr": stderr,
                    "exit_code": exit_code
                })
            except Exception:
                # Don't let history logging break execution flow
                pass

    # If nothing executed, bail out
    if last_exec_result is None:
        output.error("No execution result available")
        return

    # Prepare a combined result object for analysis
    combined_result = ExecResult(
        stdout="\n".join(aggregated_stdout),
        stderr="\n".join(aggregated_stderr),
        exit_code=last_exec_result.exit_code
    )

    # Run analysis pipeline on the last (or combined) result
    try:
        analysis = analyze(intent, combined_result)
    except Exception as e:
        console_local.print(f"[red]Analysis failed: {e}[/red]")
        analysis = None

    # Render structured output if analysis succeeded
    if analysis:
        try:
            render_analysis(analysis)
        except Exception as e:
            console_local.print(f"[red]Rendering failed: {e}[/red]")

    # Status messages based on combined_result.status
    if combined_result.status == "success":
        output.success("Execution completed")
    elif combined_result.status == "warning":
        output.warning("Execution completed with warnings")
    else:
        output.error("Execution failed")

    # Raw output toggle
    answer = Prompt.ask("\nShow raw output? (y/n)", default="n")
    if answer.lower() == "y":
        output.show_raw_output(combined_result, show=True)

    # Suggested follow-ups
    console_local.print("\nSuggested commands")
    console_local.print("1. scan-service {target}".format(target=plans[-1].target))
    console_local.print(f"2. whois {plans[-1].target}")
    console_local.print(f"3. dig {plans[-1].target}")
    console_local.print(f"4. workflow web {plans[-1].target}")
    console_local.print("5. show raw output")

    choice = Prompt.ask("Enter command number or press Enter to continue", default="")

    target = plans[-1].target  # <-- define once

    if choice == "5":
        # Show raw output only when explicitly requested
        output.show_raw_output(combined_result, show=True)
    elif choice == "1":
        handle(f"scan-service {target}", console_obj=console_local, current_investigation=current_investigation)
    elif choice == "2":
        handle(f"whois {target}", console_obj=console_local, current_investigation=current_investigation)
    elif choice == "3":
        handle(f"dig {target}", console_obj=console_local, current_investigation=current_investigation)
    elif choice == "4":
        handle(f"workflow web {target}", console_obj=console_local, current_investigation=current_investigation)
