# candor/analysis/workflows.py

WORKFLOW_PHASES = {
    # Web stack
    "nikto": "Web Enumeration",
    "gobuster": "Web Enumeration",
    "nuclei": "Web Enumeration",
    "ffuf": "Web Enumeration",
    "sqlmap": "Web Exploitation",

    # SMB/Windows
    "enum4linux": "SMB Enumeration",
    "smbclient": "SMB Enumeration",
    "rpcclient": "SMB Enumeration",
    "netexec": "SMB Enumeration",
    "bloodhound": "Active Directory Mapping",

    # Exploit research
    "searchsploit": "Exploit Research",
    "metasploit": "Exploit Verification",

    # Network scanning
    "nmap": "Service Scanning",
    "masscan": "Service Scanning",

    # Databases
    "mysql": "Database Enumeration",
    "psql": "Database Enumeration",

    # Misc
    "dig": "DNS Enumeration",
    "dnsrecon": "DNS Enumeration",
    "showmount": "NFS Enumeration",
}

PHASE_ORDER = [
    "Service Scanning",
    "DNS Enumeration",
    "Web Enumeration",
    "SMB Enumeration",
    "Active Directory",
    "Database Enumeration",
    "Exploit Research",
    "Vulnerability Validation",
    "Exploitation",
    "General",
]
