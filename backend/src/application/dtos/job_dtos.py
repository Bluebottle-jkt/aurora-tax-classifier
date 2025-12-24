"""
Job Data Transfer Objects.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class CreateJobRequest(BaseModel):
    """Request to create a new job"""
    business_type: str = Field(..., min_length=1)
    preprocessing_preset: str = Field(default="standard")


class JobSummary(BaseModel):
    """Job summary information"""
    total_rows: int
    avg_confidence: float
    risk_percent: float


class JobResponse(BaseModel):
    """Job response with full details"""
    job_id: str
    business_type: str
    file_name: str
    status: str
    created_at: str
    updated_at: str
    summary: Optional[JobSummary] = None
    risk_report: Optional[Dict[str, Any]] = None
    audit_trail: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
