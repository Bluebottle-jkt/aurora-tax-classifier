"""
Get Job Rows Use Case
"""

from typing import List, Dict, Any
from ..ports import PredictionRepositoryPort


class GetJobRowsUseCase:
    def __init__(self, prediction_repository: PredictionRepositoryPort):
        self.prediction_repository = prediction_repository

    def execute(
        self, job_id: str, page: int = 1, page_size: int = 100
    ) -> Dict[str, Any]:
        offset = (page - 1) * page_size
        rows = self.prediction_repository.find_by_job(job_id, page_size, offset)
        total = self.prediction_repository.count_by_job(job_id)

        return {
            "rows": [row.to_dict() for row in rows],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "pages": (total + page_size - 1) // page_size
            }
        }
