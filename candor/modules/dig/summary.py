import re

def summarize_dig(output: str) -> dict:
    """
    Parse dig output and return structured summary.
    """
    summary = {"answers": [], "authority": [], "additional": []}

    section = None
    for line in output.splitlines():
        if line.startswith(";; ANSWER SECTION:"):
            section = "answers"
            continue
        elif line.startswith(";; AUTHORITY SECTION:"):
            section = "authority"
            continue
        elif line.startswith(";; ADDITIONAL SECTION:"):
            section = "additional"
            continue

        if section and line and not line.startswith(";;"):
            summary[section].append(line.strip())

    return summary if any(summary.values()) else {"message": "No DNS records found."}
