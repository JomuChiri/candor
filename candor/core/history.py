# candor/core/history.py
import os
import pickle
from dataclasses import dataclass
from candor.core.intent import Intent
from candor.core.plan import Plan
from candor.core.result import ExecutionResult

HISTORY_PATH = os.path.expanduser("~/.candor/history")

@dataclass
class Job:
    id: int
    intent: Intent
    plan: Plan
    result: ExecutionResult

def ensure_history_dir():
    os.makedirs(HISTORY_PATH, exist_ok=True)

def record_job(intent, plan, result):
    ensure_history_dir()
    job_id = len(list_jobs()) + 1
    job = Job(id=job_id, intent=intent, plan=plan, result=result)
    filename = os.path.join(HISTORY_PATH, f"job_{job_id}.pkl")
    with open(filename, "wb") as f:
        pickle.dump(job, f)
    return job

def list_jobs():
    ensure_history_dir()
    jobs = []
    for fname in sorted(os.listdir(HISTORY_PATH)):
        if fname.startswith("job_") and fname.endswith(".pkl"):
            with open(os.path.join(HISTORY_PATH, fname), "rb") as f:
                jobs.append(pickle.load(f))
    return jobs

def load_job(job_id="latest"):
    jobs = list_jobs()
    if not jobs:
        return None
    if job_id == "latest":
        return jobs[-1]
    for job in jobs:
        if job.id == job_id:
            return job
    return None
