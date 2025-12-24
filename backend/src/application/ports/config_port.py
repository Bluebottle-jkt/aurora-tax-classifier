"""
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
