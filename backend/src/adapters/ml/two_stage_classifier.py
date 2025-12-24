"""
Two-Stage Classifier using separate models for Fiscal Correction and Tax Object Classification
"""

import joblib
from pathlib import Path
from typing import List, Dict
import re
from ...application.ports import ClassifierPort


class TwoStageClassifier(ClassifierPort):
    """
    Two-stage classifier that:
    1. First classifies fiscal corrections (koreksi fiskal)
    2. Then classifies tax objects (objek PPh)
    3. Combines results into unified probability distribution
    """

    # Label mapping from model outputs to expected system labels
    FISCAL_CORRECTION_MAP = {
        'Koreksi Fiskal Positif': 'Fiscal_Correction_Positive',
        'Koreksi Fiskal Negatif': 'Fiscal_Correction_Negative',
        'Tidak ada koreksi fiskal': None  # No fiscal correction
    }

    TAX_OBJECT_MAP = {
        'Non Objek': 'Non_Object',
        'Objek PPh Pasal 21': 'PPh21',
        'Objek PPh Pasal 22': 'PPh22',
        'Objek PPh Pasal 23 - Bunga': 'PPh23_Bunga',
        'Objek PPh Pasal 23 - Dividen': 'PPh23_Dividen',
        'Objek PPh Pasal 23 - Hadiah Penghargaan': 'PPh23_Hadiah',
        'Objek PPh Pasal 23 - Jasa': 'PPh23_Jasa',
        'Objek PPh Pasal 23 - Royalti': 'PPh23_Royalti',
        'Objek PPh Pasal 23 - Sewa': 'PPh23_Sewa',
        'Objek PPh Pasal 26': 'PPh26',
        'Objek PPh Pasal 4(2) - Dividen': 'PPh4_2_Final',  # Map to PPh4_2_Final
        'Objek PPh Pasal 4(2) - Jasa Konstruksi': 'PPh4_2_Final',
        'Objek PPh Pasal 4(2) - Sewa': 'PPh4_2_Final',
    }

    # All valid labels in the system
    ALL_LABELS = [
        "PPh21", "PPh22", "PPh23_Bunga", "PPh23_Dividen", "PPh23_Hadiah",
        "PPh23_Jasa", "PPh23_Royalti", "PPh23_Sewa", "PPh26", "PPN",
        "PPh4_2_Final", "Fiscal_Correction_Positive", "Fiscal_Correction_Negative",
        "Non_Object"
    ]

    def __init__(
        self,
        fiscal_model_path: str = "models/koreksi_fiskal_lr.joblib",
        tax_object_model_path: str = "models/objek_pph_lr.joblib"
    ):
        """
        Initialize two-stage classifier.

        Args:
            fiscal_model_path: Path to fiscal correction model
            tax_object_model_path: Path to tax object classification model
        """
        self.fiscal_model_path = Path(fiscal_model_path)
        self.tax_object_model_path = Path(tax_object_model_path)
        self.fiscal_model = None
        self.tax_object_model = None
        self.version = "two-stage-v1.0"

        # Load models
        if self.fiscal_model_path.exists():
            self.fiscal_model = joblib.load(self.fiscal_model_path)
        else:
            raise FileNotFoundError(f"Fiscal correction model not found: {self.fiscal_model_path}")

        if self.tax_object_model_path.exists():
            self.tax_object_model = joblib.load(self.tax_object_model_path)
        else:
            raise FileNotFoundError(f"Tax object model not found: {self.tax_object_model_path}")

    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        """
        Predict probabilities using two-stage approach.

        Args:
            texts: List of account names

        Returns:
            List of {label: probability} dictionaries with unified labels
        """
        if not self.fiscal_model or not self.tax_object_model:
            raise ValueError("Models not loaded")

        # Preprocess all texts
        preprocessed = [self._preprocess(text) for text in texts]

        # Stage 1: Predict fiscal corrections
        fiscal_proba = self.fiscal_model.predict_proba(preprocessed)
        fiscal_labels = self.fiscal_model.classes_

        # Stage 2: Predict tax objects
        tax_object_proba = self.tax_object_model.predict_proba(preprocessed)
        tax_object_labels = self.tax_object_model.classes_

        # Combine results
        results = []
        for i in range(len(texts)):
            combined_probs = self._combine_predictions(
                fiscal_proba[i],
                fiscal_labels,
                tax_object_proba[i],
                tax_object_labels
            )
            results.append(combined_probs)

        return results

    def _combine_predictions(
        self,
        fiscal_probs: list,
        fiscal_labels: list,
        tax_object_probs: list,
        tax_object_labels: list
    ) -> Dict[str, float]:
        """
        Combine predictions from both models into unified probability distribution.

        Strategy:
        1. Map fiscal correction probabilities to system labels
        2. Map tax object probabilities to system labels
        3. Normalize to ensure probabilities sum to 1.0
        4. Handle special cases (e.g., PPN which may not be in either model)

        Args:
            fiscal_probs: Probabilities from fiscal correction model
            fiscal_labels: Labels from fiscal correction model
            tax_object_probs: Probabilities from tax object model
            tax_object_labels: Labels from tax object model

        Returns:
            Dictionary of {system_label: probability}
        """
        combined = {}

        # Process fiscal correction predictions
        for prob, label in zip(fiscal_probs, fiscal_labels):
            mapped_label = self.FISCAL_CORRECTION_MAP.get(label)
            if mapped_label:  # Only add if there's a mapping (skip "Tidak ada koreksi fiskal")
                combined[mapped_label] = combined.get(mapped_label, 0.0) + float(prob)

        # Process tax object predictions
        for prob, label in zip(tax_object_probs, tax_object_labels):
            mapped_label = self.TAX_OBJECT_MAP.get(label)
            if mapped_label:
                # For PPh4_2_Final, sum all variations
                combined[mapped_label] = combined.get(mapped_label, 0.0) + float(prob)

        # Add small probability for PPN if not present (not in either model)
        if 'PPN' not in combined:
            combined['PPN'] = 0.01

        # Normalize probabilities to sum to 1.0
        total = sum(combined.values())
        if total > 0:
            combined = {label: prob / total for label, prob in combined.items()}

        # Ensure all system labels are present (with 0 probability if not predicted)
        for label in self.ALL_LABELS:
            if label not in combined:
                combined[label] = 0.0

        return combined

    def get_version(self) -> str:
        """Get model version"""
        return self.version

    @staticmethod
    def _preprocess(text: str) -> str:
        """
        Preprocess Indonesian text.

        Args:
            text: Raw account name text

        Returns:
            Preprocessed text
        """
        # Lowercase
        text = text.lower()

        # Remove special characters (keep only letters, numbers, spaces)
        text = re.sub(r'[^a-z0-9\s]', ' ', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text
