from __future__ import annotations
import argparse
import json
import pandas as pd
import joblib
from src.utils import read_invoice_xlsx, normalize_text
from src.labeler import Ontology

def main():
    ap = argparse.ArgumentParser(
        description="Aurora v2 Invoice Classifier - Predict labels for invoice lines"
    )
    ap.add_argument("--xlsx_path", required=True, help="Path to input XLSX file")
    ap.add_argument(
        "--invoice_side",
        required=True,
        choices=["output", "input"],
        help="Invoice side: 'output' (faktur keluaran) or 'input' (faktur masukan)"
    )
    ap.add_argument(
        "--business_type_id",
        required=True,
        help="Business type ID (e.g., BT_GRABLIKE_ONDEMAND_SUPERAPP)"
    )
    ap.add_argument(
        "--ontology_path",
        default="ontology/ontology_grablike_v2.json",
        help="Path to ontology JSON file"
    )
    ap.add_argument(
        "--model_path",
        default="models/aurora_invoice_model.joblib",
        help="Path to trained model file"
    )
    ap.add_argument(
        "--out_csv",
        default="predictions.csv",
        help="Output CSV file path"
    )
    args = ap.parse_args()

    # Load ontology
    print(f"Loading ontology from {args.ontology_path}...")
    ontology = Ontology.load(args.ontology_path)

    # Create label_id -> label_name mapping
    label_map = {node["id"]: node.get("label", node["id"])
                 for node in ontology.ontology["nodes"]}

    # Load model
    print(f"Loading model from {args.model_path}...")
    model = joblib.load(args.model_path)

    # Read all sheets from XLSX
    print(f"Reading XLSX file: {args.xlsx_path}")
    df = read_invoice_xlsx(args.xlsx_path, text_col="nama barang")

    # Normalize text
    df["invoice_text_norm"] = df["invoice_text"].apply(normalize_text)

    # Filter out empty rows
    df = df[df["invoice_text_norm"].str.len() > 0].copy()

    if len(df) == 0:
        print("Warning: No valid invoice lines found after filtering empty rows!")
        df_out = pd.DataFrame(columns=[
            "row_id", "sheet", "invoice_text", "invoice_text_norm",
            "pred_label_id", "pred_label_name", "invoice_side", "business_type_id"
        ])
    else:
        # Predict labels
        print(f"Predicting labels for {len(df)} invoice lines...")
        predictions = model.predict(df["invoice_text_norm"])

        # Map label IDs to label names
        label_names = [label_map.get(lid, lid) for lid in predictions]

        # Create output dataframe
        df_out = pd.DataFrame({
            "row_id": df["row_id"].values,
            "sheet": df["sheet"].values,
            "invoice_text": df["invoice_text"].values,
            "invoice_text_norm": df["invoice_text_norm"].values,
            "pred_label_id": predictions,
            "pred_label_name": label_names,
            "invoice_side": args.invoice_side,
            "business_type_id": args.business_type_id
        })

    # Save output
    df_out.to_csv(args.out_csv, index=False)
    print(f"\nSaved predictions to: {args.out_csv}")
    print(f"Total rows processed: {len(df_out)}")

    # Print summary statistics
    if len(df_out) > 0:
        print("\n=== Label Distribution ===")
        label_counts = df_out["pred_label_name"].value_counts()
        for label, count in label_counts.head(10).items():
            pct = 100 * count / len(df_out)
            print(f"{label:50s} : {count:5d} ({pct:5.1f}%)")

        if len(label_counts) > 10:
            print(f"... and {len(label_counts) - 10} more labels")

if __name__ == "__main__":
    main()
