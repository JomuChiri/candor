#candor/analysis/reporting.py
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from collections import defaultdict, Counter

from candor.analysis.analyzer import AnalysisResult, Finding, Recommendation
from candor.analysis.workflows import WORKFLOW_PHASES, PHASE_ORDER

console = Console()

# ---------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------

SEVERITY_STYLE = {
    "informational": ("dim", "ℹ"),
    "low": ("green", "🟢"),
    "medium": ("yellow", "🟡"),
    "high": ("orange1", "⚠"),
    "critical": ("bold red", "🔴"),
}

RISK_STYLE = {
    "INFORMATIONAL": "dim",
    "LOW": "green",
    "MEDIUM": "yellow",
    "HIGH": "orange1",
    "CRITICAL": "bold red",
}

WORKFLOW_PHASES = {
    "nmap": "Service Detection",
    "enum4linux": "SMB Enumeration",
    "smbclient": "SMB Enumeration",
    "rpcclient": "SMB Enumeration",
    "netexec": "Lateral Movement",
    "nikto": "Web Enumeration",
    "nuclei": "Web Enumeration",
    "gobuster": "Web Enumeration",
    "ffuf": "Web Enumeration",
    "dig": "DNS Enumeration",
    "dnsrecon": "DNS Enumeration",
    "ldapsearch": "LDAP Enumeration",
    "bloodhound": "AD Enumeration",
    "impacket": "Kerberos",
    # fallback
}

PHASE_ORDER = [
    "Service Detection",
    "SMB Enumeration",
    "Web Enumeration",
    "DNS Enumeration",
    "Database Enumeration",
    "LDAP Enumeration",
    "Kerberos",
    "AD Enumeration",
    "Lateral Movement",
    "General",
]

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def _confidence_bar(confidence: float) -> str:
    confidence = max(0.0, min(confidence, 1.0))
    filled = int(confidence * 10)
    return "█" * filled + "░" * (10 - filled) + f" {int(confidence*100)}%"

def _recommendation_key(rec: Recommendation):
    return (rec.tool, rec.action, tuple(sorted(rec.arguments.items())))

def _deduplicate(recommendations: list[Recommendation]) -> list[Recommendation]:
    unique = {}
    for rec in recommendations:
        key = _recommendation_key(rec)
        if key not in unique:
            unique[key] = rec
            continue
        existing = unique[key]
        existing.confidence = max(existing.confidence, rec.confidence)
        if rec.reason and rec.reason not in existing.reason:
            existing.reason += f"; {rec.reason}"
    return sorted(unique.values(), key=lambda r: r.confidence, reverse=True)

def _build_command(rec: Recommendation):
    args = [f"{key}={value}" for key, value in rec.arguments.items()]
    return f"{rec.tool} {rec.action} {' '.join(args)}".strip()

# ---------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------

def render_summary(analysis: AnalysisResult):
    style = RISK_STYLE.get(getattr(analysis, "risk", "INFORMATIONAL").upper(), "white")

    # FIX: count findings properly
    findings_count = len(analysis.findings) if analysis.findings else 0

    # FIX: count recommendations safely
    recommendations_count = 0
    for f in analysis.findings:
        if hasattr(f, "recommendations"):
            recommendations_count += len(analysis.recommendations) if analysis.recommendations else 0

    severity_counts = Counter(
        getattr(f, "severity", "informational").lower() for f in analysis.findings
    )
    breakdown_lines = []
    for sev in ["critical", "high", "medium", "low", "informational"]:
        count = severity_counts.get(sev, 0)
        if count:
            sev_style, emoji = SEVERITY_STYLE.get(sev, ("white", "?"))
            breakdown_lines.append(f"[{sev_style}]{emoji} {sev.upper()}[/]: {count}")

    # NEW: surfaces line
    detected_surfaces = getattr(analysis, "surfaces", [])
    if detected_surfaces:
        surface_badges = ", ".join(
            f"[cyan]{s.upper()}[/]" for s in detected_surfaces
        )
        surfaces_line = f"Detected Surfaces : {surface_badges}"
    else:
        surfaces_line = "Detected Surfaces : None"

    console.print(
        Panel.fit(
            "\n".join([
                f"Summary          : {analysis.summary}",
                f"Findings         : {findings_count}",
                f"Recommendations  : {recommendations_count}",
                f"Overall Risk     : [{style}]{getattr(analysis, 'risk', 'INFORMATIONAL')}[/{style}]",
                surfaces_line,
                "",
                "Severity Breakdown:",
                *breakdown_lines,
            ]),
            title="Analysis Summary",
        )
    )

# ---------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------

def render_findings(findings: list[Finding]):
    if not findings:
        return
    table = Table(title="Findings", header_style="bold cyan")
    table.add_column("Service")
    table.add_column("Severity")
    table.add_column("CVE")
    table.add_column("Description")
    for finding in findings:
        style, emoji = SEVERITY_STYLE.get(getattr(finding, "severity", "informational").lower(), ("white", "?"))
        severity = f"{emoji} {getattr(finding, 'severity', 'INFORMATIONAL').upper()}"
        table.add_row(
            getattr(finding, "service", "-"),
            severity,
            getattr(finding, "cve", "-"),
            getattr(finding, "description", ""),
            style=style,
        )
    console.print(table)

# ---------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------

def render_recommendations(recommendations: list[Recommendation]):
    recommendations = _deduplicate(recommendations)
    if not recommendations:
        return

    grouped = defaultdict(list)
    for rec in recommendations:
        category = WORKFLOW_PHASES.get(rec.tool, "General")
        grouped[category].append(rec)

    for phase in PHASE_ORDER:
        recs = grouped.get(phase, [])
        if not recs:
            continue
        table = Table(title=f"{phase} Recommendations", header_style="bold cyan")
        table.add_column("Tool")
        table.add_column("Action")
        table.add_column("Confidence")
        table.add_column("Reason")
        table.add_column("Command")
        for rec in recs:
            table.add_row(
                rec.tool,
                rec.action,
                _confidence_bar(rec.confidence),
                rec.reason,
                _build_command(rec),
            )
        console.print(table)

def render_next_step(analysis: AnalysisResult):
    if not analysis.recommendations:
        return
    primary = analysis.recommendations[0]
    console.print(
        Panel.fit(
            f"[bold green]Next Investigation[/]\n\n"
            f"Suggested command:\n"
            f"candor> {primary.tool} {primary.action} {primary.arguments.get('target','')}\n\n"
            f"Reason:\n{primary.reason}",
            title="Primary Recommendation",
        )
    )

# ---------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------

def render_analysis(analysis: AnalysisResult):
    console.print()
    render_summary(analysis)
    render_findings(analysis.findings)

    # FIX: include both per-finding and top-level recommendations
    recommendations = []
    if getattr(analysis, "recommendations", None):
        recommendations.extend(analysis.recommendations)
    for f in analysis.findings:
        if hasattr(f, "recommendations") and f.recommendations:
            recommendations.extend(f.recommendations)

    render_recommendations(recommendations)

