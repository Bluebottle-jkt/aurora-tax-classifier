# Aurora v2 - Invoice-Based Tax Classifier

Aurora v2 is an invoice line-item tax classifier for Indonesian businesses, specifically designed for on-demand platform services (Grab-like model). It classifies invoice text from `nama barang` column into a detailed tax ontology covering PPN Keluaran, PPN Masukan, and related PPh categories.

## Features

- **Multi-sheet XLSX support**: Reads all sheets from Excel files
- **Invoice-side aware**: Handles both output (faktur keluaran) and input (faktur masukan) invoices
- **Business type alignment**: Supports KBLI-based business type selection
- **Ontology-driven labeling**: Uses hierarchical tax ontology with regex patterns
- **Auto-leaf generation**: Suggests new leaf nodes for unmatchedpatterns
- **TF-IDF + LinearSVC classifier**: Baseline ML model for label prediction
- **CLI-based**: No Streamlit dependency, pure command-line interface

## Directory Structure

```
aurora_v2/
├── ontology/
│   └── ontology_grablike_v2.json    # Tax ontology with patterns
├── src/
│   ├── utils.py                      # XLSX reader and text normalization
│   └── labeler.py                    # Ontology loader and pattern matcher
├── models/
│   └── aurora_invoice_model.joblib   # Trained model (generated)
├── build_dataset.py                  # Create labeled dataset
├── train_model.py                    # Train classifier model
├── predict.py                        # Run inference on new invoices
└── README.md                         # This file
```

## Installation

From the repository root:

```bash
cd aurora_v2
pip install -r ../requirements.txt
```

Required dependencies:
- pandas >= 2.0
- openpyxl >= 3.1
- scikit-learn >= 1.3
- joblib >= 1.3
- regex >= 2024.5.15

## Usage

### Step 1: Build Labeled Dataset

Create a labeled dataset from your invoice XLSX files:

```bash
python build_dataset.py \
  --ontology ontology/ontology_grablike_v2.json \
  --faktur_keluaran path/to/contoh_detil_faktur.xlsx \
  --faktur_masukan path/to/contoh_detil_faktur_pajak_masukan.xlsx \
  --out_csv dataset_labeled.csv \
  --out_new_nodes new_nodes_append.json
```

**Outputs:**
- `dataset_labeled.csv`: Combined dataset with pattern-matched labels
- `new_nodes_append.json`: Suggested new leaf nodes for unmatched patterns

### Step 2: Train Model

Train the TF-IDF + LinearSVC classifier:

```bash
python train_model.py \
  --dataset_csv dataset_labeled.csv \
  --model_out models/aurora_invoice_model.joblib \
  --min_df 2 \
  --test_size 0.15
```

**Outputs:**
- `models/aurora_invoice_model.joblib`: Trained model
- Classification report printed to console

### Step 3: Predict on New Invoices

Run inference on new invoice files:

**For Output Invoices (Faktur Keluaran):**
```bash
python predict.py \
  --xlsx_path path/to/new_faktur_keluaran.xlsx \
  --invoice_side output \
  --business_type_id BT_GRABLIKE_ONDEMAND_SUPERAPP \
  --ontology_path ontology/ontology_grablike_v2.json \
  --model_path models/aurora_invoice_model.joblib \
  --out_csv predictions_output.csv
```

**For Input Invoices (Faktur Masukan):**
```bash
python predict.py \
  --xlsx_path path/to/new_faktur_masukan.xlsx \
  --invoice_side input \
  --business_type_id BT_GRABLIKE_ONDEMAND_SUPERAPP \
  --ontology_path ontology/ontology_grablike_v2.json \
  --model_path models/aurora_invoice_model.joblib \
  --out_csv predictions_input.csv
```

**Output CSV Columns:**
- `row_id`: Row index
- `sheet`: Sheet name from XLSX
- `invoice_text`: Original text from `nama barang`
- `invoice_text_norm`: Normalized text
- `pred_label_id`: Predicted label ID (e.g., `REV_MGMT_FEE_FOOD`)
- `pred_label_name`: Human-readable label name
- `invoice_side`: `output` or `input`
- `business_type_id`: Selected business type

## Business Types

Available business type IDs:

- `BT_GRABLIKE_ONDEMAND_SUPERAPP`: On-demand Superapp (mobility + food + delivery)
- `BT_ONDEMAND_MOBILITY_ONLY`: Mobility-only (ride-hailing)
- `BT_ONDEMAND_DELIVERY_ONLY`: Delivery/logistics only
- `BT_PLATFORM_DIGITAL_ONLY`: Digital platform only

## Ontology Structure

The ontology is hierarchical:

```
TAX
├── PPN
│   ├── PPN_OUTPUT (Faktur Keluaran)
│   │   ├── PPN_OUTPUT_REV (Revenue Objects)
│   │   │   ├── REV_PLATFORM (Platform Fees)
│   │   │   │   ├── REV_MGMT_FEE_FOOD
│   │   │   │   ├── REV_MGMT_FEE_MOBILITY
│   │   │   │   └── ...
│   │   │   ├── REV_ADS (Advertising)
│   │   │   └── REV_DEVICES (Hardware Sales)
│   ├── PPN_INPUT (Faktur Masukan)
│   │   ├── PPN_INPUT_COST (Cost Objects)
│   │   │   ├── COST_PLATFORM_IT
│   │   │   ├── COST_MARKETING_ADS
│   │   │   ├── COST_DEVICES
│   │   │   └── COST_GENERAL
│   └── ...
├── PPh
└── PPNBM
```

## How It Works

1. **Pattern Matching**: The labeler first tries to match invoice text against regex patterns in the ontology
2. **Leaf Generation**: If no match, it applies leaf generator rules to suggest new nodes
3. **Fallback**: If still no match, assigns fallback labels (`REV_PLATFORM` for output, `COST_GENERAL` for input)
4. **ML Training**: The labeled dataset is used to train a TF-IDF + LinearSVC model
5. **Prediction**: New invoices are classified using the trained model

## Important Notes

- **Column Name**: All XLSX files must have a column named `nama barang` (case-insensitive)
- **Multi-sheet**: The system automatically reads all sheets from XLSX files
- **Empty Rows**: Empty or NaN values are filtered out during processing
- **Deterministic**: All outputs are deterministic and reproducible

## Extending the Ontology

To add new labels:

1. Edit `ontology/ontology_grablike_v2.json`
2. Add new nodes with patterns in the `crosswalk` section
3. Optionally add leaf generator rules for auto-extension
4. Rebuild dataset and retrain model

## Example Workflow

```bash
# Navigate to aurora_v2 directory
cd d:\TaxObjectFinder\aurora-tax-classifier\aurora_v2

# Build dataset
python build_dataset.py \
  --ontology ontology/ontology_grablike_v2.json \
  --faktur_keluaran ../data/contoh_detil_faktur.xlsx \
  --faktur_masukan ../data/contoh_detil_faktur_pajak_masukan.xlsx \
  --out_csv dataset_labeled.csv \
  --out_new_nodes new_nodes_append.json

# Train model
python train_model.py \
  --dataset_csv dataset_labeled.csv \
  --model_out models/aurora_invoice_model.joblib

# Predict on new files
python predict.py \
  --xlsx_path ../data/new_invoice.xlsx \
  --invoice_side output \
  --business_type_id BT_GRABLIKE_ONDEMAND_SUPERAPP \
  --out_csv predictions.csv
```

## Integration with Main Aurora App

Aurora v2 can be integrated into the main Aurora application as an additional feature:

- The CLI tools can be called from backend endpoints
- The ontology and model can be loaded in the FastAPI application
- Predictions can be displayed alongside existing tax classification

## License

Part of the Aurora Tax Classifier project.
