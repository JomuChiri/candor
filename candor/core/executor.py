import subprocess

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
