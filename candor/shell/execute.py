import subprocess, time
from candor.core.result import ExecutionResult

def run_command(command_list: list[str], timeout: int = 60) -> ExecutionResult:
    start = time.time()
    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False  # safer
        )
        elapsed = time.time() - start
        return ExecutionResult(
            success=(result.returncode == 0),
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            elapsed=elapsed
        )
    except subprocess.TimeoutExpired as e:
        return ExecutionResult(False, "", str(e), -1, time.time() - start)
    except KeyboardInterrupt:
        return ExecutionResult(False, "", "Interrupted by user", -1, time.time() - start)
