# candor/core/investigation_manager.py
from pathlib import Path
from candor.core.timeline import Timeline

class Investigation:
    """
    Stateful investigation object.
    Tracks target, services, findings, risk, and completed actions.
    """

    def __init__(self, target):
        self.target = target
        self.services = []
        self.findings = []
        self.completed = []
        self.risk = "INFORMATIONAL"
        self.timeline = Timeline(target)

    def add_services(self, services):
        self.services.extend(services)

    def add_findings(self, findings):
        self.findings.extend(findings)

    def set_risk(self, risk):
        self.risk = risk

    def mark_completed(self, action):
        if action not in self.completed:
            self.completed.append(action)

    def add_command(self, command, evidence_file, summary=""):
        self.timeline.add_event(command)
        # Could also store evidence references here
        self.completed.append(command)

    def save(self):
        # Persist investigation state (JSON, DB, etc.)
        state_file = Path(f"candor/investigations/{self.target}/state.json")
        state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(state_file, "w") as f:
            f.write(str({
                "target": self.target,
                "services": self.services,
                "findings": self.findings,
                "risk": self.risk,
                "completed": self.completed
            }))

    def summarize(self):
        return {
            "Target": self.target,
            "Services": len(self.services),
            "Risk": self.risk,
            "Critical Findings": [
                f for f in self.findings if f.get("severity") in ("high", "critical")
            ],
            "Completed": self.completed
        }

# ---------------------------------------------------------------------
# Evidence + timeline recording
# ---------------------------------------------------------------------

def record_execution(intent, result, current_investigation):
    """
    Record execution details into investigation:
    - Save evidence file
    - Update timeline
    - Persist investigation state
    """
    if not current_investigation:
        return

    evidence_dir = Path(f"candor/investigations/{intent.target}")
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_file = evidence_dir / f"{intent.tool}-{intent.action}.txt"

    with open(evidence_file, "w") as f:
        f.write(result.stdout or "")

    current_investigation.add_command(
        f"{intent.tool}-{intent.action}",
        str(evidence_file),
        summary="..."
    )
    current_investigation.save()
    current_investigation.timeline.save()
