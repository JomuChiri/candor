def summarize_smbclient(output: str) -> dict:
    """
    Parse smbclient output and return structured summary.
    """
    summary = {"shares": []}

    for line in output.splitlines():
        if "Disk" in line or "Share" in line:
            summary["shares"].append(line.strip())

    return summary if summary["shares"] else {"message": "No shares found."}
