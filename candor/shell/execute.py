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
            shell=False
        )
        elapsed = time.time() - start

        # Decide status
        if result.returncode == 0:
            if result.stderr.strip():
                status = "warning"
            else:
                status = "success"
        else:
            status = "failure"

        return ExecutionResult(
            success=(result.returncode == 0),
            stdout=result.stdout,
            stderr=result.stderr,
            returncode=result.returncode,
            elapsed=elapsed,
            status=status
        )

    except subprocess.TimeoutExpired as e:
        return ExecutionResult(False, "", str(e), -1, time.time() - start, status="failure")
    except KeyboardInterrupt:
        return ExecutionResult(False, "", "Interrupted by user", -1, time.time() - start, status="failure")
