"""
TF-IDF explainability adapter
"""

from typing import List, Dict, Any
from ...application.ports import ExplainabilityPort


class TfidfExplainer(ExplainabilityPort):
    """TF-IDF-based explainability"""

    def __init__(self, model):
        self.model = model

    def get_top_terms(self, text: str, label: str, limit: int = 5) -> List[str]:
        """Get top terms (simplified)"""
        # This is a simplified version
        # Full implementation would extract feature importance from TF-IDF
        terms = text.lower().split()
        return terms[:limit]

    def get_nearest_examples(
        self, text: str, limit: int = 3
    ) -> List[Dict[str, Any]]:
        """Get nearest examples (simplified)"""
        return []
