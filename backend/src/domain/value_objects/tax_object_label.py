"""
Tax Object Label Value Object.
Represents a valid Indonesian tax object classification.
"""

from typing import List
from ..errors import InvalidTaxObjectLabelError


class TaxObjectLabel:
    """
    Immutable value object representing a tax object label.
    Enforces valid label taxonomy.
    """

    # Valid tax object labels (can be loaded from config in production)
    VALID_LABELS: List[str] = [
        "PPh21",
        "PPh22",
        "PPh23_Bunga",
        "PPh23_Dividen",
        "PPh23_Hadiah",
        "PPh23_Jasa",
        "PPh23_Royalti",
        "PPh23_Sewa",
        "PPh26",
        "PPN",
        "PPh4_2_Final",
        "Fiscal_Correction_Positive",
        "Fiscal_Correction_Negative",
        "Non_Object",
    ]

    def __init__(self, label: str):
        """
        Create a TaxObjectLabel.

        Args:
            label: The tax object label string

        Raises:
            InvalidTaxObjectLabelError: If label is not in valid taxonomy
        """
        if not isinstance(label, str):
            raise InvalidTaxObjectLabelError(f"Label must be a string, got {type(label)}")

        label = label.strip()

        if not label:
            raise InvalidTaxObjectLabelError("Label cannot be empty")

        if label not in self.VALID_LABELS:
            raise InvalidTaxObjectLabelError(
                f"Invalid label '{label}'. Valid labels: {', '.join(self.VALID_LABELS)}"
            )

        self._label = label

    @property
    def label(self) -> str:
        """Get the label value"""
        return self._label

    def __str__(self) -> str:
        return self._label

    def __repr__(self) -> str:
        return f"TaxObjectLabel('{self._label}')"

    def __eq__(self, other) -> bool:
        if not isinstance(other, TaxObjectLabel):
            return False
        return self._label == other._label

    def __hash__(self) -> int:
        return hash(self._label)

    @classmethod
    def is_valid(cls, label: str) -> bool:
        """Check if a label string is valid without raising exception"""
        return label in cls.VALID_LABELS

    @classmethod
    def all_labels(cls) -> List[str]:
        """Get all valid labels"""
        return cls.VALID_LABELS.copy()
