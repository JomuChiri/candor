import subprocess
import signal

def run_command(command: str, timeout: int = 60):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout if result.stdout else result.stderr
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds"
    except KeyboardInterrupt:
        return "Execution interrupted by user"
    except Exception as e:
        return str(e)
