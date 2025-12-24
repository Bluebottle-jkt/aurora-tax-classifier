"""
Get Config Use Case
"""

from typing import Dict, Any
from ..ports import ConfigPort


class GetConfigUseCase:
    def __init__(self, config: ConfigPort):
        self.config = config

    def execute(self) -> Dict[str, Any]:
        return {
            "labels": self.config.get_labels(),
            "scoring_config": self.config.get_scoring_config(),
            "priors": self.config.get_priors()
        }
