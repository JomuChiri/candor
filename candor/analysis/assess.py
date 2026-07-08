# candor/analysis/assess.py

def assess_ports(open_ports: list[int]) -> dict:
    """
    Interpret open ports into findings, risk level, and recommendations.
    Returns a dict with keys: assessment, risk, recommendations.
    """

    findings = []
    recommendations = []
    risk = "LOW"

    # Map common ports to findings + recommendations
    if 22 in open_ports:
        findings.append("SSH service available")
        recommendations.append("Ensure SSH is hardened (keys, MFA).")
        risk = escalate_risk(risk, "MEDIUM")

    if 3389 in open_ports:
        findings.append("Remote Desktop (RDP) exposed")
        recommendations.append("Restrict RDP access to trusted networks.")
        risk = escalate_risk(risk, "HIGH")

    if 445 in open_ports:
        findings.append("SMB service exposed")
        recommendations.append("Restrict SMB; verify firewall rules.")
        risk = escalate_risk(risk, "HIGH")

    if 80 in open_ports:
        findings.append("HTTP service detected")
        recommendations.append("Enforce HTTPS; redirect HTTP to HTTPS.")

    if 443 in open_ports:
        findings.append("HTTPS service detected")
        # No immediate recommendation unless misconfigured

    # Risk escalation based on breadth of exposure
    if len(open_ports) > 10 and risk != "HIGH":
        risk = "MEDIUM"

    # Defaults if nothing found
    if not findings:
        findings.append("No significant services detected")
    if not recommendations:
        recommendations.append("No immediate concerns.")

    return {
        "assessment": findings,
        "risk": risk,
        "recommendations": recommendations
    }


def escalate_risk(current: str, new: str) -> str:
    """
    Escalate risk level based on severity order.
    """
    levels = ["LOW", "MEDIUM", "HIGH"]
    return new if levels.index(new) > levels.index(current) else current
