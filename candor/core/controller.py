# candor/core/controller.py
from candor.commands import dispatch_builtin, execute

def run(query: str, console, current_investigation=None):
    """
    Central controller for CLI queries.
    Decides whether to run a built-in command or fallback to intent execution.
    """
    if dispatch_builtin(query, console, current_investigation):
        return

    # Fallback: execute intent
    execute.handle(query, console, current_investigation)
