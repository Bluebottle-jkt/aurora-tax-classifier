#!/usr/bin/env python3
"""
AURORA Project Generator
Creates all remaining files for the complete project structure.
Run this script to generate the full application.
"""

import os
from pathlib import Path

# File contents dictionary
FILES = {
    # Backend - Application Ports
    "backend/src/application/ports/classifier_port.py": '''"""
Classifier Port interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class ClassifierPort(ABC):
    """Port for ML classifier"""

    @abstractmethod
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Predict probability distribution for texts.

        Args:
            texts: List of account names

        Returns:
            List of {label: probability} dictionaries
        """
        pass

    @abstractmethod
    def get_version(self) -> str:
        """Get model version"""
        pass
''',

    "backend/src/application/ports/storage_port.py": '''"""
Storage Port interface.
"""

from abc import ABC, abstractmethod
from typing import BinaryIO


class StoragePort(ABC):
    """Port for file storage"""

    @abstractmethod
    def save_file(self, file: BinaryIO, job_id: str, filename: str) -> str:
        """Save uploaded file and return path"""
        pass

    @abstractmethod
    def get_file_path(self, job_id: str, filename: str) -> str:
        """Get file path"""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        """Delete file"""
        pass
''',

    "backend/src/application/ports/config_port.py": '''"""
Config Port interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ConfigPort(ABC):
    """Port for configuration loading"""

    @abstractmethod
    def get_scoring_config(self) -> Dict[str, Any]:
        """Get scoring configuration"""
        pass

    @abstractmethod
    def get_priors(self) -> Dict[str, Dict[str, float]]:
        """Get business type priors"""
        pass

    @abstractmethod
    def get_labels(self) -> list[str]:
        """Get valid tax object labels"""
        pass
''',

    "backend/src/application/ports/explainability_port.py": '''"""
Explainability Port interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ExplainabilityPort(ABC):
    """Port for model explainability"""

    @abstractmethod
    def get_top_terms(self, text: str, label: str, limit: int = 5) -> List[str]:
        """Get top contributing terms for prediction"""
        pass

    @abstractmethod
    def get_nearest_examples(
        self, text: str, limit: int = 3
    ) -> List[Dict[str, Any]]:
        """Get nearest training examples"""
        pass
''',

    # Backend - Application DTOs
    "backend/src/application/dtos/__init__.py": '''from .job_dtos import CreateJobRequest, JobResponse, JobSummary
from .prediction_dtos import PredictionRowResponse
from .config_dtos import ConfigResponse

__all__ = [
    "CreateJobRequest",
    "JobResponse",
    "JobSummary",
    "PredictionRowResponse",
    "ConfigResponse",
]
''',

    "backend/src/application/dtos/job_dtos.py": '''"""
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
''',

    "backend/src/application/dtos/prediction_dtos.py": '''"""
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
''',

    "backend/src/application/dtos/config_dtos.py": '''"""
Config Data Transfer Objects.
"""

from typing import Dict, Any, List
from pydantic import BaseModel


class ConfigResponse(BaseModel):
    """Configuration response"""
    labels: List[str]
    scoring_config: Dict[str, Any]
    priors: Dict[str, Dict[str, float]]
''',

}

def create_files():
    """Create all files"""
    base_path = Path(__file__).parent

    for file_path, content in FILES.items():
        full_path = base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"Creating {file_path}...")
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"\\n✅ Created {len(FILES)} files")
    print("\\nNext: Run the complete setup script to generate ALL remaining files")

if __name__ == "__main__":
    create_files()
