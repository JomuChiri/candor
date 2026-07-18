def summarize_dnsrecon(output: str) -> dict:
    """
    Parse dnsrecon output and return structured summary.
    """
    summary = {"records": [], "zone_transfers": []}

    for line in output.splitlines():
        if "A" in line or "MX" in line or "NS" in line:
            summary["records"].append(line.strip())
        if "AXFR" in line or "Zone Transfer" in line:
            summary["zone_transfers"].append(line.strip())

    return summary if any(summary.values()) else {"message": "No DNS records found."}
