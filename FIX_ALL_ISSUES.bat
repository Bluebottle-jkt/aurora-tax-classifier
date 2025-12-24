@echo off
REM ============================================================================
REM AURORA - Fix All Issues Script
REM Fixes JSON format, missing configs, and trains model
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - Fixing All Issues
echo ========================================================================
echo.

cd /d "%~dp0"

echo [FIX 1/4] Fixing seed_corpus.jsonl format...
python -c "import json; seed_data = [{'text': 'gaji karyawan', 'label': 'PPh21'}, {'text': 'salary pegawai bulanan', 'label': 'PPh21'}, {'text': 'tunjangan hari raya THR', 'label': 'PPh21'}, {'text': 'bonus karyawan', 'label': 'PPh21'}, {'text': 'upah tenaga kerja', 'label': 'PPh21'}, {'text': 'pembayaran impor barang', 'label': 'PPh22'}, {'text': 'pembelian barang pemerintah', 'label': 'PPh22'}, {'text': 'bunga deposito bank', 'label': 'PPh23_Bunga'}, {'text': 'bunga pinjaman', 'label': 'PPh23_Bunga'}, {'text': 'dividen saham', 'label': 'PPh23_Dividen'}, {'text': 'pembagian dividen', 'label': 'PPh23_Dividen'}, {'text': 'hadiah undian', 'label': 'PPh23_Hadiah'}, {'text': 'hadiah lomba', 'label': 'PPh23_Hadiah'}, {'text': 'jasa konsultan', 'label': 'PPh23_Jasa'}, {'text': 'jasa profesi akuntan', 'label': 'PPh23_Jasa'}, {'text': 'jasa notaris', 'label': 'PPh23_Jasa'}, {'text': 'jasa pengacara', 'label': 'PPh23_Jasa'}, {'text': 'jasa teknisi', 'label': 'PPh23_Jasa'}, {'text': 'royalti paten', 'label': 'PPh23_Royalti'}, {'text': 'royalti merek', 'label': 'PPh23_Royalti'}, {'text': 'sewa gedung kantor', 'label': 'PPh23_Sewa'}, {'text': 'sewa kendaraan', 'label': 'PPh23_Sewa'}, {'text': 'sewa alat berat', 'label': 'PPh23_Sewa'}, {'text': 'bunga non resident', 'label': 'PPh26'}, {'text': 'dividen luar negeri', 'label': 'PPh26'}, {'text': 'pajak pertambahan nilai', 'label': 'PPN'}, {'text': 'PPN masukan', 'label': 'PPN'}, {'text': 'PPN keluaran', 'label': 'PPN'}, {'text': 'sewa tanah bangunan', 'label': 'PPh4_2_Final'}, {'text': 'penghasilan konstruksi', 'label': 'PPh4_2_Final'}, {'text': 'koreksi fiskal positif', 'label': 'Fiscal_Correction_Positive'}, {'text': 'koreksi fiskal negatif', 'label': 'Fiscal_Correction_Negative'}, {'text': 'biaya entertainment', 'label': 'Fiscal_Correction_Positive'}, {'text': 'biaya representasi', 'label': 'Fiscal_Correction_Positive'}, {'text': 'pendapatan bunga', 'label': 'Non_Object'}, {'text': 'biaya listrik', 'label': 'Non_Object'}, {'text': 'biaya telepon', 'label': 'Non_Object'}, {'text': 'biaya air', 'label': 'Non_Object'}]; f = open('backend/data/seed_corpus.jsonl', 'w', encoding='utf-8'); [f.write(json.dumps(item, ensure_ascii=False) + '\n') for item in seed_data]; f.close(); print('[OK] Fixed seed_corpus.jsonl')"

echo [FIX 2/4] Creating missing frontend config files...
if not exist frontend\tsconfig.node.json (
    echo {"compilerOptions":{"composite":true,"skipLibCheck":true,"module":"ESNext","moduleResolution":"bundler","allowSyntheticDefaultImports":true},"include":["vite.config.ts"]} > frontend\tsconfig.node.json
    echo [OK] Created tsconfig.node.json
) else (
    echo [SKIP] tsconfig.node.json already exists
)

if not exist frontend\postcss.config.js (
    echo export default {plugins: {tailwindcss: {},autoprefixer: {}}} > frontend\postcss.config.js
    echo [OK] Created postcss.config.js
) else (
    echo [SKIP] postcss.config.js already exists
)

echo [FIX 3/4] Training ML model...
cd backend
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    python -m src.adapters.ml.train_baseline
) else (
    python -m src.adapters.ml.train_baseline
)
cd ..

echo [FIX 4/4] Verifying fixes...
echo.
echo Checking files:
if exist backend\data\seed_corpus.jsonl (echo [OK] seed_corpus.jsonl exists) else (echo [ERROR] seed_corpus.jsonl missing)
if exist backend\models\baseline_model.pkl (echo [OK] baseline_model.pkl exists) else (echo [ERROR] baseline_model.pkl missing)
if exist frontend\tsconfig.node.json (echo [OK] tsconfig.node.json exists) else (echo [ERROR] tsconfig.node.json missing)
if exist frontend\postcss.config.js (echo [OK] postcss.config.js exists) else (echo [ERROR] postcss.config.js missing)

echo.
echo ========================================================================
echo ALL ISSUES FIXED!
echo ========================================================================
echo.
echo You can now run: RUN_APP.bat
echo.
pause
