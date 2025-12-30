"""
Inspect File Use Case - Preview file structure without full processing
"""

import pandas as pd
from typing import Dict, Any, List, BinaryIO
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class InspectFileUseCase:
    """Inspects uploaded files and returns metadata + preview"""

    def execute(self, file_stream: BinaryIO, filename: str) -> Dict[str, Any]:
        """
        Inspect file and return structure metadata + preview

        Args:
            file_stream: File content stream
            filename: Original filename

        Returns:
            Dictionary with file metadata, sheet info, and preview
        """
        file_ext = Path(filename).suffix.lower()

        if file_ext == '.csv':
            return self._inspect_csv(file_stream, filename)
        elif file_ext in ['.xlsx', '.xls']:
            return self._inspect_excel(file_stream, filename)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")

    def _inspect_csv(self, file_stream: BinaryIO, filename: str) -> Dict[str, Any]:
        """Inspect CSV file"""
        try:
            # Read first 20 rows for preview
            df_preview = pd.read_csv(file_stream, nrows=20, encoding='utf-8')
            file_stream.seek(0)

            # Get total row count (rough estimate)
            df_full = pd.read_csv(file_stream, encoding='utf-8')
            total_rows = len(df_full)

            return {
                "file_type": "csv",
                "filename": filename,
                "sheets": [{
                    "name": "Sheet1",
                    "index": 0,
                    "n_rows": total_rows,
                    "n_cols": len(df_preview.columns),
                    "columns": df_preview.columns.tolist()
                }],
                "default_sheet": "Sheet1",
                "preview": {
                    "sheet_name": "Sheet1",
                    "columns": df_preview.columns.tolist(),
                    "rows": df_preview.head(5).values.tolist(),
                    "n_rows_total": total_rows
                },
                "warnings": []
            }
        except Exception as e:
            logger.error(f"Error inspecting CSV: {str(e)}")
            raise ValueError(f"Failed to read CSV file: {str(e)}")

    def _inspect_excel(self, file_stream: BinaryIO, filename: str) -> Dict[str, Any]:
        """Inspect Excel file (handles multi-sheet)"""
        try:
            excel_file = pd.ExcelFile(file_stream, engine='openpyxl')
            sheets_info = []
            warnings = []

            # Inspect each sheet
            for idx, sheet_name in enumerate(excel_file.sheet_names):
                try:
                    # Read full sheet to get row count
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)

                    # Check if sheet is empty or header-only
                    if len(df) == 0:
                        warnings.append(f"Sheet '{sheet_name}' is empty")
                        continue
                    elif len(df) == 1:
                        warnings.append(f"Sheet '{sheet_name}' contains only header row")

                    sheets_info.append({
                        "name": sheet_name,
                        "index": idx,
                        "n_rows": len(df),
                        "n_cols": len(df.columns),
                        "columns": df.columns.tolist()
                    })
                except Exception as e:
                    warnings.append(f"Error reading sheet '{sheet_name}': {str(e)}")
                    logger.warning(f"Sheet '{sheet_name}' failed to read: {str(e)}")

            if not sheets_info:
                raise ValueError("No readable sheets found in Excel file")

            # Get preview from first non-empty sheet
            default_sheet = sheets_info[0]["name"]
            df_preview = pd.read_excel(excel_file, sheet_name=default_sheet, nrows=5)

            return {
                "file_type": "xlsx",
                "filename": filename,
                "sheets": sheets_info,
                "default_sheet": default_sheet,
                "preview": {
                    "sheet_name": default_sheet,
                    "columns": df_preview.columns.tolist(),
                    "rows": df_preview.values.tolist(),
                    "n_rows_total": sheets_info[0]["n_rows"]
                },
                "warnings": warnings
            }
        except Exception as e:
            logger.error(f"Error inspecting Excel: {str(e)}")
            raise ValueError(f"Failed to read Excel file: {str(e)}")
