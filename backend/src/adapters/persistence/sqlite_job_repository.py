from typing import List, Optional, Dict
from ...application.ports import JobRepositoryPort
from ...domain.entities import Job


class SQLiteJobRepository(JobRepositoryPort):
    """In-memory repository for MVP"""

    def __init__(self):
        self._jobs: Dict[str, Job] = {}

    def save(self, job: Job) -> None:
        self._jobs[job.job_id] = job

    def find_by_id(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    def find_all(self, limit: int = 100, offset: int = 0) -> List[Job]:
        all_jobs = list(self._jobs.values())
        return all_jobs[offset:offset + limit]

    def exists(self, job_id: str) -> bool:
        return job_id in self._jobs
