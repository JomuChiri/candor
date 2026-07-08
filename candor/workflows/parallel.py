# candor/workflows/parallel.py
from candor.workflows import WORKFLOWS
from candor.modules import registry
from candor.core.findings import FindingsDB
from pathlib import Path

def run_parallel(workflows: list[str], target: str, investigation):
    """
    Execute multiple workflows in parallel and merge results.
    """
    results = {}

    for wf_name in workflows:
        if wf_name not in WORKFLOWS:
            results[wf_name] = {"error": f"No such workflow: {wf_name}"}
            continue

        wf_results = []
        for step in WORKFLOWS[wf_name]:
            step["target"] = target
            module = registry.get(step["tool"])
            result = module.execute(step)

            # Evidence storage
            evidence_file = f"candor/investigations/{target}/{step['tool']}-{step['action']}.txt"
            Path(evidence_file).parent.mkdir(parents=True, exist_ok=True)
            with open(evidence_file, "w") as f:
                f.write(result.stdout or "")
            investigation.add_command(f"{step['tool']}-{step['action']}", evidence_file, summary="...")
            investigation.save()

            wf_results.append({
                "tool": step["tool"],
                "action": step["action"],
                "status": result.status
            })

        results[wf_name] = wf_results

    return results
