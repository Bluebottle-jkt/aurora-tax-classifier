"""
Prediction Row Entity - represents a single GL row prediction.
"""

from typing import Optional, List, Dict, Any
from ..value_objects import TaxObjectLabel, ConfidenceScore


class PredictionRow:
    """
    Represents a single prediction row for a GL entry.
    """

    def __init__(
        self,
        row_id: str,
        job_id: str,
        row_index: int,
        account_name: str,
        predicted_label: TaxObjectLabel,
        confidence: ConfidenceScore,
        explanation: str,
        signals: List[str],
        account_code: Optional[str] = None,
        amount: Optional[float] = None,
        date: Optional[str] = None,
        debit_credit: Optional[str] = None,
        counterparty: Optional[str] = None,
        probability_distribution: Optional[Dict[str, float]] = None,
        top_terms: Optional[List[str]] = None,
        nearest_examples: Optional[List[Dict[str, Any]]] = None,
    ):
        """
        Create a PredictionRow.

        Args:
            row_id: Unique row identifier
            job_id: Parent job identifier
            row_index: Index in original file (0-based)
            account_name: GL account name (required field)
            predicted_label: Predicted tax object label
            confidence: Confidence score
            explanation: Human-readable explanation
            signals: Risk/quality signals
            account_code: GL account code
            amount: Transaction amount
            date: Transaction date
            debit_credit: Debit or credit indicator
            counterparty: Transaction counterparty
            probability_distribution: Full probability distribution
            top_terms: Top contributing TF-IDF terms
            nearest_examples: Nearest training examples
        """
        self._row_id = row_id
        self._job_id = job_id
        self._row_index = row_index
        self._account_name = account_name
        self._predicted_label = predicted_label
        self._confidence = confidence
        self._explanation = explanation
        self._signals = signals or []
        self._account_code = account_code
        self._amount = amount
        self._date = date
        self._debit_credit = debit_credit
        self._counterparty = counterparty
        self._probability_distribution = probability_distribution or {}
        self._top_terms = top_terms or []
        self._nearest_examples = nearest_examples or []

    # Properties
    @property
    def row_id(self) -> str:
        return self._row_id

    @property
    def job_id(self) -> str:
        return self._job_id

    @property
    def row_index(self) -> int:
        return self._row_index

    @property
    def account_name(self) -> str:
        return self._account_name

    @property
    def predicted_label(self) -> TaxObjectLabel:
        return self._predicted_label

    @property
    def confidence(self) -> ConfidenceScore:
        return self._confidence

    @property
    def explanation(self) -> str:
        return self._explanation

    @property
    def signals(self) -> List[str]:
        return self._signals.copy()

    @property
    def account_code(self) -> Optional[str]:
        return self._account_code

    @property
    def amount(self) -> Optional[float]:
        return self._amount

    @property
    def date(self) -> Optional[str]:
        return self._date

    @property
    def debit_credit(self) -> Optional[str]:
        return self._debit_credit

    @property
    def counterparty(self) -> Optional[str]:
        return self._counterparty

    @property
    def probability_distribution(self) -> Dict[str, float]:
        return self._probability_distribution.copy()

    @property
    def top_terms(self) -> List[str]:
        return self._top_terms.copy()

    @property
    def nearest_examples(self) -> List[Dict[str, Any]]:
        return self._nearest_examples.copy()

    # Business logic
    def is_high_confidence(self, threshold: float = 80.0) -> bool:
        """Check if prediction is high confidence"""
        return self._confidence.is_high_confidence(threshold)

    def is_low_confidence(self, threshold: float = 50.0) -> bool:
        """Check if prediction is low confidence"""
        return self._confidence.is_low_confidence(threshold)

    def has_quality_issues(self) -> bool:
        """Check if row has quality issues"""
        quality_signals = [
            "short_text",
            "vague_text",
            "missing_amount",
            "invalid_date",
        ]
        return any(signal in self._signals for signal in quality_signals)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "row_id": self._row_id,
            "job_id": self._job_id,
            "row_index": self._row_index,
            "account_name": self._account_name,
            "account_code": self._account_code,
            "amount": self._amount,
            "date": self._date,
            "debit_credit": self._debit_credit,
            "counterparty": self._counterparty,
            "predicted_tax_object": str(self._predicted_label),
            "confidence_percent": self._confidence.score,
            "explanation": self._explanation,
            "signals": self._signals,
            "probability_distribution": self._probability_distribution,
            "top_terms": self._top_terms,
            "nearest_examples": self._nearest_examples,
        }

    def __repr__(self) -> str:
        return (
            f"PredictionRow(row_id='{self._row_id}', "
            f"label={self._predicted_label}, "
            f"confidence={self._confidence})"
        )
