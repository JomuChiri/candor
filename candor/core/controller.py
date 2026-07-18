from candor.modules.registry import MODULES, list_by_category
from candor.core.intent import parse_intent
from candor.core.plan import Plan
from candor.core.output import show_raw_output, success, warning
from candor.core.investigation_manager import record_execution
from candor.core.executor import execute_plan
from candor.parser.planner import build_plan
from candor.analysis.analyzer import analyze_services
from candor.analysis.reporting import render_analysis
from candor.modules.nmap.summary import summarize_nmap
from candor.core.errors import IntentParseError

def run(query, console, current_investigation):
    """
    Thin orchestrator: parse → plan → execute → analyze → report.
    """
     # Special case: help, help <tool>, help categories, help search <keyword>, help actions <tool>, help default <tool>
    if query.strip().startswith("help"):
        parts = query.strip().split(maxsplit=2)
        if len(parts) == 1:
            # Global help: list all modules by category
            categories = list_by_category()
            for category, modules in categories.items():
                console.print(f"[bold cyan]{category}[/]")
                for meta in modules:
                    console.print(f"  • {meta['name']}: {meta['description']}")
            return
        elif parts[1].lower() == "categories":
            # Just list categories
            categories = list_by_category()
            console.print("[bold cyan]Available Categories[/]")
            for category in categories.keys():
                console.print(f"  • {category}")
            return
        elif parts[1].lower() == "search" and len(parts) == 3:
            # Search help by keyword
            keyword = parts[2].lower()
            matches = []
            for module in MODULES.values():
                meta = module.metadata()
                if keyword in meta["name"].lower() or keyword in meta["description"].lower():
                    matches.append(meta)
            if not matches:
                console.print(f"[bold red]No tools found matching keyword:[/] {keyword}")
                return
            console.print(f"[bold cyan]Tools matching '{keyword}'[/]")
            for meta in matches:
                console.print(f"  • {meta['name']}: {meta['description']}")
            return
        elif parts[1].lower() == "actions" and len(parts) == 3:
            # List actions for a specific tool
            tool = parts[2].strip()
            module = MODULES.get(tool)
            if not module:
                warning(f"No module registered for tool: {tool}")
                return
            actions = module.metadata()["actions"]
            console.print(f"[bold cyan]Available actions for {tool}[/]")
            for action in actions.keys():
                console.print(f"  • {action}")
            return
        elif parts[1].lower() == "default" and len(parts) == 3:
            # Show default action for a specific tool
            tool = parts[2].strip()
            module = MODULES.get(tool)
            if not module:
                warning(f"No module registered for tool: {tool}")
                return
            default_action = module.metadata()["default_action"]
            console.print(f"[bold cyan]Default action for {tool}[/]")
            console.print(f"  • {default_action}")
            return
        else:
            # Tool-specific help
            tool = parts[1].strip()
            module = MODULES.get(tool)
            if not module:
                warning(f"No module registered for tool: {tool}")
                return
            console.print(module.help())
            return

    try:
        intent = parse_intent(query)
        plan = build_plan(intent)
    except Exception as e:
        warning(f"Failed to parse/build plan: {e}")
        return

    # Execute centrally
    result = execute_plan(plan)
    show_raw_output(result, show=True)
    record_execution(intent, result, current_investigation)

    # --- Unified analysis hook ---
    if plan.tool == "nmap":
        # Parse services from nmap output
        summary = summarize_nmap(result.stdout)
        services = summary.get("open_ports", [])

        # Run analyzer + render report
        analysis = analyze_services(services, target=intent.target)
        render_analysis(analysis)

    else:
        # Fall back to module-specific analyze() if defined
        module = MODULES.get(plan.tool)
        if module and hasattr(module, "analyze"):
            analysis = module.analyze(result)
            if analysis:
                # If the module returns an AnalysisResult, render it
                if hasattr(analysis, "summary") and hasattr(analysis, "findings"):
                    render_analysis(analysis)
                else:
                    # Fallback: if module returns plain text
                    console.print(f"[bold magenta]Analysis:[/] {analysis}")

    success(f"{plan.tool.capitalize()} {plan.action} recorded.")