"""
Risk Policy - business rules for calculating dataset-level risk scores.
Pure domain logic, no framework dependencies.
"""

import math
from typing import Dict, List, Optional
from ..value_objects import RiskScore


class RiskPolicy:
    """
    Implements business-to-ledger compliance risk scoring.
    Uses Jensen-Shannon divergence + anomaly detection.
    """

    def __init__(
        self,
        distance_weight: float = 0.55,
        anomaly_weight: float = 0.45,
        high_correction_threshold: float = 0.15,
        high_non_object_threshold: float = 0.25,
        high_variance_threshold: float = 0.8,
        end_of_period_threshold: float = 0.30,
    ):
        """
        Initialize policy with configurable parameters.

        Args:
            distance_weight: Weight for distribution distance component
            anomaly_weight: Weight for anomaly component
            high_correction_threshold: Threshold for correction rate anomaly
            high_non_object_threshold: Threshold for non-object rate anomaly
            high_variance_threshold: Threshold for label variance
            end_of_period_threshold: Threshold for end-of-period clustering
        """
        self.distance_weight = distance_weight
        self.anomaly_weight = anomaly_weight
        self.high_correction_threshold = high_correction_threshold
        self.high_non_object_threshold = high_non_object_threshold
        self.high_variance_threshold = high_variance_threshold
        self.end_of_period_threshold = end_of_period_threshold

    @staticmethod
    def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Clamp value to range"""
        return max(min_val, min(max_val, value))

    def calculate(
        self,
        observed_distribution: Dict[str, float],
        expected_distribution: Dict[str, float],
        label_counts: Dict[str, int],
        total_rows: int,
        end_of_period_ratio: Optional[float] = None,
    ) -> tuple[RiskScore, Dict[str, float], float, float]:
        """
        Calculate risk score for a dataset.

        Args:
            observed_distribution: Observed label distribution (probabilities sum to 1)
            expected_distribution: Expected distribution for business type
            label_counts: Count of each label
            total_rows: Total number of rows
            end_of_period_ratio: Ratio of transactions in last 10 days of period

        Returns:
            Tuple of (RiskScore, anomaly_components, distance, anomaly_score)
        """
        # Calculate distribution distance (Jensen-Shannon divergence)
        js_distance = self._jensen_shannon_divergence(
            observed_distribution,
            expected_distribution
        )

        # Calculate anomaly components
        anomaly_components = self._calculate_anomalies(
            label_counts,
            total_rows,
            end_of_period_ratio
        )

        # Aggregate anomaly score
        anomaly_score = sum(anomaly_components.values()) / max(len(anomaly_components), 1)

        # Final risk score
        risk_raw = (
            self.distance_weight * js_distance +
            self.anomaly_weight * anomaly_score
        )

        risk_raw = self.clamp(risk_raw, 0.0, 1.0)
        risk_percent = round(risk_raw * 100, 1)

        return (
            RiskScore(risk_percent),
            anomaly_components,
            js_distance,
            anomaly_score
        )

    def _jensen_shannon_divergence(
        self,
        p: Dict[str, float],
        q: Dict[str, float]
    ) -> float:
        """
        Calculate Jensen-Shannon divergence between two distributions.
        JSD = 0.5 * KL(P || M) + 0.5 * KL(Q || M), where M = 0.5 * (P + Q)

        Args:
            p: First distribution
            q: Second distribution

        Returns:
            JSD value in [0, 1]
        """
        # Get all labels
        all_labels = set(p.keys()) | set(q.keys())

        # Smooth probabilities to avoid log(0)
        epsilon = 1e-10

        # Calculate M (midpoint distribution)
        m = {}
        for label in all_labels:
            p_val = p.get(label, 0.0) + epsilon
            q_val = q.get(label, 0.0) + epsilon
            m[label] = 0.5 * (p_val + q_val)

        # Calculate KL divergences
        kl_pm = self._kl_divergence(p, m, all_labels, epsilon)
        kl_qm = self._kl_divergence(q, m, all_labels, epsilon)

        # JSD
        jsd = 0.5 * kl_pm + 0.5 * kl_qm

        # Normalize to [0, 1] (max JSD for binary is log(2))
        normalized_jsd = jsd / math.log(2)

        return self.clamp(normalized_jsd, 0.0, 1.0)

    def _kl_divergence(
        self,
        p: Dict[str, float],
        q: Dict[str, float],
        labels: set,
        epsilon: float
    ) -> float:
        """Calculate Kullback-Leibler divergence KL(P || Q)"""
        kl = 0.0
        for label in labels:
            p_val = p.get(label, 0.0) + epsilon
            q_val = q.get(label, 0.0) + epsilon
            kl += p_val * math.log(p_val / q_val)
        return kl

    def _calculate_anomalies(
        self,
        label_counts: Dict[str, int],
        total_rows: int,
        end_of_period_ratio: Optional[float]
    ) -> Dict[str, float]:
        """
        Calculate various anomaly indicators.

        Returns:
            Dict of anomaly_name -> score (0-1)
        """
        anomalies = {}

        if total_rows == 0:
            return anomalies

        # High correction rate
        correction_count = (
            label_counts.get("Fiscal_Correction_Positive", 0) +
            label_counts.get("Fiscal_Correction_Negative", 0)
        )
        correction_rate = correction_count / total_rows
        if correction_rate > self.high_correction_threshold:
            anomalies["high_correction_rate"] = self.clamp(
                correction_rate / self.high_correction_threshold,
                0.0,
                1.0
            )

        # High non-object rate
        non_object_count = label_counts.get("Non_Object", 0)
        non_object_rate = non_object_count / total_rows
        if non_object_rate > self.high_non_object_threshold:
            anomalies["high_non_object_rate"] = self.clamp(
                non_object_rate / self.high_non_object_threshold,
                0.0,
                1.0
            )

        # High variance in labels (many labels with small counts)
        label_entropy = self._calculate_entropy(label_counts, total_rows)
        max_entropy = math.log(len(label_counts)) if len(label_counts) > 1 else 1.0
        normalized_entropy = label_entropy / max_entropy if max_entropy > 0 else 0.0

        if normalized_entropy > self.high_variance_threshold:
            anomalies["high_label_variance"] = normalized_entropy

        # End-of-period clustering (if date info available)
        if end_of_period_ratio is not None and end_of_period_ratio > self.end_of_period_threshold:
            anomalies["end_of_period_clustering"] = self.clamp(
                end_of_period_ratio / self.end_of_period_threshold,
                0.0,
                1.0
            )

        return anomalies

    def _calculate_entropy(self, counts: Dict[str, int], total: int) -> float:
        """Calculate Shannon entropy of distribution"""
        if total == 0:
            return 0.0

        entropy = 0.0
        for count in counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log(p)

        return entropy
