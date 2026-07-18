# candor/core/controller.py
from rich.panel import Panel
from candor.modules.registry import registry
from candor.core.intent import parse_intent
from candor.core.output import (
    show_raw_output,
    success,
    warning,
)
from candor.core.investigation_manager import (
    record_execution,
)
from candor.core.errors import IntentParseError
from candor.analysis.reporting import render_analysis
from candor.analysis.state import InvestigationState

def run(query, console, current_investigation):

    # --------------------------------------------------
    # HELP
    # --------------------------------------------------
    if query.strip().startswith("help"):
        parts = query.strip().split(maxsplit=2)

        # help
        if len(parts) == 1:
            for category, modules in registry.by_category().items():
                console.print(f"\n[bold cyan]{category}[/]")
                for meta in modules:
                    console.print(
                        f"  • {meta['name']}: "
                        f"{meta['description']}"
                    )
            return

        # help categories
        if parts[1] == "categories":
            console.print("[bold cyan]Categories[/]")
            for category in registry.by_category():
                console.print(f"  • {category}")
            return

        # help search smb
        if parts[1] == "search" and len(parts) == 3:
            keyword = parts[2].lower()
            matches = []
            for meta in registry.list():
                if (
                    keyword in meta["name"].lower()
                    or keyword in meta["description"].lower()
                ):
                    matches.append(meta)
            if not matches:
                warning(f"No modules found for '{keyword}'")
                return
            console.print(f"[bold cyan]Matches for '{keyword}'[/]")
            for meta in matches:
                console.print(
                    f"  • {meta['name']}: "
                    f"{meta['description']}"
                )
            return

        # help actions nmap
        if parts[1] == "actions" and len(parts) == 3:
            module = registry.resolve(parts[2])
            console.print(f"[bold cyan]{module.name} actions[/]")
            for action, desc in module.actions.items():
                console.print(f"  • {action:<12} {desc}")
            return

        # help default nmap
        if parts[1] == "default" and len(parts) == 3:
            module = registry.resolve(parts[2])
            console.print(f"Default action: {getattr(module, 'default_action', None)}")
            return

        # help nmap
        try:
            module = registry.resolve(parts[1])
            console.print(module.help())
        except KeyError:
            warning(f"No module named '{parts[1]}'")
        return

    # --------------------------------------------------
    # EXECUTION
    # --------------------------------------------------
    try:
        intent = parse_intent(query)
        module = registry.resolve(intent.tool)
        command = module.build(intent)
    except IntentParseError as e:
        warning(str(e))
        return
    except Exception as e:
        warning(f"Planning failed: {e}")
        return

    # Execute
    result = module.execute(command)
    show_raw_output(result, show=True)
    record_execution(intent, result, current_investigation)

    # Analysis
    analysis = module.analyze(result)
    if analysis:
        render_analysis(analysis)

    success(f"{module.name} {intent.action} completed.")

def run_next_step(state: InvestigationState, console):
    rec = state.next_step()
    if not rec:
        console.print("[bold green]No pending recommendations. Investigation complete.[/]")
        return

    console.print(
        Panel.fit(
            f"[bold cyan]Recommended Next Step[/]\n\n"
            f"Run:\n candor> {rec.tool} {rec.action} {rec.arguments.get('target','')}\n\n"
            f"Reason:\n {rec.reason}",
            title="Next Investigation",
        )
    )
