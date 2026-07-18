# candor/analysis/attack_surface.py

# ---------------------------------------------------------------------
# Service signatures
# ---------------------------------------------------------------------

SERVICE_SIGNATURES = {
    21:  {"service": "ftp",           "severity": "high"},
    22:  {"service": "ssh",           "severity": "medium"},
    23:  {"service": "telnet",        "severity": "critical"},
    25:  {"service": "smtp",          "severity": "high"},
    53:  {"service": "dns",           "severity": "medium"},
    80:  {"service": "http",          "severity": "medium"},
    139: {"service": "netbios-ssn",   "severity": "medium"},
    445: {"service": "microsoft-ds",  "severity": "medium"},
    512: {"service": "exec",          "severity": "critical"},
    513: {"service": "login",         "severity": "critical"},
    514: {"service": "shell",         "severity": "critical"},
    1524:{"service": "ingreslock",    "severity": "critical"},
    2049:{"service": "nfs",           "severity": "medium"},
    3306:{"service": "mysql",         "severity": "medium"},
    5432:{"service": "postgresql",    "severity": "medium"},
    88:  {"service": "kerberos",      "severity": "high"},
    389: {"service": "ldap",          "severity": "high"},
    636: {"service": "ldaps",         "severity": "high"},
}

# ---------------------------------------------------------------------
# Investigation workflows
# ---------------------------------------------------------------------

WORKFLOWS = {
    "http": [
        ("nikto", "scan"),
        ("nuclei", "scan"),
        ("gobuster", "dir"),
        ("ffuf", "content"),
    ],

    "smb": [
        ("enum4linux", "scan"),
        ("rpcclient", "enum"),
        ("smbclient", "list"),
        ("netexec", "smb"),
    ],

    "dns": [
        ("dig", "lookup"),
        ("dnsrecon", "scan"),
    ],

    "database": [
        ("nmap", "scan-service"),
        ("searchsploit", "search"),
    ],

    "kerberos": [
        ("impacket", "getTGT"),
        ("impacket", "kerbrute"),
        ("netexec", "kerberos"),
    ],

    "ldap": [
        ("ldapsearch", "enum"),
        ("netexec", "ldap"),
        ("bloodhound", "ingest"),
    ],
}

# ---------------------------------------------------------------------
# Attack surface mapping
# ---------------------------------------------------------------------

SURFACE_PORTS = {
    "http": {80, 443, 8009, 8180},
    "smb": {139, 445},
    "dns": {53},
    "database": {3306, 5432},
    "kerberos": {88},
    "ldap": {389, 636},
}

# ---------------------------------------------------------------------
# Risk scoring
# ---------------------------------------------------------------------

def calculate_risk(findings) -> str:
    """
    Calculate overall risk score from a list of Finding-like objects.
    Each finding must have a .severity attribute.
    """

    score = 0
    weights = {
        "critical": 10,
        "high": 6,
        "medium": 3,
        "low": 1,
        "informational": 0,
    }

    for f in findings:
        sev = getattr(f, "severity", "informational").lower()
        score += weights.get(sev, 0)

    if score >= 40:
        return "CRITICAL"
    if score >= 20:
        return "HIGH"
    if score >= 10:
        return "MEDIUM"
    return "LOW"
