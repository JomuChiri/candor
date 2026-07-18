def summarize_bloodhound(output: str) -> dict:
    """
    Parse BloodHound output and return structured summary.
    """
    summary = {"nodes": [], "edges": [], "critical_paths": []}

    for line in output.splitlines():
        if "Node" in line:
            summary["nodes"].append(line.strip())
        elif "Edge" in line:
            summary["edges"].append(line.strip())
        elif "Path" in line or "Shortest Path" in line:
            summary["critical_paths"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No BloodHound data parsed."}
