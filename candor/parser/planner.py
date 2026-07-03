from candor.modules import registry
from candor.core.intent import Intent
from candor.core.plan import Plan

def build_plan(intent: Intent) -> Plan:
    module = registry.get(intent.tool)
    if not module:
        raise ValueError(f"No module found for tool {intent.tool}")
    return module.build(intent)
