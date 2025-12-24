"""
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
