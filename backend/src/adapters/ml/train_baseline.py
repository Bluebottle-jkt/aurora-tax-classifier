"""
Train baseline TF-IDF classifier
"""

import json
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import re


def preprocess(text: str) -> str:
    """Preprocess text"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def train():
    """Train baseline model"""
    # Load seed corpus
    corpus_path = Path("data/seed_corpus.jsonl")
    texts = []
    labels = []

    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            texts.append(preprocess(item['text']))
            labels.append(item['label'])

    # Create pipeline
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=100, ngram_range=(1, 2))),
        ('clf', LogisticRegression(multi_class='multinomial', max_iter=1000))
    ])

    # Train
    model.fit(texts, labels)

    # Save
    model_path = Path("models/baseline_model.pkl")
    model_path.parent.mkdir(exist_ok=True)
    joblib.dump(model, model_path)

    print(f"[OK] Model trained and saved to {model_path}")
    print(f"  Labels: {model.classes_}")
    print(f"  Training samples: {len(texts)}")


if __name__ == "__main__":
    train()
