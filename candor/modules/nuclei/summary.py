def summarize_nuclei(output: str) -> dict:
    """
    Parse Nuclei output and return structured summary.
    """
    summary = {"findings": []}

    for line in output.splitlines():
        if "[info]" in line.lower() or "[critical]" in line.lower():
            summary["findings"].append(line.strip())

    return summary if summary["findings"] else {"message": "No vulnerabilities found."}
