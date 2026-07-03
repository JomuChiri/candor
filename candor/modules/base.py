class BaseModule:
    name = ""

    def build(self, intent):
        raise NotImplementedError

    def execute(self, plan):
        raise NotImplementedError
