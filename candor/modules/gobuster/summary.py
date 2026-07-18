def summarize_gobuster(output: str) -> dict:
    """
    Parse Gobuster output and return structured summary.
    """
    summary = {"found_paths": []}

    for line in output.splitlines():
        if line.startswith("/"):
            summary["found_paths"].append(line.strip())

    return summary if summary["found_paths"] else {"message": "No directories found."}
