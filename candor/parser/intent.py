# candor/parser/intent.py
from candor.core.intent import Intent

def parse_intent(query: str):
    words = query.strip().split()
    if not words:
        return None

    if words[0] in ("whois", "lookup") and len(words) > 1:
        return Intent(tool="whois", target=words[1])

    if words[0] in ("scan", "nmap") and len(words) > 1:
        return Intent(tool="nmap", action="service_scan", target=words[1])

    if words[0] in ("osdetect", "os") and len(words) > 1:
        return Intent(tool="nmap", action="os_detection", target=words[1])

    return None
