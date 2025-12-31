from __future__ import annotations
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import joblib

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset_csv", required=True)
    ap.add_argument("--model_out", default="aurora_invoice_model.joblib")
    ap.add_argument("--min_df", type=int, default=2)
    ap.add_argument("--test_size", type=float, default=0.15)
    ap.add_argument("--min_label_count", type=int, default=5, help="Minimum count for a label to be kept (others go to __OTHER__)")
    args = ap.parse_args()

    df = pd.read_csv(args.dataset_csv)
    df = df[df["invoice_text_norm"].astype(str).str.len() > 0].copy()

    # For v0, we train on pattern-labeled + fallback labels. You can later replace with human-validated labels.
    X = df["invoice_text_norm"].astype(str)
    y_raw = df["primary_label_id"].astype(str)

    # Collapse rare labels into __OTHER__ to avoid stratification issues
    label_counts = y_raw.value_counts()
    rare_labels = label_counts[label_counts < args.min_label_count].index
    y = y_raw.apply(lambda lbl: "__OTHER__" if lbl in rare_labels else lbl)

    print(f"Total samples: {len(df)}")
    print(f"Unique labels (after collapsing rare): {y.nunique()}")
    print(f"Rare labels collapsed: {len(rare_labels)}")

    # Try stratified split, but fall back to regular split if still issues
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42, stratify=y)
    except ValueError as e:
        print(f"Warning: Stratification failed ({e}). Using regular split.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size, random_state=42)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=args.min_df)),
        ("clf", LinearSVC())
    ])

    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    print(classification_report(y_test, y_pred, zero_division=0))

    joblib.dump(pipe, args.model_out)
    print(f"Saved model to: {args.model_out}")

if __name__ == "__main__":
    main()
