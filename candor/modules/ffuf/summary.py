def summarize_ffuf(output: str) -> dict:
    """
    Parse ffuf output and return structured summary.
    """
    summary = {"hits": []}

    for line in output.splitlines():
        if "Status:" in line and "Size:" in line:
            summary["hits"].append(line.strip())

    return summary if summary["hits"] else {"message": "No fuzzing results found."}
