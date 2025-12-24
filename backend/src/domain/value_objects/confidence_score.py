"""
Confidence Score Value Object.
Represents a confidence score between 0 and 100.
"""

from ..errors import InvalidConfidenceScoreError


class ConfidenceScore:
    """
    Immutable value object representing a confidence score (0-100%).
    """

    MIN_SCORE = 0
    MAX_SCORE = 100

    def __init__(self, score: float):
        """
        Create a ConfidenceScore.

        Args:
            score: Confidence score between 0 and 100

        Raises:
            InvalidConfidenceScoreError: If score is out of range
        """
        if not isinstance(score, (int, float)):
            raise InvalidConfidenceScoreError(
                f"Score must be a number, got {type(score)}"
            )

        if score < self.MIN_SCORE or score > self.MAX_SCORE:
            raise InvalidConfidenceScoreError(
                f"Score must be between {self.MIN_SCORE} and {self.MAX_SCORE}, got {score}"
            )

        self._score = float(score)

    @property
    def score(self) -> float:
        """Get the score value"""
        return self._score

    @property
    def percentage(self) -> str:
        """Get score as percentage string"""
        return f"{self._score:.1f}%"

    def is_high_confidence(self, threshold: float = 80.0) -> bool:
        """Check if score is above threshold"""
        return self._score >= threshold

    def is_low_confidence(self, threshold: float = 50.0) -> bool:
        """Check if score is below threshold"""
        return self._score < threshold

    def __str__(self) -> str:
        return f"{self._score:.1f}"

    def __repr__(self) -> str:
        return f"ConfidenceScore({self._score:.1f})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, ConfidenceScore):
            return False
        return abs(self._score - other._score) < 0.01

    def __lt__(self, other) -> bool:
        if not isinstance(other, ConfidenceScore):
            raise TypeError(f"Cannot compare ConfidenceScore with {type(other)}")
        return self._score < other._score

    def __hash__(self) -> int:
        return hash(round(self._score, 1))
