"""
Get Job Status Use Case
"""

from typing import Optional
from ...domain.entities import Job
from ..ports import JobRepositoryPort
from ..dtos import JobResponse, JobSummary


class GetJobStatusUseCase:
    def __init__(self, job_repository: JobRepositoryPort):
        self.job_repository = job_repository

    def execute(self, job_id: str) -> Optional[JobResponse]:
        job = self.job_repository.find_by_id(job_id)
        if not job:
            return None

        summary = None
        if job.status.value == "completed":
            summary = JobSummary(
                total_rows=job.total_rows,
                avg_confidence=round(job.avg_confidence, 2),
                risk_percent=round(job.risk_percent, 2)
            )

        return JobResponse(
            job_id=job.job_id,
            business_type=job.business_type,
            file_name=job.file_name,
            status=job.status.value,
            created_at=job.created_at.isoformat(),
            updated_at=job.updated_at.isoformat(),
            summary=summary,
            error_message=job.error_message
        )
