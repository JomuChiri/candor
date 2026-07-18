def summarize_rpcclient(output: str) -> dict:
    """
    Parse rpcclient output and return structured summary.
    """
    summary = {"users": [], "groups": [], "domains": []}

    for line in output.splitlines():
        if "user:" in line.lower():
            summary["users"].append(line.strip())
        elif "group:" in line.lower():
            summary["groups"].append(line.strip())
        elif "domain:" in line.lower():
            summary["domains"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No RPC information found."}
