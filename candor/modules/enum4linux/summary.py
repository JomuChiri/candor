def summarize_enum4linux(output: str) -> dict:
    """
    Parse enum4linux output and return structured summary.
    """
    summary = {"shares": [], "users": []}

    for line in output.splitlines():
        if "Disk" in line or "Share" in line:
            summary["shares"].append(line.strip())
        if "user:" in line.lower():
            summary["users"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No SMB information found."}
