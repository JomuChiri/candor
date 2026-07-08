# candor/core/mitre.py

MITRE_MAP = {
    "whois-lookup": "Reconnaissance",
    "dig-lookup": "Reconnaissance",
    "dnsrecon-basic": "Reconnaissance",
    "nmap-scan-fast": "Discovery",
    "nmap-scan-service": "Discovery",
    "nmap-scan-os": "Discovery",
    "smb-enum": "Discovery",
    "ldap-enum": "Discovery",
    "kerberos-enum": "Discovery",
    "ffuf": "Reconnaissance",
    "nikto": "Discovery",
    "sqlmap": "Execution",
    "bloodhound": "Privilege Escalation"
}

def map_to_mitre(action: str) -> str:
    return MITRE_MAP.get(action, "Unmapped")
