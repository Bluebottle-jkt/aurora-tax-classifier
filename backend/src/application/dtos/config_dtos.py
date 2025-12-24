"""
Config Data Transfer Objects.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class ConfigResponse(BaseModel):
    """Configuration response"""
    labels: List[str]
    scoring_config: Dict[str, Any]
    priors: Dict[str, Dict[str, float]]
