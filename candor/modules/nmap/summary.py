# candor/modules/nmap/summary.py

import re

from candor.analysis.analyzer import (
    AnalysisResult,
    Finding,
    Recommendation,
)
from candor.analysis.attack_surface import (
    SERVICE_SIGNATURES,
    SURFACE_PORTS,
    WORKFLOWS,
    calculate_risk,
)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def build_workflow_recommendations(surfaces, target):

    recommendations = []

    recommendations.append(
        Recommendation(
            tool="nmap",
            action="scan-service",
            arguments={"target": target},
            confidence=0.95,
            reason="Identify versions running on exposed services.",
        )
    )

    for surface in sorted(surfaces):

        for tool, action in WORKFLOWS[surface]:

            recommendations.append(
                Recommendation(
                    tool=tool,
                    action=action,
                    arguments={"target": target},
                    confidence=0.85,
                    reason=f"{surface.upper()} attack surface detected.",
                )
            )

    return recommendations


# ---------------------------------------------------------------------
# Main summarizer
# ---------------------------------------------------------------------

def summarize_nmap(output: str) -> AnalysisResult:
    host = None
    findings = []
    detected_surfaces = set()

    for line in output.splitlines():
        if "scan report for" in line.lower():
            host = line.split("for", 1)[1].strip()
            continue

        match = re.match(r"(\d+)/(\w+)\s+open\s+(\S+)(.*)", line)
        if not match:
            continue

        port = int(match.group(1))
        proto = match.group(2)
        service = match.group(3)
        version = match.group(4).strip()

        signature = SERVICE_SIGNATURES.get(port, {"service": service, "severity": "medium"})

        findings.append(
            Finding(
                signature=f"{port}/{proto}",
                service=service,
                severity=signature["severity"],
                cve=None,
                description=f"Port {port}/{proto} open ({service} {version})".strip(),
                recommendations=[],
            )
        )

        for surface, ports in SURFACE_PORTS.items():
            if port in ports:
                detected_surfaces.add(surface)

    recommendations = build_workflow_recommendations(detected_surfaces, host)

    return AnalysisResult(
        summary=f"Discovered {len(findings)} open services on {host}.",
        findings=findings,
        recommendations=recommendations,
        risk=calculate_risk(findings),
        surfaces=list(detected_surfaces),
    )
