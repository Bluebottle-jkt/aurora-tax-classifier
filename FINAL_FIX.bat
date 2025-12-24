@echo off
REM ============================================================================
REM AURORA - FINAL COMPREHENSIVE FIX
REM Fixes ALL issues including column mapping
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - Final Comprehensive Fix
echo ========================================================================
echo.

cd /d "%~dp0"

echo This script will fix:
echo   1. JSON format in seed_corpus.jsonl
echo   2. Missing TypeScript configs
echo   3. Missing port interface files
echo   4. Missing DTO files
echo   5. Config parameter mismatches
echo   6. Unused Sastrawi import
echo   7. Column name mapping (description -^> account_name)
echo   8. Train ML model
echo.

echo Starting fixes...
echo.

REM Fix 1: seed_corpus.jsonl
echo [FIX 1/8] Fixing seed_corpus.jsonl format...
python << EOF
import json
seed_data = [
    {'text': 'gaji karyawan', 'label': 'PPh21'},
    {'text': 'salary pegawai bulanan', 'label': 'PPh21'},
    {'text': 'tunjangan hari raya THR', 'label': 'PPh21'},
    {'text': 'bonus karyawan', 'label': 'PPh21'},
    {'text': 'upah tenaga kerja', 'label': 'PPh21'},
    {'text': 'pembayaran impor barang', 'label': 'PPh22'},
    {'text': 'pembelian barang pemerintah', 'label': 'PPh22'},
    {'text': 'bunga deposito bank', 'label': 'PPh23_Bunga'},
    {'text': 'bunga pinjaman', 'label': 'PPh23_Bunga'},
    {'text': 'dividen saham', 'label': 'PPh23_Dividen'},
    {'text': 'pembagian dividen', 'label': 'PPh23_Dividen'},
    {'text': 'hadiah undian', 'label': 'PPh23_Hadiah'},
    {'text': 'hadiah lomba', 'label': 'PPh23_Hadiah'},
    {'text': 'jasa konsultan', 'label': 'PPh23_Jasa'},
    {'text': 'jasa profesi akuntan', 'label': 'PPh23_Jasa'},
    {'text': 'jasa notaris', 'label': 'PPh23_Jasa'},
    {'text': 'jasa pengacara', 'label': 'PPh23_Jasa'},
    {'text': 'jasa teknisi', 'label': 'PPh23_Jasa'},
    {'text': 'royalti paten', 'label': 'PPh23_Royalti'},
    {'text': 'royalti merek', 'label': 'PPh23_Royalti'},
    {'text': 'sewa gedung kantor', 'label': 'PPh23_Sewa'},
    {'text': 'sewa kendaraan', 'label': 'PPh23_Sewa'},
    {'text': 'sewa alat berat', 'label': 'PPh23_Sewa'},
    {'text': 'bunga non resident', 'label': 'PPh26'},
    {'text': 'dividen luar negeri', 'label': 'PPh26'},
    {'text': 'pajak pertambahan nilai', 'label': 'PPN'},
    {'text': 'PPN masukan', 'label': 'PPN'},
    {'text': 'PPN keluaran', 'label': 'PPN'},
    {'text': 'sewa tanah bangunan', 'label': 'PPh4_2_Final'},
    {'text': 'penghasilan konstruksi', 'label': 'PPh4_2_Final'},
    {'text': 'koreksi fiskal positif', 'label': 'Fiscal_Correction_Positive'},
    {'text': 'koreksi fiskal negatif', 'label': 'Fiscal_Correction_Negative'},
    {'text': 'biaya entertainment', 'label': 'Fiscal_Correction_Positive'},
    {'text': 'biaya representasi', 'label': 'Fiscal_Correction_Positive'},
    {'text': 'pendapatan bunga', 'label': 'Non_Object'},
    {'text': 'biaya listrik', 'label': 'Non_Object'},
    {'text': 'biaya telepon', 'label': 'Non_Object'},
    {'text': 'biaya air', 'label': 'Non_Object'},
]
with open('backend/data/seed_corpus.jsonl', 'w', encoding='utf-8') as f:
    for item in seed_data:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')
print('[OK] seed_corpus.jsonl')
EOF

REM Fix 2: Frontend configs
echo [FIX 2/8] Creating frontend config files...
if not exist frontend\tsconfig.node.json (
    echo {"compilerOptions":{"composite":true,"skipLibCheck":true,"module":"ESNext","moduleResolution":"bundler","allowSyntheticDefaultImports":true},"include":["vite.config.ts"]} > frontend\tsconfig.node.json
)
if not exist frontend\postcss.config.js (
    echo export default {plugins: {tailwindcss: {},autoprefixer: {}}} > frontend\postcss.config.js
)

REM Fix 3: scoring.json
echo [FIX 3/8] Fixing scoring.json...
python << EOF
import json
config = {
    'confidence': {
        'p_max_weight': 0.65,
        'margin_weight': 0.35,
        'short_text_penalty': 0.75,
        'vague_text_penalty': 0.85,
        'short_text_threshold': 3
    },
    'risk': {
        'distance_weight': 0.55,
        'anomaly_weight': 0.45,
        'high_correction_threshold': 0.15,
        'high_non_object_threshold': 0.25,
        'high_variance_threshold': 0.8,
        'end_of_period_threshold': 0.30
    }
}
with open('backend/config/scoring.json', 'w') as f:
    json.dump(config, f, indent=2)
print('[OK] scoring.json')
EOF

REM Fix 4: Remove Sastrawi
echo [FIX 4/8] Removing unused imports...
python << EOF
content = open('backend/src/adapters/ml/tfidf_classifier.py', 'r', encoding='utf-8').read()
content = content.replace('from Sastrawi.Stopword.StopWordRemoverFactory import StopWordRemoverFactory\n', '')
open('backend/src/adapters/ml/tfidf_classifier.py', 'w', encoding='utf-8').write(content)
print('[OK] tfidf_classifier.py')
EOF

REM Fix 5: Column mapping
echo [FIX 5/8] Adding column name mapping...
python << EOF
with open('backend/src/application/use_cases/process_job_use_case.py', 'r', encoding='utf-8') as f:
    content = f.read()

if "# Map common column names" not in content:
    old_load = '''    def _load_data(self, file_path: str) -> pd.DataFrame:
        """Load CSV or Excel file"""
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path, encoding='utf-8')
        else:
            return pd.read_excel(file_path)'''

    new_load = '''    def _load_data(self, file_path: str) -> pd.DataFrame:
        """Load CSV or Excel file"""
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            df = pd.read_excel(file_path)

        # Map common column names to account_name if missing
        if 'account_name' not in df.columns:
            for col in ['description', 'account_description', 'nama_akun', 'deskripsi']:
                if col in df.columns:
                    df['account_name'] = df[col]
                    break

        return df'''

    content = content.replace(old_load, new_load)

    with open('backend/src/application/use_cases/process_job_use_case.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('[OK] Added column mapping')
else:
    print('[SKIP] Column mapping exists')
EOF

REM Fix 6-8: Port files, DTOs, and model training handled by other scripts
echo [FIX 6/8] Ensuring port files exist...
call FIX_ALL_ISSUES.bat

echo [FIX 7/8] Training model...
cd backend
python -m src.adapters.ml.train_baseline
cd ..

echo [FIX 8/8] Testing backend...
cd backend
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend ready')"
cd ..

echo.
echo ========================================================================
echo ALL FIXES APPLIED!
echo ========================================================================
echo.
echo The app now supports files with either:
echo   - account_name column (standard)
echo   - description column (auto-mapped)
echo   - account_description column (auto-mapped)
echo.
echo Next: Run RUN_APP.bat to start
echo.
pause
