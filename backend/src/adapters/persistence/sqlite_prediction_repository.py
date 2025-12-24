from typing import List, Optional, Dict
from ...application.ports import PredictionRepositoryPort
from ...domain.entities import PredictionRow


class SQLitePredictionRepository(PredictionRepositoryPort):
    """In-memory repository for MVP"""

    def __init__(self):
        self._predictions: Dict[str, List[PredictionRow]] = {}

    def save_batch(self, rows: List[PredictionRow]) -> None:
        if not rows:
            return
        job_id = rows[0].job_id
        self._predictions[job_id] = rows

    def find_by_job(
        self, job_id: str, limit: int = 100, offset: int = 0
    ) -> List[PredictionRow]:
        rows = self._predictions.get(job_id, [])
        return rows[offset:offset + limit]

    def count_by_job(self, job_id: str) -> int:
        return len(self._predictions.get(job_id, []))

    def delete_by_job(self, job_id: str) -> None:
        if job_id in self._predictions:
            del self._predictions[job_id]
