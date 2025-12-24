"""
Risk Score Value Object.
Represents a business-to-ledger compliance risk score between 0 and 100.
"""

from ..errors import InvalidRiskScoreError


class RiskScore:
    """
    Immutable value object representing a risk score (0-100%).
    Higher score = higher risk.
    """

    MIN_SCORE = 0
    MAX_SCORE = 100

    def __init__(self, score: float):
        """
        Create a RiskScore.

        Args:
            score: Risk score between 0 and 100

        Raises:
            InvalidRiskScoreError: If score is out of range
        """
        if not isinstance(score, (int, float)):
            raise InvalidRiskScoreError(
                f"Score must be a number, got {type(score)}"
            )

        if score < self.MIN_SCORE or score > self.MAX_SCORE:
            raise InvalidRiskScoreError(
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

    @property
    def risk_level(self) -> str:
        """Get risk level category"""
        if self._score < 20:
            return "LOW"
        elif self._score < 50:
            return "MODERATE"
        elif self._score < 75:
            return "HIGH"
        else:
            return "CRITICAL"

    def is_high_risk(self, threshold: float = 50.0) -> bool:
        """Check if risk is above threshold"""
        return self._score >= threshold

    def is_low_risk(self, threshold: float = 20.0) -> bool:
        """Check if risk is below threshold"""
        return self._score < threshold

    def __str__(self) -> str:
        return f"{self._score:.1f}"

    def __repr__(self) -> str:
        return f"RiskScore({self._score:.1f})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, RiskScore):
            return False
        return abs(self._score - other._score) < 0.01

    def __lt__(self, other) -> bool:
        if not isinstance(other, RiskScore):
            raise TypeError(f"Cannot compare RiskScore with {type(other)}")
        return self._score < other._score

    def __hash__(self) -> int:
        return hash(round(self._score, 1))
