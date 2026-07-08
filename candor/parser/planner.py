from candor.modules import registry
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.parser.intent import Intent

def build_plan(intent: Intent):
    """
    Build execution plan from intent.
    For v0.5, support high-level actions like 'enumerate' or 'investigate'.
    """
    module = registry.get(intent.tool)
    if intent.action in ["enumerate", "investigate"]:
        # Multi-step plan
        steps = [
            {"tool": "whois", "action": "lookup", "target": intent.target},
            {"tool": "dig", "action": "lookup", "target": intent.target},
            {"tool": "nmap", "action": "scan-fast", "target": intent.target},
            {"tool": "nmap", "action": "scan-service", "target": intent.target},
        ]
        return steps
        
    if not module:
        raise ValueError(f"No module found for tool {intent.tool}")
    return module.build(intent)

    # Default single-step plan
    return [{"tool": intent.tool, "action": intent.action, "target": intent.target}]


