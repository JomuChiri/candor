# candor/parser/natural_map.py

# Dictionary of phrases → canonical actions
NATURAL_MAP = {
    # Nmap
    "service detection": "scan-service",
    "detect services": "scan-service",
    "enumerate services": "scan-service",
    "os scan": "scan-os",
    "identify operating system": "scan-os",
    "ping host": "ping_scan",
    "is host reachable": "ping_scan",
    "aggressive scan": "scan-all",
    "scan aggressively": "scan-all",
    "udp scan": "scan-udp",
    "script scan": "scan-script",
    "scan-fast": "scan-fast",
    "fast scan": "scan-fast",
    "scan-os": "scan-os",
    "os detection": "scan-os",
    "scan-service": "scan-service",
    "service detection": "scan-service",

    # Whois
    "lookup domain": "lookup",
    "whois lookup": "lookup",
    "check registration": "lookup",
}
