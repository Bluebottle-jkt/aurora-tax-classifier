from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd

def read_invoice_xlsx(path: str, text_col: str = "nama barang") -> pd.DataFrame:
    """
    Read *all sheets* in an XLSX and return a normalized dataframe with:
      - invoice_text: string
      - sheet: sheet name
      - row_id: row index within concatenated df
    """
    xls = pd.ExcelFile(path)
    frames = []
    for sh in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sh)
        if text_col not in df.columns:
            # Try case-insensitive match
            cols = {c.lower(): c for c in df.columns}
            if text_col.lower() in cols:
                df = df.rename(columns={cols[text_col.lower()]: text_col})
            else:
                raise ValueError(f"Column '{text_col}' not found in sheet '{sh}'. Found: {list(df.columns)}")
        out = pd.DataFrame({
            "invoice_text": df[text_col].astype(str).fillna(""),
            "sheet": sh
        })
        frames.append(out)
    out_df = pd.concat(frames, ignore_index=True)
    out_df["row_id"] = out_df.index.astype(int)
    # Basic normalization
    out_df["invoice_text_norm"] = out_df["invoice_text"].astype(str).str.strip()
    return out_df

def normalize_text(s: str) -> str:
    s = (s or "").strip()
    s = re.sub(r"\s+", " ", s)
    return s
