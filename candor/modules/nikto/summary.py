import re

def summarize_nikto(output: str) -> dict:
    """
    Parse Nikto output and return structured summary.
    """
    summary = {"host": None, "issues": []}

    for line in output.splitlines():
        if "Target IP" in line or "Target Hostname" in line:
            summary["host"] = line.split(":")[-1].strip()
        if re.search(r"OSVDB|CVE", line):
            summary["issues"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No summary available."}
