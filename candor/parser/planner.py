from candor.modules import registry

class Plan:
    def __init__(self, command):
        self.command = command

def build_plan(intent):
    module = registry.get(intent["tool"])
    if not module:
        raise ValueError(f"No module found for tool {intent['tool']}")
    return module.build(intent)
