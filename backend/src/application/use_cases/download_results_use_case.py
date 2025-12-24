"""
Download Results Use Case
"""

import csv
from io import StringIO
from ..ports import PredictionRepositoryPort, JobRepositoryPort


class DownloadResultsUseCase:
    def __init__(
        self,
        prediction_repository: PredictionRepositoryPort,
        job_repository: JobRepositoryPort
    ):
        self.prediction_repository = prediction_repository
        self.job_repository = job_repository

    def execute(self, job_id: str) -> str:
        # Get all rows
        rows = self.prediction_repository.find_by_job(job_id, limit=10000, offset=0)

        # Create CSV
        output = StringIO()
        if not rows:
            return ""

        # Write header
        fieldnames = [
            "row_index", "account_name", "account_code", "amount", "date",
            "predicted_tax_object", "confidence_percent", "explanation", "signals"
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        # Write rows
        for row in rows:
            writer.writerow({
                "row_index": row.row_index,
                "account_name": row.account_name,
                "account_code": row.account_code or "",
                "amount": row.amount or "",
                "date": row.date or "",
                "predicted_tax_object": str(row.predicted_label),
                "confidence_percent": row.confidence.score,
                "explanation": row.explanation,
                "signals": "|".join(row.signals)
            })

        return output.getvalue()
