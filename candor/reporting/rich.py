# candor/reporting/rich.py
import json
from pathlib import Path
from candor.analysis.recommendations import explain_recommendation
from candor.core.findings import FindingsDB

def generate_report(target: str, fmt: str = "markdown") -> str:
    """
    Generate a rich investigation report from metadata + findings.
    fmt = "markdown" or "html"
    Returns path to saved report.
    """
    base_dir = Path("candor/investigations") / target
    metadata_file = base_dir / "metadata.json"

    if not metadata_file.exists():
        raise FileNotFoundError(f"No investigation metadata for {target}")

    with open(metadata_file) as f:
        meta = json.load(f)

    # Findings DB
    db = FindingsDB()
    findings = db.list_findings()

    # Sections
    executive_summary = f"Investigation of {meta['target']} (started {meta['start_time']})"
    scope = f"Target: {meta['target']} | Resolved IP: {meta.get('resolved_ip','N/A')}"
    commands = "\n".join([f"- {cmd}" for cmd in meta.get("commands_run", [])])

    # Findings section
    findings_section = ""
    for severity, items in findings.items():
        findings_section += f"\n### {severity}\n"
        for item in items:
            findings_section += (
                f"- {item['description']} "
                f"(Target: {item['target']}, Source: {item['source']}, MITRE: {item['mitre']})\n"
            )

    # Recommendations with explanations
    recommendations_section = ""
    for rec in meta.get("assessment", {}).get("recommendations", []):
        recommendations_section += explain_recommendation(rec) + "\n"

    # Timeline
    timeline_file = base_dir / "timeline.json"
    if timeline_file.exists():
        with open(timeline_file) as f:
            timeline_data = json.load(f)
        timeline_section = "\n".join([f"- {e['time']} {e['action']}" for e in timeline_data])
    else:
        timeline_section = "No timeline recorded."

    # Markdown template
    report_md = f"""
# Candor Investigation Report

## Executive Summary
{executive_summary}

## Scope
{scope}

## Commands Executed
{commands}

## Findings
{findings_section}

## Recommendations
{recommendations_section}

## Timeline
{timeline_section}

## Evidence
See candor/investigations/{target}/ for raw outputs.
"""

    # Save
    path = base_dir / ("report.md" if fmt == "markdown" else "report.html")
    if fmt == "markdown":
        path.write_text(report_md)
    else:
        path.write_text(f"<html><body><pre>{report_md}</pre></body></html>")
    return str(path)
