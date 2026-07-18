import subprocess
from candor.core.result import Result

def run_plan(plan):
    """
    Execute a Plan object by spawning its command.
    Returns stdout, stderr, and exit code.
    """
    try:
        result = subprocess.run(
            plan.command if isinstance(plan.command, list) else plan.command.split(),
            capture_output=True,
            text=True,
            check=False
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": str(e),
            "exit_code": 1
        }

def execute_plan(plan):
    """
    Execute a unified Plan object.
    Handles subprocess execution, error capture, and wraps output in Result.
    """
    try:
        result = subprocess.run(
            plan.command,
            capture_output=True,
            text=True
        )
        return Result(
            stdout=result.stdout,
            stderr=result.stderr,
            status="success" if result.returncode == 0 else "error",
            tool=plan.tool,
            action=plan.action,
            target=plan.target
        )
    except Exception as e:
        return Result(
            stdout="",
            stderr=str(e),
            status="error",
            tool=plan.tool,
            action=plan.action,
            target=plan.target
        )