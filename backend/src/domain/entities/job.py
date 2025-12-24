"""
Job Entity - represents a classification job.
Core domain entity with business logic.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
from ..errors import InvalidJobStatusError


class JobStatus(Enum):
    """Valid job statuses"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Job:
    """
    Represents a tax object classification job.
    Aggregate root for the job bounded context.
    """

    def __init__(
        self,
        job_id: str,
        business_type: str,
        file_name: str,
        file_hash: str,
        status: JobStatus = JobStatus.PENDING,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        total_rows: int = 0,
        avg_confidence: float = 0.0,
        risk_percent: float = 0.0,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Create a Job entity.

        Args:
            job_id: Unique job identifier
            business_type: Taxpayer business type
            file_name: Original uploaded file name
            file_hash: SHA256 hash of uploaded file
            status: Current job status
            created_at: Creation timestamp
            updated_at: Last update timestamp
            total_rows: Total number of GL rows
            avg_confidence: Average confidence across all predictions
            risk_percent: Dataset-level risk score
            error_message: Error message if job failed
            metadata: Additional job metadata
        """
        self._job_id = job_id
        self._business_type = business_type
        self._file_name = file_name
        self._file_hash = file_hash
        self._status = status
        self._created_at = created_at or datetime.utcnow()
        self._updated_at = updated_at or datetime.utcnow()
        self._total_rows = total_rows
        self._avg_confidence = avg_confidence
        self._risk_percent = risk_percent
        self._error_message = error_message
        self._metadata = metadata or {}

    # Properties
    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def business_type(self) -> str:
        return self._business_type

    @property
    def file_name(self) -> str:
        return self._file_name

    @property
    def file_hash(self) -> str:
        return self._file_hash

    @property
    def status(self) -> JobStatus:
        return self._status

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    @property
    def total_rows(self) -> int:
        return self._total_rows

    @property
    def avg_confidence(self) -> float:
        return self._avg_confidence

    @property
    def risk_percent(self) -> float:
        return self._risk_percent

    @property
    def error_message(self) -> Optional[str]:
        return self._error_message

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata.copy()

    # Business logic
    def start_processing(self) -> None:
        """
        Transition job to processing status.

        Raises:
            InvalidJobStatusError: If transition is invalid
        """
        if self._status != JobStatus.PENDING:
            raise InvalidJobStatusError(
                f"Cannot start processing job in status {self._status.value}"
            )
        self._status = JobStatus.PROCESSING
        self._updated_at = datetime.utcnow()

    def mark_completed(
        self,
        total_rows: int,
        avg_confidence: float,
        risk_percent: float
    ) -> None:
        """
        Mark job as completed with results.

        Args:
            total_rows: Total number of processed rows
            avg_confidence: Average confidence score
            risk_percent: Dataset-level risk score

        Raises:
            InvalidJobStatusError: If transition is invalid
        """
        if self._status != JobStatus.PROCESSING:
            raise InvalidJobStatusError(
                f"Cannot complete job in status {self._status.value}"
            )
        self._status = JobStatus.COMPLETED
        self._total_rows = total_rows
        self._avg_confidence = avg_confidence
        self._risk_percent = risk_percent
        self._updated_at = datetime.utcnow()

    def mark_failed(self, error_message: str) -> None:
        """
        Mark job as failed with error message.

        Args:
            error_message: Description of failure

        Raises:
            InvalidJobStatusError: If transition is invalid
        """
        if self._status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            raise InvalidJobStatusError(
                f"Cannot fail job in status {self._status.value}"
            )
        self._status = JobStatus.FAILED
        self._error_message = error_message
        self._updated_at = datetime.utcnow()

    def is_terminal(self) -> bool:
        """Check if job is in a terminal status"""
        return self._status in [JobStatus.COMPLETED, JobStatus.FAILED]

    def can_retry(self) -> bool:
        """Check if job can be retried"""
        return self._status == JobStatus.FAILED

    def __repr__(self) -> str:
        return (
            f"Job(job_id='{self._job_id}', "
            f"status={self._status.value}, "
            f"business_type='{self._business_type}')"
        )
