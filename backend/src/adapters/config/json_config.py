"""
JSON config adapter
"""

import json
from pathlib import Path
from typing import Dict, Any
from ...application.ports import ConfigPort
from ...domain.value_objects import TaxObjectLabel


class JsonConfig(ConfigPort):
    """JSON-based configuration"""

    def __init__(
        self,
        scoring_path: str = "config/scoring.json",
        priors_path: str = "config/priors.json",
    ):
        self.scoring_path = Path(scoring_path)
        self.priors_path = Path(priors_path)

    def get_scoring_config(self) -> Dict[str, Any]:
        with open(self.scoring_path, 'r') as f:
            return json.load(f)

    def get_priors(self) -> Dict[str, Dict[str, float]]:
        with open(self.priors_path, 'r') as f:
            return json.load(f)

    def get_labels(self) -> list[str]:
        return TaxObjectLabel.all_labels()
