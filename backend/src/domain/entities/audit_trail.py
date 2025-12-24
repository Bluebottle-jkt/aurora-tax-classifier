"""
Audit Trail Entity - represents audit information for a job.
"""

from datetime import datetime
from typing import Dict, Any


class AuditTrail:
    """
    Represents audit trail information for compliance and traceability.
    """

    def __init__(
        self,
        job_id: str,
        model_version: str,
        preprocessing_version: str,
        scoring_version: str,
        input_file_sha256: str,
        timestamp: datetime,
        metadata: Dict[str, Any],
    ):
        """
        Create an AuditTrail.

        Args:
            job_id: Parent job identifier
            model_version: ML model version used
            preprocessing_version: Preprocessing pipeline version
            scoring_version: Scoring algorithm version
            input_file_sha256: SHA256 hash of input file
            timestamp: Processing timestamp
            metadata: Additional audit metadata
        """
        self._job_id = job_id
        self._model_version = model_version
        self._preprocessing_version = preprocessing_version
        self._scoring_version = scoring_version
        self._input_file_sha256 = input_file_sha256
        self._timestamp = timestamp
        self._metadata = metadata

    # Properties
    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def model_version(self) -> str:
        return self._model_version

    @property
    def preprocessing_version(self) -> str:
        return self._preprocessing_version

    @property
    def scoring_version(self) -> str:
        return self._scoring_version

    @property
    def input_file_sha256(self) -> str:
        return self._input_file_sha256

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata.copy()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "job_id": self._job_id,
            "model_version": self._model_version,
            "preprocessing_version": self._preprocessing_version,
            "scoring_version": self._scoring_version,
            "input_file_sha256": self._input_file_sha256,
            "timestamp": self._timestamp.isoformat(),
            "metadata": self._metadata,
        }

    def __repr__(self) -> str:
        return (
            f"AuditTrail(job_id='{self._job_id}', "
            f"model_version='{self._model_version}', "
            f"timestamp={self._timestamp.isoformat()})"
        )
