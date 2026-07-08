# candor/modules/whois/summary.py
import re

def summarize_whois(output: str) -> str:
    """
    Parse raw WHOIS output into a structured summary.
    Extracts registrar, creation date, expiry date, and name servers.
    """
    registrar = None
    creation = None
    expiry = None
    name_servers = []

    for line in output.splitlines():
        line = line.strip()
        if line.lower().startswith("registrar:"):
            registrar = line.split(":", 1)[1].strip()
        elif re.search(r"creation date", line, re.IGNORECASE):
            creation = line.split(":", 1)[1].strip()
        elif re.search(r"expiry date|expiration date", line, re.IGNORECASE):
            expiry = line.split(":", 1)[1].strip()
        elif line.lower().startswith("name server:"):
            ns = line.split(":", 1)[1].strip()
            name_servers.append(ns)

    summary = []
    if registrar:
        summary.append(f"Registrar : {registrar}")
    if creation:
        summary.append(f"Created   : {creation}")
    if expiry:
        summary.append(f"Expires   : {expiry}")
    if name_servers:
        summary.append("Name Servers:")
        for ns in name_servers:
            summary.append(f"  - {ns}")

    return "\n".join(summary) if summary else "No summary available."
