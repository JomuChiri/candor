# candor/core/investigation_manager.py
from pathlib import Path
from candor.core.timeline import Timeline

def record_execution(intent, result, current_investigation):
    """
    Record execution details into investigation:
    - Save evidence file
    - Update timeline
    - Persist investigation state
    """
    if not current_investigation:
        return

    evidence_dir = f"candor/investigations/{intent.target}"
    Path(evidence_dir).mkdir(parents=True, exist_ok=True)
    evidence_file = f"{evidence_dir}/{intent.tool}-{intent.action}.txt"

    with open(evidence_file, "w") as f:
        f.write(result.stdout or "")

    current_investigation.add_command(
        f"{intent.tool}-{intent.action}",
        evidence_file,
        summary="..."
    )
    current_investigation.save()

    if not hasattr(current_investigation, "timeline"):
        current_investigation.timeline = Timeline(current_investigation.target)

    current_investigation.timeline.add_event(f"{intent.tool}-{intent.action}")
    current_investigation.timeline.save()
