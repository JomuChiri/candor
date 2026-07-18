# candor/parser/planner.py

from candor.modules import registry
from candor.core.intent import Intent
from candor.core.plan import Plan

def build_plan(intent: Intent):
    """
    Build execution plan from intent.
    For v0.6, support high-level actions like 'enumerate' or 'investigate'.
    Returns either a list of Plan objects (multi-step) or a single Plan.
    """

    module = registry.get(intent.tool)

    # Multi-step investigation sequences
    if intent.action in ["enumerate", "investigate"]:
        steps = [
            Plan("whois", "lookup", intent.target, f"whois {intent.target}"),
            Plan("dig", "lookup", intent.target, f"dig {intent.target}"),
            Plan("nmap", "scan-fast", intent.target, f"nmap -F {intent.target}"),
            Plan("nmap", "scan-service", intent.target, f"nmap -sV {intent.target}"),
        ]
        return steps

    # If no module found, bail out
    if not module:
        raise ValueError(f"No module found for tool {intent.tool}")

    # Delegate to module-specific builder
    plan = module.build(intent.action, intent.target)

    #Wrap in Plan object if module returns a raw command list
    if isinstance(plan, list):
        return Plan(
            tool=intent.tool,
            action=intent.action,
            target=intent.target,
            command=plan
        )

    # If module returns dict, normalize
    if isinstance(plan, dict):
        return Plan(
            tool=plan.get("tool", intent.tool),
            action=plan.get("action", intent.action),
            target=plan.get("target", intent.target),
            command=plan.get("command", f"{intent.tool} {intent.action} {intent.target}")
        )

    return plan