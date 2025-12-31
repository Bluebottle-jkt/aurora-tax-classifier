from __future__ import annotations
import argparse, json
import pandas as pd
from src.utils import read_invoice_xlsx, normalize_text
from src.labeler import Ontology, InvoiceLabeler

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ontology", required=True)
    ap.add_argument("--faktur_keluaran", required=True)
    ap.add_argument("--faktur_masukan", required=True)
    ap.add_argument("--out_csv", default="dataset_labeled.csv")
    ap.add_argument("--out_new_nodes", default="new_nodes_append.json")
    args = ap.parse_args()

    onto = Ontology.load(args.ontology)
    lab = InvoiceLabeler(onto)

    out_df = read_invoice_xlsx(args.faktur_keluaran)
    out_df["invoice_side"] = "output"

    in_df = read_invoice_xlsx(args.faktur_masukan)
    in_df["invoice_side"] = "input"

    df = pd.concat([out_df, in_df], ignore_index=True)
    results = []
    new_nodes = []

    for _, row in df.iterrows():
        text = normalize_text(row["invoice_text_norm"])
        side = row["invoice_side"]
        res = lab.label_one(text, side)
        results.append({
            "invoice_side": res.invoice_side,
            "invoice_text": row["invoice_text"],
            "invoice_text_norm": text,
            "primary_label_id": res.primary_label_id,
            "ancestor_path": " > ".join(res.ancestor_path),
            "confidence": res.confidence_0_100,
            "evidence_terms": "|".join(res.evidence_terms),
            "leaf_generator_rule_id": res.leaf_generator_rule_id or ""
        })
        if res.suggested_new_leaf_node:
            new_nodes.append(res.suggested_new_leaf_node)

    out = pd.DataFrame(results)
    out.to_csv(args.out_csv, index=False)

    # de-duplicate new nodes by id
    seen = set()
    uniq = []
    for n in new_nodes:
        if n["id"] not in seen:
            uniq.append(n); seen.add(n["id"])
    with open(args.out_new_nodes, "w", encoding="utf-8") as f:
        json.dump(uniq, f, ensure_ascii=False, indent=2)

    print(f"Wrote {args.out_csv} with {len(out)} rows.")
    print(f"Wrote {args.out_new_nodes} with {len(uniq)} suggested new leaf nodes.")

if __name__ == "__main__":
    main()
