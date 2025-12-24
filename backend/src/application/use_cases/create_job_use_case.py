"""
Create Job Use Case
"""

import hashlib
from datetime import datetime
from typing import BinaryIO
from ...domain.entities import Job, JobStatus
from ..ports import JobRepositoryPort, StoragePort


class CreateJobUseCase:
    """Creates a new classification job"""

    def __init__(
        self,
        job_repository: JobRepositoryPort,
        storage: StoragePort,
    ):
        self.job_repository = job_repository
        self.storage = storage

    def execute(
        self,
        file: BinaryIO,
        filename: str,
        business_type: str,
    ) -> Job:
        """
        Create a new job.

        Args:
            file: Uploaded file
            filename: Original filename
            business_type: Business type

        Returns:
            Created Job entity
        """
        # Generate job ID
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        job_id = f"job_{timestamp}_{hash(filename) % 10000:04d}"

        # Calculate file hash
        file.seek(0)
        file_hash = hashlib.sha256(file.read()).hexdigest()
        file.seek(0)

        # Save file
        self.storage.save_file(file, job_id, filename)

        # Create job entity
        job = Job(
            job_id=job_id,
            business_type=business_type,
            file_name=filename,
            file_hash=file_hash,
            status=JobStatus.PENDING,
        )

        # Persist
        self.job_repository.save(job)

        return job
