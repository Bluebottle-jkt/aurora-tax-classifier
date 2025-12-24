"""
Risk Report Entity - represents dataset-level risk assessment.
"""

from typing import Dict, List, Any
from ..value_objects import RiskScore


class RiskReport:
    """
    Represents a business-to-ledger compliance risk report.
    """

    def __init__(
        self,
        job_id: str,
        business_type: str,
        risk_score: RiskScore,
        label_distribution: Dict[str, float],
        expected_distribution: Dict[str, float],
        distribution_distance: float,
        anomaly_score: float,
        anomaly_components: Dict[str, float],
        quality_warnings: List[str],
        metadata: Dict[str, Any],
    ):
        """
        Create a RiskReport.

        Args:
            job_id: Parent job identifier
            business_type: Taxpayer business type
            risk_score: Overall risk score
            label_distribution: Observed label distribution
            expected_distribution: Expected distribution for business type
            distribution_distance: Distance between observed and expected
            anomaly_score: Anomaly component score
            anomaly_components: Breakdown of anomaly indicators
            quality_warnings: Data quality warnings
            metadata: Additional report metadata
        """
        self._job_id = job_id
        self._business_type = business_type
        self._risk_score = risk_score
        self._label_distribution = label_distribution
        self._expected_distribution = expected_distribution
        self._distribution_distance = distribution_distance
        self._anomaly_score = anomaly_score
        self._anomaly_components = anomaly_components
        self._quality_warnings = quality_warnings
        self._metadata = metadata

    # Properties
    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def business_type(self) -> str:
        return self._business_type

    @property
    def risk_score(self) -> RiskScore:
        return self._risk_score

    @property
    def risk_level(self) -> str:
        return self._risk_score.risk_level

    @property
    def label_distribution(self) -> Dict[str, float]:
        return self._label_distribution.copy()

    @property
    def expected_distribution(self) -> Dict[str, float]:
        return self._expected_distribution.copy()

    @property
    def distribution_distance(self) -> float:
        return self._distribution_distance

    @property
    def anomaly_score(self) -> float:
        return self._anomaly_score

    @property
    def anomaly_components(self) -> Dict[str, float]:
        return self._anomaly_components.copy()

    @property
    def quality_warnings(self) -> List[str]:
        return self._quality_warnings.copy()

    @property
    def metadata(self) -> Dict[str, Any]:
        return self._metadata.copy()

    # Business logic
    def is_high_risk(self, threshold: float = 50.0) -> bool:
        """Check if risk is above threshold"""
        return self._risk_score.is_high_risk(threshold)

    def has_quality_issues(self) -> bool:
        """Check if report has quality warnings"""
        return len(self._quality_warnings) > 0

    def get_top_anomalies(self, limit: int = 3) -> List[tuple[str, float]]:
        """Get top anomaly components by score"""
        sorted_anomalies = sorted(
            self._anomaly_components.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_anomalies[:limit]

    def get_distribution_deviation(self, label: str) -> float:
        """Get deviation for specific label"""
        observed = self._label_distribution.get(label, 0.0)
        expected = self._expected_distribution.get(label, 0.0)
        return observed - expected

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "job_id": self._job_id,
            "business_type": self._business_type,
            "risk_percent": self._risk_score.score,
            "risk_level": self._risk_score.risk_level,
            "breakdown": {
                "distribution_distance": self._distribution_distance,
                "anomaly_score": self._anomaly_score,
                "anomaly_components": self._anomaly_components,
            },
            "label_distribution": self._label_distribution,
            "expected_distribution": self._expected_distribution,
            "quality_warnings": self._quality_warnings,
            "metadata": self._metadata,
        }

    def __repr__(self) -> str:
        return (
            f"RiskReport(job_id='{self._job_id}', "
            f"risk_score={self._risk_score}, "
            f"risk_level={self._risk_score.risk_level})"
        )
