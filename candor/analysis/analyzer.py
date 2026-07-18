from dataclasses import dataclass, field
from typing import Dict, List

from candor.analysis.signatures import (
    SERVICE_SIGNATURES,
    VULNERABILITY_SIGNATURES,
    SEVERITY_SCORE,
)

# ----------------------------------------------------------------------
# Models
# ----------------------------------------------------------------------

@dataclass(slots=True)
class Recommendation:
    tool: str
    action: str
    arguments: Dict[str, str]
    reason: str = ""
    confidence: float = 1.0


@dataclass(slots=True)
class Finding:
    signature: str
    service: str
    severity: str
    description: str | None = None
    cve: str | None = None
    recommendations: List[Recommendation] = field(default_factory=list)


@dataclass(slots=True)
class AnalysisResult:
    summary: str
    findings: List[Finding]
    risk: str


# ----------------------------------------------------------------------
# Internal helpers
# ----------------------------------------------------------------------

_SCORE_TO_RISK = {
    0: "INFORMATIONAL",
    1: "LOW",
    2: "MEDIUM",
    3: "HIGH",
    4: "CRITICAL",
}


def _build_recommendations(meta: dict, target: str | None) -> List[Recommendation]:
    recommendations = []

    for item in meta.get("recommendations", []):

        args = {
            key: (
                target if value == "{target}" else
                service if value == "{service}" else
                signature if value == "{version}" else
                value
            )
            for key, value in item.get("arguments", {}).items()
        }

        recommendations.append(
            Recommendation(
                tool=item["tool"],
                action=item["action"],
                arguments=args,
                reason=item.get("reason", ""),
                confidence=item.get("confidence", 1.0),
            )
        )

    return recommendations


def _match_signature(service: str):
    """
    Yield every matching service/vulnerability signature.
    """

    text = service.lower()

    for database in (SERVICE_SIGNATURES, VULNERABILITY_SIGNATURES):
        for signature, meta in database.items():
            if signature.lower() in text:
                yield signature, meta


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------

def analyze_services(services: List[str], target: str |None = None) -> AnalysisResult:
    findings: List[Finding] = []
    highest_score = 0

    for service in services:

        for signature, meta in _match_signature(service):

            severity = meta.get("severity", "informational")
            highest_score = max(
                highest_score,
                SEVERITY_SCORE.get(severity, 0),
            )

            findings.append(
                Finding(
                    signature=signature,
                    service=service,
                    severity=severity,
                    description=meta.get("description"),
                    cve=meta.get("cve"),
                    recommendations=_build_recommendations(meta, target),
                )
            )

    return AnalysisResult(
        summary=f"{len(services)} services analyzed",
        findings=findings,
        risk=_SCORE_TO_RISK[highest_score],
    )