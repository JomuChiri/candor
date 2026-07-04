# candor/reporting.py
import os
from candor.core.result import ExecutionResult
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.history import load_job

REPORTS_DIR = os.path.expanduser("~/.candor/reports")

def ensure_reports_dir():
    os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_markdown(job) -> str:
    intent: Intent = job.intent
    plan: Plan = job.plan
    result: ExecutionResult = job.result

    md = []
    md.append(f"# Candor Report — Job {job.id}")
    md.append("")
    md.append("## Plan")
    md.append(f"- Tool: {intent.tool}")
    md.append(f"- Action: {intent.action}")
    md.append(f"- Target: {intent.target}")
    md.append(f"- Command: {' '.join(plan.command)}")
    md.append("")
    md.append("## Result")
    md.append(f"- Status: {result.status}")
    md.append(f"- Exit Code: {result.returncode}")
    md.append(f"- Duration: {result.elapsed:.2f}s")
    md.append("")
    if result.stdout:
        md.append("### Output")
        md.append("```")
        md.append(result.stdout)
        md.append("```")
    if result.stderr:
        md.append("### Errors")
        md.append("```")
        md.append(result.stderr)
        md.append("```")
    return "\n".join(md)

def generate_html(job) -> str:
    md = generate_markdown(job)
    # Simple conversion: wrap in <pre> for now
    return f"<html><body><pre>{md}</pre></body></html>"

def save_report(job, fmt="markdown") -> str:
    ensure_reports_dir()
    filename = os.path.join(REPORTS_DIR, f"job_{job.id}.{ 'md' if fmt=='markdown' else 'html'}")
    content = generate_markdown(job) if fmt == "markdown" else generate_html(job)
    with open(filename, "w") as f:
        f.write(content)
    return filename
