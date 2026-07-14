# candor/commands/__init__.py

def get_commands():
    # Import inside the function to avoid circular imports
    from candor.commands import (
        help, jobs, doctor, report, workflow,
        findings, explain, metadata, case
    )
    return [help, jobs, doctor, report, workflow, findings, explain, metadata, case]

def dispatch_builtin(query: str, console, current_investigation=None) -> bool:
    for cmd in get_commands():
        if cmd.matches(query):
            cmd.handle(query, console, current_investigation)
            return True
    return False

def dispatch_execute(query: str, console, current_investigation=None):
    from candor.commands import execute
    execute.handle(query, console, current_investigation)
