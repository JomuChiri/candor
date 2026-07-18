def summarize_searchsploit(output: str) -> dict:
    """
    Parse Searchsploit output and return structured summary.
    """
    summary = {"exploits": []}

    for line in output.splitlines():
        if line.strip() and not line.startswith("-----------"):
            summary["exploits"].append(line.strip())

    return summary if summary["exploits"] else {"message": "No exploits found."}
