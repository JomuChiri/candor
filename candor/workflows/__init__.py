# candor/workflows/__init__.py

WORKFLOWS = {
    "web-enum": [
        {"tool": "whois", "action": "lookup"},
        {"tool": "dig", "action": "lookup"},
        {"tool": "dnsrecon", "action": "basic"},
        {"tool": "nmap", "action": "scan-fast"},
        {"tool": "nmap", "action": "scan-service"},
        {"tool": "http", "action": "check"},
    ],
    "network-recon": [
        {"tool": "whois", "action": "lookup"},
        {"tool": "nmap", "action": "scan-fast"},
        {"tool": "nmap", "action": "scan-os"},
    ],
    "host-enum": [
        {"tool": "nmap", "action": "scan-service"},
        {"tool": "nmap", "action": "scan-os"},
    ],
    "osint": [
        {"tool": "whois", "action": "lookup"},
        {"tool": "dig", "action": "lookup"},
        {"tool": "dnsrecon", "action": "basic"},
    ]
}
