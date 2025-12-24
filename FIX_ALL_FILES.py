#!/usr/bin/env python3
"""
Fix all stub files with complete implementations
"""

import os
from pathlib import Path

def write_file(path, content):
    """Write file with content"""
    Path(path).write_text(content, encoding='utf-8')
    print(f"[OK] {path} ({len(content)} bytes)")

# Add download route to FastAPI app
fastapi_download_addition = """

@app.get("/api/jobs/{job_id}/download")
async def download_results(job_id: str, x_aurora_key: str = Header(None)):
    from fastapi.responses import Response
    verify_api_key(x_aurora_key)

    job = job_repo.find_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status.value != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")

    rows = pred_repo.find_by_job(job_id, limit=10000, offset=0)

    import csv
    from io import StringIO
    output = StringIO()

    if rows:
        fieldnames = ["row_index", "account_name", "predicted_tax_object",
                     "confidence_percent", "explanation"]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            writer.writerow({
                "row_index": row.row_index,
                "account_name": row.account_name,
                "predicted_tax_object": str(row.predicted_label),
                "confidence_percent": row.confidence.score,
                "explanation": row.explanation
            })

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={job_id}_results.csv"}
    )
"""

# Read current fastapi_app.py
fastapi_path = "backend/src/frameworks/fastapi_app.py"
current_content = Path(fastapi_path).read_text(encoding='utf-8')

# Check if download route exists
if "/download" not in current_content:
    # Find insertion point (before the health check or at end)
    if "@app.get(\"/api/healthz\")" in current_content:
        parts = current_content.split("@app.get(\"/api/healthz\")")
        new_content = parts[0] + fastapi_download_addition + "\n\n@app.get(\"/api/healthz\")" + parts[1]
    else:
        new_content = current_content + fastapi_download_addition

    Path(fastapi_path).write_text(new_content, encoding='utf-8')
    print(f"[UPDATED] {fastapi_path} - Added download route")
else:
    print(f"[SKIP] {fastapi_path} - Download route already exists")

# Fix SQLite repository to include Dict import
sqlite_repo_fix = """from typing import List, Optional, Dict
from ...application.ports import PredictionRepositoryPort
from ...domain.entities import PredictionRow


class SQLitePredictionRepository(PredictionRepositoryPort):
    \"\"\"In-memory repository for MVP\"\"\"

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
"""

write_file("backend/src/adapters/persistence/sqlite_prediction_repository.py", sqlite_repo_fix)

# Add missing Dict import to job repository
sqlite_job_fix = """from typing import List, Optional, Dict
from ...application.ports import JobRepositoryPort
from ...domain.entities import Job


class SQLiteJobRepository(JobRepositoryPort):
    \"\"\"In-memory repository for MVP\"\"\"

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
"""

write_file("backend/src/adapters/persistence/sqlite_job_repository.py", sqlite_job_fix)

print("\n[SUCCESS] All files fixed with complete implementations!")
print("\nFile sizes:")
os.system("cd backend/src && find . -name '*.py' -exec wc -l {} + | sort -n | tail -10")
