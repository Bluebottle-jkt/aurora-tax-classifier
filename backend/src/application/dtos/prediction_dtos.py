"""
Prediction Data Transfer Objects.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class PredictionRowResponse(BaseModel):
    """Prediction row response"""
    row_id: str
    row_index: int
    account_name: str
    account_code: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[str] = None
    predicted_tax_object: str
    confidence_percent: float
    explanation: str
    signals: List[str]
    probability_distribution: Optional[Dict[str, float]] = None
    top_terms: Optional[List[str]] = None
    nearest_examples: Optional[List[Dict[str, Any]]] = None
