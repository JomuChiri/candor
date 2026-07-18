def summarize_impacket(output: str) -> dict:
    """
    Parse Impacket output and return structured summary.
    """
    summary = {"executions": [], "credentials": [], "secrets": []}

    for line in output.splitlines():
        if "Executed" in line or "Command" in line:
            summary["executions"].append(line.strip())
        elif "username" in line.lower() or "password" in line.lower():
            summary["credentials"].append(line.strip())
        elif "hash" in line.lower() or "NTLM" in line:
            summary["secrets"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No Impacket results found."}
