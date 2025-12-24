"""
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
