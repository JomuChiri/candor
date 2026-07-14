from candor.modules.nmap.summary import summarize_nmap
from candor.modules.whois.summary import summarize_whois
from candor.analysis.assess import assess_ports
from candor.analysis.recommendations import explain_recommendation
from candor.analysis.confidence import score_confidence
from candor.core.findings import FindingsDB
from candor.analysis.summary_whois import summarize_whois

class AnalysisResult:
    def __init__(self, summary=None, findings=None, assessment=None,
                 recommendations=None, risk="Informational", confidence=None):
        self.summary = summary or {}
        self.findings = findings or []
        self.assessment = assessment or []
        self.recommendations = recommendations or []
        self.risk = risk
        self.confidence = confidence

def analyze(intent, result):
    """
    Run analysis pipeline based on tool output.
    Returns AnalysisResult with summary, findings, assessment,
    recommendations, risk, and confidence.
    """
    if intent.tool == "whois":
        summary = summarize_whois(result.stdout)
        return AnalysisResult(
            summary=summary,
            findings=["WHOIS record retrieved"],
            assessment=["Domain registration details parsed successfully."],
            risk="Informational",
            recommendations=[
                f"dig {intent.target}",
                f"nmap -F {intent.target}"
            ],
            confidence=90
        )

    if intent.tool == "nmap":
        summary = summarize_nmap(result.stdout)
        open_ports = summary.get("open_ports", [])

        assessment_data = assess_ports(open_ports)
        risk = assessment_data.get("risk", "LOW")

        # Map to human‑friendly severity
        severity_map = {"LOW": "Informational", "MEDIUM": "Medium", "HIGH": "High"}
        severity = severity_map.get(risk, "Informational")

        # Store findings
        db = FindingsDB()
        for f in assessment_data.get("assessment", []):
            db.add_finding(severity, f, f"{intent.tool}-{intent.action}", intent.target)

        # Explain recommendations
        explained_recs = [
            explain_recommendation(r) for r in assessment_data.get("recommendations", [])
        ]

        # Build analysis result
        analysis = AnalysisResult(
            summary=summary,
            findings=assessment_data.get("assessment", []),
            assessment=assessment_data.get("assessment", []),
            risk=severity,
            recommendations=explained_recs
        )

        # Add confidence score
        analysis.confidence = score_confidence(
            summary, analysis.findings, analysis.assessment
        )

        return analysis
