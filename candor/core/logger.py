import os
import re
from datetime import date

def sanitize_filename(value: str) -> str:
    # Replace any character not alphanumeric, dash, or underscore
    return re.sub(r'[^A-Za-z0-9_\-]', '_', value)

def log_execution(job):
    log_dir = os.path.join("logs", date.today().isoformat())
    os.makedirs(log_dir, exist_ok=True)

    safe_target = sanitize_filename(job.intent.target)
    filename = f"{job.intent.tool}_{safe_target}.log"
    path = os.path.join(log_dir, filename)

    with open(path, "w") as f:
        f.write(f"Job #{job.id}\n")
        f.write(f"Tool: {job.intent.tool}\n")
        f.write(f"Action: {job.intent.action}\n")
        f.write(f"Target: {job.intent.target}\n")
        f.write(f"Exit Code: {job.result.returncode}\n")
        f.write(f"Duration: {job.result.elapsed:.2f}s\n")
        f.write("Output:\n")
        f.write(job.result.stdout)
        if job.result.stderr:
            f.write("\nErrors:\n")
            f.write(job.result.stderr)
