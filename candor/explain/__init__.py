# candor/explain/__init__.py

EXPLANATIONS = {
    "scan-fast": {
        "tool": "nmap",
        "command": "nmap -T4 -F",
        "purpose": "Quickly scans the most common ports to identify basic exposure.",
        "when_to_use": "Early in an investigation to get a fast overview.",
        "pros": ["Fast", "Low resource usage"],
        "cons": ["Limited coverage", "May miss uncommon ports"],
        "mitre": "Discovery"
    },
    "scan-service": {
        "tool": "nmap",
        "command": "nmap -sV",
        "purpose": "Attempts to identify services and versions running on open ports.",
        "when_to_use": "After finding open ports to understand what services are exposed.",
        "pros": ["Accurate service detection", "Useful for vulnerability mapping"],
        "cons": ["Slower than fast scans", "Can trigger IDS alerts"],
        "mitre": "Discovery"
    },
    "scan-os": {
        "tool": "nmap",
        "command": "nmap -O",
        "purpose": "Tries to determine the operating system of the target host.",
        "when_to_use": "When you need OS fingerprinting for attack surface analysis.",
        "pros": ["Provides OS context", "Helpful for tailoring exploits"],
        "cons": ["Not always accurate", "Requires root privileges"],
        "mitre": "Discovery"
    },
    "whois-lookup": {
        "tool": "whois",
        "command": "whois <domain>",
        "purpose": "Retrieves domain registration details.",
        "when_to_use": "At the start of an investigation to gather ownership and registrar info.",
        "pros": ["Simple", "Provides registrar and expiry data"],
        "cons": ["Limited security context", "Privacy-protected domains may hide details"],
        "mitre": "Reconnaissance"
    }
}

def explain(action: str) -> str:
    info = EXPLANATIONS.get(action)
    if not info:
        return f"No explanation available for {action}."
    lines = [
        f"[bold magenta]{info['tool']} — {action}[/]",
        f"Runs: {info['command']}",
        f"Purpose: {info['purpose']}",
        f"When to use: {info['when_to_use']}",
        f"Pros: {', '.join(info['pros'])}",
        f"Cons: {', '.join(info['cons'])}",
        f"MITRE ATT&CK: {info['mitre']}"
    ]
    return "\n".join(lines)
