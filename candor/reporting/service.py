# candor/reporting/service.py
import json
from pathlib import Path
from candor.reporting.rich import generate_report
from candor.core.case import Case

def generate_investigation_report(target: str, fmt: str = "markdown") -> str:
    """
    Generate a report for a single investigation target.
    Delegates to candor.reporting.rich.generate_report.
    Returns the path to the generated report file.
    """
    return generate_report(target, fmt=fmt)


def generate_case_report(case_name: str, fmt: str = "markdown") -> str:
    """
    Generate a consolidated report across all investigations in a case.
    Iterates through investigations, collects metadata, and writes a combined report.
    """
    case = Case(case_name)
    investigations = case.list_investigations()

    if not investigations:
        raise ValueError(f"No investigations found in case {case_name}")

    report_dir = Path(f"candor/cases/{case_name}")
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"case_report.{ 'html' if fmt == 'html' else 'md' }"

    consolidated = {
        "case": case_name,
        "investigations": []
    }

    for target in investigations:
        try:
            inv_report = generate_report(target, fmt="markdown")  # always generate markdown internally
            with open(inv_report) as f:
                consolidated["investigations"].append({
                    "target": target,
                    "report": f.read()
                })
        except Exception as e:
            consolidated["investigations"].append({
                "target": target,
                "error": str(e)
            })

    # Save consolidated case report
    with open(report_file, "w") as f:
        if fmt == "html":
            # very simple HTML wrapper
            f.write("<html><body>")
            f.write(f"<h1>Case Report: {case_name}</h1>")
            for inv in consolidated["investigations"]:
                f.write(f"<h2>{inv['target']}</h2>")
                if "report" in inv:
                    f.write(f"<pre>{inv['report']}</pre>")
                else:
                    f.write(f"<p>Error: {inv['error']}</p>")
            f.write("</body></html>")
        else:
            # markdown
            f.write(f"# Case Report: {case_name}\n\n")
            for inv in consolidated["investigations"]:
                f.write(f"## {inv['target']}\n")
                if "report" in inv:
                    f.write(inv["report"])
                else:
                    f.write(f"Error: {inv['error']}\n")

    return str(report_file)
