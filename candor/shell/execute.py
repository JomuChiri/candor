import subprocess
import time

from candor.core.result import ExecutionResult


def run_command(command_list: list[str], timeout: int = 60) -> ExecutionResult:
    start = time.time()

    try:
        result = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            shell=False,
        )

        elapsed = time.time() - start

        return ExecutionResult(
            returncode=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
            elapsed=elapsed,
        )

    except subprocess.TimeoutExpired as e:
        return ExecutionResult(
            returncode=-1,
            stdout="",
            stderr=f"Command timed out after {timeout} seconds.\n{e}",
            elapsed=time.time() - start,
        )

    except KeyboardInterrupt:
        return ExecutionResult(
            returncode=-1,
            stdout="",
            stderr="Execution interrupted by user.",
            elapsed=time.time() - start,
        )

    except FileNotFoundError as e:
        return ExecutionResult(
            returncode=-1,
            stdout="",
            stderr=f"Command not found: {e}",
            elapsed=time.time() - start,
        )

    except Exception as e:
        return ExecutionResult(
            returncode=-1,
            stdout="",
            stderr=str(e),
            elapsed=time.time() - start,
        )
