"""
Confidence Policy - business rules for calculating row-level confidence scores.
Pure domain logic, no framework dependencies.
"""

import math
import re
from typing import Dict, List
from ..value_objects import ConfidenceScore


class ConfidencePolicy:
    """
    Implements confidence scoring algorithm as a pure function.
    Formula:
        confidence_raw = p_max_weight * p_max + margin_weight * sigmoid(10 * margin)
        confidence_percent = round(100 * clamp(confidence_raw with penalties, 0, 1))
    """

    def __init__(
        self,
        p_max_weight: float = 0.65,
        margin_weight: float = 0.35,
        short_text_penalty: float = 0.75,
        vague_text_penalty: float = 0.85,
        short_text_threshold: int = 3,
    ):
        """
        Initialize policy with configurable parameters.

        Args:
            p_max_weight: Weight for maximum probability
            margin_weight: Weight for probability margin
            short_text_penalty: Penalty multiplier for short text
            vague_text_penalty: Penalty multiplier for vague text
            short_text_threshold: Character threshold for short text
        """
        self.p_max_weight = p_max_weight
        self.margin_weight = margin_weight
        self.short_text_penalty = short_text_penalty
        self.vague_text_penalty = vague_text_penalty
        self.short_text_threshold = short_text_threshold

    @staticmethod
    def sigmoid(x: float) -> float:
        """Sigmoid function for margin scaling"""
        return 1.0 / (1.0 + math.exp(-x))

    @staticmethod
    def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Clamp value to range"""
        return max(min_val, min(max_val, value))

    def calculate(
        self,
        probability_distribution: Dict[str, float],
        account_name: str,
    ) -> tuple[ConfidenceScore, List[str]]:
        """
        Calculate confidence score for a prediction.

        Args:
            probability_distribution: Dict of label -> probability
            account_name: The account name text

        Returns:
            Tuple of (ConfidenceScore, list of quality signals)
        """
        # Get top two probabilities
        probs = sorted(probability_distribution.values(), reverse=True)
        p_max = probs[0] if len(probs) > 0 else 0.0
        p_second = probs[1] if len(probs) > 1 else 0.0
        margin = p_max - p_second

        # Base confidence calculation
        confidence_raw = (
            self.p_max_weight * p_max +
            self.margin_weight * self.sigmoid(10 * margin)
        )

        # Apply penalties and track signals
        signals = []

        # Short text penalty
        if self._is_short_text(account_name):
            confidence_raw *= self.short_text_penalty
            signals.append("short_text")

        # Vague text penalty
        if self._is_vague_text(account_name):
            confidence_raw *= self.vague_text_penalty
            signals.append("vague_text")

        # Mostly digits/symbols penalty
        if self._is_mostly_symbols(account_name):
            confidence_raw *= self.short_text_penalty
            signals.append("mostly_symbols")

        # Clamp to [0, 1] and convert to percentage
        confidence_raw = self.clamp(confidence_raw, 0.0, 1.0)
        confidence_percent = round(confidence_raw * 100, 1)

        return ConfidenceScore(confidence_percent), signals

    def _is_short_text(self, text: str) -> bool:
        """Check if text is too short"""
        return len(text.strip()) < self.short_text_threshold

    def _is_vague_text(self, text: str) -> bool:
        """Check if text contains vague keywords"""
        vague_keywords = [
            "unknown", "misc", "miscellaneous", "other", "others",
            "lain", "lainnya", "umum", "berbagai"
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in vague_keywords)

    def _is_mostly_symbols(self, text: str) -> bool:
        """Check if text is mostly digits or symbols"""
        if not text:
            return False

        # Count alphanumeric vs total characters
        alphanumeric = len(re.findall(r'[a-zA-Z]', text))
        total = len(text.replace(' ', ''))

        if total == 0:
            return True

        # If less than 30% alphabetic characters, consider it mostly symbols
        return (alphanumeric / total) < 0.3
