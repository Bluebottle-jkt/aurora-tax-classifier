"""
TF-IDF + Logistic Regression Classifier
"""

import joblib
import json
from pathlib import Path
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re
from ...application.ports import ClassifierPort


class TfidfClassifier(ClassifierPort):
    """TF-IDF + Logistic Regression classifier"""

    def __init__(self, model_path: str = "models/baseline_model.pkl"):
        self.model_path = Path(model_path)
        self.model = None
        self.version = "baseline-v1.0"

        if self.model_path.exists():
            self.model = joblib.load(self.model_path)

    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        """Predict probabilities"""
        if not self.model:
            raise ValueError("Model not trained")

        # Preprocess
        preprocessed = [self._preprocess(text) for text in texts]

        # Predict
        proba = self.model.predict_proba(preprocessed)
        labels = self.model.classes_

        # Convert to list of dicts
        results = []
        for prob_array in proba:
            prob_dict = {label: float(prob) for label, prob in zip(labels, prob_array)}
            results.append(prob_dict)

        return results

    def get_version(self) -> str:
        return self.version

    @staticmethod
    def _preprocess(text: str) -> str:
        """Preprocess Indonesian text"""
        # Lowercase
        text = text.lower()

        # Remove special characters
        text = re.sub(r'[^a-z0-9\s]', ' ', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text
