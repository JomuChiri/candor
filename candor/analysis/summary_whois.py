# candor/analysis/summary_whois.py
import re

def summarize_whois(raw_output: str) -> dict:
    """
    Parse WHOIS output into structured fields for reporting.
    Returns a dict with domain, registrar, created, expires, and nameservers.
    """
    summary = {}

    for line in raw_output.splitlines():
        line = line.strip()
        if line.startswith("Domain Name:"):
            summary["domain"] = line.split(":", 1)[1].strip()
        elif line.startswith("Registrar:"):
            summary["registrar"] = line.split(":", 1)[1].strip()
        elif line.startswith("Creation Date:"):
            summary["created"] = line.split(":", 1)[1].strip()
        elif "Expiry Date" in line or "Expiration Date" in line:
            summary["expires"] = line.split(":", 1)[1].strip()
        elif line.startswith("Name Server:"):
            ns = line.split(":", 1)[1].strip()
            summary.setdefault("nameservers", []).append(ns)

    return summary
