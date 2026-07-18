def summarize_netexec(output: str) -> dict:
    """
    Parse NetExec output and return structured summary.
    """
    summary = {"shares": [], "users": [], "auth_results": []}

    for line in output.splitlines():
        if "Share" in line:
            summary["shares"].append(line.strip())
        elif "User" in line or "username" in line.lower():
            summary["users"].append(line.strip())
        elif "Authentication" in line or "Login" in line:
            summary["auth_results"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No NetExec information found."}
