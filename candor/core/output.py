# candor/core/output.py
from rich.console import Console
from candor.analysis.analyzer import analyze_services

console = Console()

# ---------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------

def heading(text: str, color="magenta"):
    console.print(f"\n[bold {color}]{text}[/]")
    console.print("────")

def success(msg: str):
    console.print(f"[bold green]✓ {msg}[/]")

def warning(msg: str):
    console.print(f"[bold yellow]⚠ {msg}[/]")

def error(msg: str):
    console.print(f"[bold red]✗ {msg}[/]")

def info(msg: str, color="blue"):
    console.print(f"[bold {color}]{msg}[/]")

def list_items(items, color="cyan"):
    for item in items:
        console.print(f"[bold {color}]-[/] {item}")

# ---------------------------------------------------------------------
# Raw output
# ---------------------------------------------------------------------

def show_raw_output(result, show=False):
    """
    Print raw stdout/stderr only if show=True.
    """
    if show and result.stdout:
        heading("Raw Output", color="blue")
        console.print(result.stdout)
    if show and result.stderr:
        heading("Errors", color="red")
        console.print(result.stderr)

# ---------------------------------------------------------------------
# Contextual suggestions
# ---------------------------------------------------------------------

def suggest_commands(analysis, target):
    suggestions = []

    for f in analysis["findings"]:
        recs = f.get("recommendations", [])
        for rec in recs:
            # Normalize into CLI-style commands
            if "nikto" in rec.lower():
                suggestions.append(f"nikto http://{target}")
            elif "gobuster" in rec.lower():
                suggestions.append(f"gobuster dir -u http://{target}")
            elif "enum4linux" in rec.lower():
                suggestions.append(f"enum4linux {target}")
            elif "smbclient" in rec.lower():
                suggestions.append(f"smbclient -L {target}")
            elif "searchsploit" in rec.lower():
                suggestions.append(rec)  # already CLI-ready
            elif "nuclei" in rec.lower():
                suggestions.append(f"nuclei -u http://{target}")
            else:
                suggestions.append(rec)

    # Deduplicate while preserving order
    seen = set()
    contextual = []
    for s in suggestions:
        if s not in seen:
            contextual.append(s)
            seen.add(s)

    return contextual

# ---------------------------------------------------------------------
# Analysis rendering
# ---------------------------------------------------------------------

def render_analysis(services, target):
    analysis = analyze_services(services, target)

    # Update state
    manager.set_target(target)
    manager.add_services(services)
    manager.add_findings(analysis["findings"])
    manager.set_risk(analysis["risk"])
    manager.mark_completed("Service Detection")
    
    heading("Summary")
    console.print(analysis["summary"])

    heading("Findings")
    if analysis["findings"]:
        for f in analysis["findings"]:
            console.print(f"• {f['service']} — {f['description']}")
            console.print(f"  Severity: {f['severity'].upper()}")
            if f.get("cve"):
                console.print(f"  CVE: {f['cve']}")
            if f.get("recommendations"):
                console.print("  Recommendations:")
                for rec in f["recommendations"]:
                    console.print(f"    - {rec}")
    else:
        console.print("• No enriched findings available")

    heading("Assessment")
    console.print(f"Overall Risk : {analysis['risk']}")

    contextual = suggest_commands(analysis, target)
    heading("Suggested Commands")
    if contextual:
        for i, cmd in enumerate(contextual, 1):
            console.print(f"{i}. {cmd}")
    else:
        console.print("• No contextual suggestions available")

