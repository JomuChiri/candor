# candor/parser/intent.py
from candor.core.intent import Intent

def parse_intent(query: str) -> Intent | None:
    words = query.strip().split()
    if not words:
        return None

    # Simple mappings for now
    if words[0] == "whois" and len(words) > 1:
        return Intent(tool="whois", target=words[1])

    if words[0] == "scan" and len(words) > 1:
        return Intent(tool="nmap", action="service_scan", target=words[1])

    if words[0] == "osdetect" and len(words) > 1:
        return Intent(tool="nmap", action="os_detection", target=words[1])

    return None
