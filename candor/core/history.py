# candor/core/history.py
from datetime import datetime
from candor.core.job import Job

HISTORY: list[Job] = []
_next_id = 1

def record_job(intent, result) -> Job:
    global _next_id
    job = Job(
        id=_next_id,
        intent=intent,
        started=datetime.now(),
        finished=datetime.now(),
        result=result
    )
    HISTORY.append(job)
    _next_id += 1
    return job

def list_jobs() -> list[Job]:
    return HISTORY
