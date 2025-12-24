"""
Repository Port interfaces.
Define contracts for persistence adapters.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ...domain.entities import Job, PredictionRow


class JobRepositoryPort(ABC):
    """Port for job persistence"""

    @abstractmethod
    def save(self, job: Job) -> None:
        """Save or update a job"""
        pass

    @abstractmethod
    def find_by_id(self, job_id: str) -> Optional[Job]:
        """Find job by ID"""
        pass

    @abstractmethod
    def find_all(self, limit: int = 100, offset: int = 0) -> List[Job]:
        """Find all jobs with pagination"""
        pass

    @abstractmethod
    def exists(self, job_id: str) -> bool:
        """Check if job exists"""
        pass


class PredictionRepositoryPort(ABC):
    """Port for prediction row persistence"""

    @abstractmethod
    def save_batch(self, rows: List[PredictionRow]) -> None:
        """Save batch of prediction rows"""
        pass

    @abstractmethod
    def find_by_job(
        self,
        job_id: str,
        limit: int = 100,
        offset: int = 0
    ) -> List[PredictionRow]:
        """Find prediction rows by job ID with pagination"""
        pass

    @abstractmethod
    def count_by_job(self, job_id: str) -> int:
        """Count prediction rows for a job"""
        pass

    @abstractmethod
    def delete_by_job(self, job_id: str) -> None:
        """Delete all predictions for a job"""
        pass
