# candor/analysis/recommendations.py

EXPLANATIONS = {
    "Restrict RDP access to trusted networks.": {
        "why": "RDP (port 3389) is a common target for brute-force and ransomware campaigns.",
        "impact": "Exposed RDP can allow attackers remote control of systems.",
        "mitre": "Initial Access"
    },
    "Restrict SMB; verify firewall rules.": {
        "why": "SMB (port 445) is often exploited for lateral movement and worm propagation (e.g., WannaCry).",
        "impact": "Unrestricted SMB can allow credential theft and remote code execution.",
        "mitre": "Lateral Movement"
    },
    "Ensure SSH is hardened (keys, MFA).": {
        "why": "SSH (port 22) is secure by design but vulnerable to weak passwords and brute-force attacks.",
        "impact": "Compromised SSH can give attackers full system access.",
        "mitre": "Initial Access"
    },
    "Enforce HTTPS; redirect HTTP to HTTPS.": {
        "why": "Plain HTTP exposes traffic to interception and manipulation.",
        "impact": "Attackers can perform man-in-the-middle attacks or inject malicious content.",
        "mitre": "Collection"
    }
}

def explain_recommendation(rec: str) -> str:
    info = EXPLANATIONS.get(rec)
    if not info:
        return f"- {rec} (No detailed explanation available)"
    return (
        f"- {rec}\n"
        f"   Why: {info['why']}\n"
        f"   Impact: {info['impact']}\n"
        f"   MITRE ATT&CK: {info['mitre']}"
    )
