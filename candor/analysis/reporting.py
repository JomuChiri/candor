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
    style = RISK_STYLE.get(analysis.risk.upper(), "white")
    findings = len(analysis.findings)
    recommendations = sum(len(f.recommendations) for f in analysis.findings)

    severity_counts = Counter(f.severity.lower() for f in analysis.findings)
    breakdown_lines = []
    for sev in ["critical", "high", "medium", "low", "informational"]:
        count = severity_counts.get(sev, 0)
        if count:
            sev_style, emoji = SEVERITY_STYLE.get(sev, ("white", "?"))
            breakdown_lines.append(f"[{sev_style}]{emoji} {sev.upper()}[/]: {count}")

    console.print(
        Panel.fit(
            "\n".join([
                f"Summary          : {analysis.summary}",
                f"Findings         : {findings}",
                f"Recommendations  : {recommendations}",
                f"Overall Risk     : [{style}]{analysis.risk}[/{style}]",
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
        style, emoji = SEVERITY_STYLE.get(finding.severity.lower(), ("white", "?"))
        severity = f"{emoji} {finding.severity.upper()}"
        table.add_row(
            finding.service,
            severity,
            finding.cve or "-",
            finding.description or "",
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

    counter = 1
    for phase in PHASE_ORDER:
        recs = grouped.get(phase, [])
        if not recs:
            continue
        table = Table(title=phase, header_style="bold cyan")
        table.add_column("#", width=3)
        table.add_column("Tool")
        table.add_column("Action")
        table.add_column("Confidence")
        table.add_column("Reason")
        table.add_column("Command")
        for rec in recs:
            table.add_row(
                str(counter),
                rec.tool,
                rec.action,
                _confidence_bar(rec.confidence),
                rec.reason,
                _build_command(rec),
            )
            counter += 1
        console.print(table)

# ---------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------

def render_analysis(analysis: AnalysisResult):
    console.print()
    render_summary(analysis)
    render_findings(analysis.findings)
    recommendations = []
    for finding in analysis.findings:
        recommendations.extend(finding.recommendations)
    render_recommendations(recommendations)
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
    style = RISK_STYLE.get(analysis.risk.upper(), "white")
    findings = len(analysis.findings)
    recommendations = sum(len(f.recommendations) for f in analysis.findings)

    severity_counts = Counter(f.severity.lower() for f in analysis.findings)
    breakdown_lines = []
    for sev in ["critical", "high", "medium", "low", "informational"]:
        count = severity_counts.get(sev, 0)
        if count:
            sev_style, emoji = SEVERITY_STYLE.get(sev, ("white", "?"))
            breakdown_lines.append(f"[{sev_style}]{emoji} {sev.upper()}[/]: {count}")

    console.print(
        Panel.fit(
            "\n".join([
                f"Summary          : {analysis.summary}",
                f"Findings         : {findings}",
                f"Recommendations  : {recommendations}",
                f"Overall Risk     : [{style}]{analysis.risk}[/{style}]",
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
        style, emoji = SEVERITY_STYLE.get(finding.severity.lower(), ("white", "?"))
        severity = f"{emoji} {finding.severity.upper()}"
        table.add_row(
            finding.service,
            severity,
            finding.cve or "-",
            finding.description or "",
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

    counter = 1
    for phase in PHASE_ORDER:
        recs = grouped.get(phase, [])
        if not recs:
            continue
        table = Table(title=phase, header_style="bold cyan")
        table.add_column("#", width=3)
        table.add_column("Tool")
        table.add_column("Action")
        table.add_column("Confidence")
        table.add_column("Reason")
        table.add_column("Command")
        for rec in recs:
            table.add_row(
                str(counter),
                rec.tool,
                rec.action,
                _confidence_bar(rec.confidence),
                rec.reason,
                _build_command(rec),
            )
            counter += 1
        console.print(table)

# ---------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------

def render_analysis(analysis: AnalysisResult):
    console.print()
    render_summary(analysis)
    render_findings(analysis.findings)
    recommendations = []
    for finding in analysis.findings:
        recommendations.extend(finding.recommendations)
    render_recommendations(recommendations)
