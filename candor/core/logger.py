import os, datetime

def log_execution(intent, result):
    date = datetime.date.today().isoformat()
    log_dir = os.path.join("logs", date)
    os.makedirs(log_dir, exist_ok=True)

    filename = f"{intent.tool}_{intent.target}.log"
    path = os.path.join(log_dir, filename)

    with open(path, "w") as f:
        f.write(f"Tool: {intent.tool}\n")
        f.write(f"Target: {intent.target}\n")
        f.write(f"Action: {intent.action}\n")
        f.write(f"Exit Code: {result.returncode}\n")
        f.write(f"Duration: {result.elapsed:.2f}s\n")
        f.write("Output:\n")
        f.write(result.stdout)
        if result.stderr:
            f.write("\nErrors:\n")
            f.write(result.stderr)
