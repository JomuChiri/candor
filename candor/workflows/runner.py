# candor/workflows/runner.py
from pathlib import Path
from candor.modules import registry
from candor.workflows import WORKFLOWS
from candor.workflows.parallel import run_parallel

def run_workflow(wf_name: str, target: str, current_investigation=None):
    """
    Run a sequential workflow by name against a target.
    Stores evidence if an investigation is active.
    """
    if wf_name not in WORKFLOWS:
        raise ValueError(f"No such workflow: {wf_name}")

    results = []
    for step in WORKFLOWS[wf_name]:
        step["target"] = target
        module = registry.get(step["tool"])
        result = module.execute(step)

        # Evidence storage
        if current_investigation:
            evidence_file = f"candor/investigations/{target}/{step['tool']}-{step['action']}.txt"
            Path(evidence_file).parent.mkdir(parents=True, exist_ok=True)
            with open(evidence_file, "w") as f:
                f.write(result.stdout or "")
            current_investigation.add_command(
                f"{step['tool']}-{step['action']}",
                evidence_file,
                summary="..."
            )
            current_investigation.save()

        results.append({
            "tool": step["tool"],
            "action": step["action"],
            "status": result.status
        })

    return results


def run_parallel_workflows(workflows: list, target: str, current_investigation=None):
    """
    Run multiple workflows in parallel against a target.
    Delegates to candor.workflows.parallel.run_parallel.
    """
    return run_parallel(workflows, target, current_investigation)
