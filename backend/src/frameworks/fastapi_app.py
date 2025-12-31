"""
FastAPI application factory
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import os

# Import adapters
from ..adapters.ml.tfidf_classifier import TfidfClassifier
from ..adapters.ml.two_stage_classifier import TwoStageClassifier
from ..adapters.persistence.sqlite_job_repository import SQLiteJobRepository
from ..adapters.persistence.sqlite_prediction_repository import SQLitePredictionRepository
from ..adapters.storage.local_storage import LocalStorage
from ..adapters.config.json_config import JsonConfig
from ..adapters.explainability.tfidf_explainer import TfidfExplainer

# Import policies
from ..domain.policies import ConfidencePolicy, RiskPolicy

# Import use cases
from ..application.use_cases import (
    CreateJobUseCase,
    ProcessJobUseCase,
)
from ..application.use_cases.inspect_file_use_case import InspectFileUseCase

# Import domain objects
from ..domain.value_objects import TaxObjectLabel

# Initialize app
app = FastAPI(title="AURORA Tax Classifier", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies (Dependency Injection)
job_repo = SQLiteJobRepository()
pred_repo = SQLitePredictionRepository()
storage = LocalStorage()
config = JsonConfig()

# Use TwoStageClassifier with the new models
classifier = TwoStageClassifier(
    fiscal_model_path="models/koreksi_fiskal_lr.joblib",
    tax_object_model_path="models/objek_pph_lr.joblib"
)

# For explainer, we'll use the tax object model as the primary model
explainer = TfidfExplainer(classifier.tax_object_model)

scoring_config = config.get_scoring_config()
confidence_policy = ConfidencePolicy(**scoring_config["confidence"])
risk_policy = RiskPolicy(**scoring_config["risk"])

create_job_uc = CreateJobUseCase(job_repo, storage)
process_job_uc = ProcessJobUseCase(
    job_repo, pred_repo, classifier, storage, config, explainer,
    confidence_policy, risk_policy
)
inspect_file_uc = InspectFileUseCase()

# API Key validation
API_KEY = os.getenv("API_KEY", "aurora-dev-key")

def verify_api_key(x_aurora_key: Optional[str] = Header(None)):
    if x_aurora_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# Routes
@app.post("/api/files/inspect")
async def inspect_file(
    file: UploadFile = File(...),
    x_aurora_key: str = Header(None)
):
    """Inspect uploaded file and return metadata + preview"""
    verify_api_key(x_aurora_key)

    try:
        # Get file content
        content = await file.read()

        # Reset file pointer for potential reuse
        await file.seek(0)

        # Use BytesIO for pandas compatibility
        from io import BytesIO
        file_stream = BytesIO(content)

        # Inspect file
        result = inspect_file_uc.execute(file_stream, file.filename)

        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File inspection failed: {str(e)}")


@app.post("/api/jobs")
async def create_job(
    file: UploadFile = File(...),
    business_type: str = Form(...),
    selected_categories: Optional[str] = Form(None),
    selected_divisions: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = None,
    x_aurora_key: str = Header(None)
):
    """Create new classification job"""
    verify_api_key(x_aurora_key)

    import json

    # Parse selected categories and divisions
    categories = json.loads(selected_categories) if selected_categories else []
    divisions = json.loads(selected_divisions) if selected_divisions else []

    # Create job
    job = create_job_uc.execute(
        file.file, file.filename, business_type
    )

    # Process in background (pass categories and divisions for future use)
    # Note: Currently the classifier doesn't filter by these, but they're available
    background_tasks.add_task(process_job_uc.execute, job.job_id)

    return {
        "job_id": job.job_id,
        "status": job.status.value,
        "selected_categories": categories,
        "selected_divisions": divisions
    }


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: str, x_aurora_key: str = Header(None)):
    """Get job status"""
    verify_api_key(x_aurora_key)

    job = job_repo.find_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Calculate total_amount if job is completed
    total_amount = None
    if job.status.value == "completed":
        rows = pred_repo.find_by_job(job_id, limit=10000, offset=0)
        amounts = [r.amount for r in rows if r.amount is not None]
        total_amount = sum(amounts) if amounts else 0

    return {
        "job_id": job.job_id,
        "status": job.status.value,
        "business_type": job.business_type,
        "file_name": job.file_name,
        "created_at": job.created_at.isoformat(),
        "summary": {
            "total_rows": job.total_rows,
            "avg_confidence": job.avg_confidence,
            "risk_percent": job.risk_percent,
            "total_amount": total_amount,
        } if job.status.value == "completed" else None
    }


@app.get("/api/jobs/{job_id}/rows")
async def get_rows(
    job_id: str,
    page: int = 1,
    page_size: int = 1000,
    x_aurora_key: str = Header(None)
):
    """Get prediction rows"""
    verify_api_key(x_aurora_key)

    offset = (page - 1) * page_size
    rows = pred_repo.find_by_job(job_id, page_size, offset)
    total = pred_repo.count_by_job(job_id)

    return {
        "rows": [row.to_dict() for row in rows],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "pages": (total + page_size - 1) // page_size
        }
    }


@app.get("/api/config")
async def get_config(x_aurora_key: str = Header(None)):
    """Get configuration"""
    verify_api_key(x_aurora_key)

    return {
        "labels": config.get_labels(),
        "scoring_config": config.get_scoring_config(),
        "priors": config.get_priors(),
    }


@app.get("/api/kbli/categories")
async def get_kbli_categories(x_aurora_key: str = Header(None)):
    """Get KBLI categories and divisions from JSON"""
    verify_api_key(x_aurora_key)

    import json
    from pathlib import Path

    # Load KBLI JSON file
    kbli_file = Path(__file__).parent.parent.parent.parent / "aurora_v2" / "kbli_2025_kategori_A_B_D_to_V_2digit_keywords.json"

    try:
        with open(kbli_file, 'r', encoding='utf-8') as f:
            kbli_data = json.load(f)

        return {
            "metadata": kbli_data.get("metadata", {}),
            "categories": kbli_data.get("categories", [])
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="KBLI data file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load KBLI data: {str(e)}")




@app.post("/api/predict/direct")
async def predict_direct(request: dict, x_aurora_key: str = Header(None)):
    """Direct text analysis endpoint"""
    try:
        verify_api_key(x_aurora_key)

        texts = request.get("texts", [])
        selected_categories = request.get("selected_categories", [])
        selected_divisions = request.get("selected_divisions", [])

        if not texts:
            raise HTTPException(status_code=400, detail="No texts provided")

        if len(texts) > 100:
            raise HTTPException(status_code=400, detail="Maximum 100 texts allowed")

        # Note: For now, we'll use the standard classifier
        # In future, you can filter models based on selected_divisions
        # For example: Load specific models for selected business types

        # Predict using classifier
        predictions_raw = classifier.predict_proba(texts)

        results = []
        for idx, (text, prob_dist) in enumerate(zip(texts, predictions_raw)):
            # Get predicted label
            predicted_label_str = max(prob_dist, key=prob_dist.get)

            # Calculate confidence
            confidence, signals = confidence_policy.calculate(prob_dist, text)

            # Get explanation
            try:
                top_terms = explainer.get_top_terms(text, predicted_label_str, limit=5)
                explanation = f"Based on terms: {', '.join(top_terms[:3])}" if top_terms else "Classification based on text pattern"
            except:
                explanation = f"Classified as {predicted_label_str} based on text analysis"

            results.append({
                "account_name": text,
                "predicted_label": predicted_label_str,
                "confidence": confidence.score,
                "explanation": explanation,
                "business_context": {
                    "categories": selected_categories,
                    "divisions": selected_divisions
                } if selected_divisions else None
            })

        return {"predictions": results}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


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


@app.get("/api/healthz")
async def health():
    """Health check"""
    return {"status": "healthy"}
