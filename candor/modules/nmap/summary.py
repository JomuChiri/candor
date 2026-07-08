# candor/modules/nmap/summary.py
import re

def summarize_nmap(output: str) -> dict:
    """
    Parse Nmap output and return structured summary.
    """
    summary = {"host": None, "open_ports": [], "elapsed": None}

    for line in output.splitlines():
        if "scan report for" in line.lower():
            summary["host"] = line.split("for")[-1].strip()
        if re.search(r"\d+/tcp\s+open", line):
            parts = line.split()
            port_proto = parts[0]   # e.g. "80/tcp"
            service = parts[-1]     # e.g. "http"
            summary["open_ports"].append(f"{port_proto} {service.upper()}")
        if "Nmap done:" in line:
            summary["elapsed"] = line.split(" in ")[-1].strip()

    return summary if any(summary.values()) else {"message": "No summary available."}
