# candor/doctor.py
import shutil
import subprocess
from candor.modules import registry

def check_tool(tool: str) -> dict:
    """Return health info for a tool: presence, version, path."""
    result = {
        "installed": False,
        "path": None,
        "version": None,
    }

    path = shutil.which(tool)
    if not path:
        return result

    result["installed"] = True
    result["path"] = path

    try:
        proc = subprocess.run(
            [tool, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if proc.stdout:
            result["version"] = proc.stdout.strip().splitlines()[0]
        elif proc.stderr:
            result["version"] = proc.stderr.strip().splitlines()[0]
    except Exception:
        result["version"] = "Unknown"

    return result

def doctor(tool: str = None) -> dict:
    """Check health of all registered modules, or a specific one."""
    results = {}
    modules = registry.modules

    if tool:
        module = modules.get(tool)
        if module:
            results[module.name] = check_tool(module.name)
        else:
            results[tool] = {"installed": False, "path": None, "version": None}
    else:
        for module in modules.values():
            results[module.name] = check_tool(module.name)

    return results
