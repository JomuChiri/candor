# candor/analysis/reporting.py
from rich.table import Table
from rich.console import Console
from candor.analysis.pipeline import AnalysisResult

console = Console()

def render_summary(summary: dict):
    console.print("\n[bold magenta]Summary[/]")
    console.print("────")

    table = Table(show_header=False)
    table.add_row("Target", summary.get("target", ""))
    table.add_row("Host", summary.get("host", ""))
    table.add_row("Duration", summary.get("elapsed", ""))
    console.print(table)

    if summary.get("open_ports"):
        svc_table = Table(title="Open Services")
        svc_table.add_column("Port")
        svc_table.add_column("Service")
        svc_table.add_column("State")
        for port in summary["open_ports"]:
            parts = port.split()
            if len(parts) >= 3:
                svc_table.add_row(parts[0], parts[2], parts[1])
            elif len(parts) == 2:
                svc_table.add_row(parts[0], parts[1], "open")
        console.print(svc_table)


def render_findings(findings: list):
    console.print("\n[bold magenta]Findings[/]")
    console.print("────")
    for f in findings:
        console.print(f"• {f}")


def render_assessment(assessment: list, risk: str, confidence: int = None):
    console.print("\n[bold magenta]Assessment[/]")
    console.print("────")
    for line in assessment:
        console.print(line)
    console.print(f"\nOverall Risk : {risk.upper()}")
    if confidence is not None:
        console.print(f"Confidence   : {confidence}%")


def render_next_steps(steps: list):
    console.print("\n[bold magenta]Recommended Next Steps[/]")
    console.print("────")
    for i, step in enumerate(steps, 1):
        console.print(f"{i}. {step}")

def render_analysis(analysis: AnalysisResult):
    console.print("\nSummary\n────")
    if isinstance(analysis.summary, dict) and analysis.summary:
        for key, value in analysis.summary.items():
            if isinstance(value, list):
                console.print(f"{key.title():<12}: {', '.join(value)}")
            else:
                console.print(f"{key.title():<12}: {value}")
    elif isinstance(analysis.summary, str):
        console.print("[dim]Raw WHOIS output[/]")
    else:
        console.print("[dim]No summary available[/]")

    if analysis.findings:
        render_findings(analysis.findings)
    if analysis.assessment:
        render_assessment(analysis.assessment, analysis.risk, getattr(analysis, "confidence", None))
    if analysis.recommendations:
        render_next_steps(analysis.recommendations)
