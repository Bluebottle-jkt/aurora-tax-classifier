@echo off
REM ============================================================================
REM AURORA - Complete Fix Script
REM Fixes ALL known issues in one go
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - Complete Fix Script
echo ========================================================================
echo.

cd /d "%~dp0"

echo This will fix:
echo   1. JSON format in seed_corpus.jsonl
echo   2. Missing TypeScript config files
echo   3. Missing Python port interfaces
echo   4. Missing DTO files
echo   5. Config parameter mismatches
echo   6. Unused Sastrawi import
echo   7. Train ML model
echo.
pause

echo.
echo [STEP 1/7] Fixing seed_corpus.jsonl...
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
print('[OK] seed_corpus.jsonl fixed')
EOF

echo.
echo [STEP 2/7] Creating frontend config files...
if not exist frontend\tsconfig.node.json (
    echo {"compilerOptions":{"composite":true,"skipLibCheck":true,"module":"ESNext","moduleResolution":"bundler","allowSyntheticDefaultImports":true},"include":["vite.config.ts"]} > frontend\tsconfig.node.json
    echo [OK] tsconfig.node.json created
)
if not exist frontend\postcss.config.js (
    echo export default {plugins: {tailwindcss: {},autoprefixer: {}}} > frontend\postcss.config.js
    echo [OK] postcss.config.js created
)

echo.
echo [STEP 3/7] Creating port interface files...
python << PORTS
from pathlib import Path
import os

os.makedirs('backend/src/application/ports', exist_ok=True)

ports = {
    'classifier_port.py': '''"""Classifier Port"""
from abc import ABC, abstractmethod
from typing import List, Dict

class ClassifierPort(ABC):
    @abstractmethod
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        pass
    @abstractmethod
    def get_version(self) -> str:
        pass
''',
    'storage_port.py': '''"""Storage Port"""
from abc import ABC, abstractmethod
from typing import BinaryIO

class StoragePort(ABC):
    @abstractmethod
    def save_file(self, file: BinaryIO, job_id: str, filename: str) -> str:
        pass
    @abstractmethod
    def get_file_path(self, job_id: str, filename: str) -> str:
        pass
    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass
''',
    'config_port.py': '''"""Config Port"""
from abc import ABC, abstractmethod
from typing import Dict, Any

class ConfigPort(ABC):
    @abstractmethod
    def get_scoring_config(self) -> Dict[str, Any]:
        pass
    @abstractmethod
    def get_priors(self) -> Dict[str, Dict[str, float]]:
        pass
    @abstractmethod
    def get_labels(self) -> list[str]:
        pass
''',
    'explainability_port.py': '''"""Explainability Port"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ExplainabilityPort(ABC):
    @abstractmethod
    def get_top_terms(self, text: str, label: str, limit: int = 5) -> List[str]:
        pass
    @abstractmethod
    def get_nearest_examples(self, text: str, limit: int = 3) -> List[Dict[str, Any]]:
        pass
'''
}

for name, content in ports.items():
    path = Path(f'backend/src/application/ports/{name}')
    if not path.exists():
        path.write_text(content, encoding='utf-8')
        print(f'[OK] {name} created')
PORTS

echo.
echo [STEP 4/7] Creating DTO files...
if not exist backend\src\application\dtos mkdir backend\src\application\dtos
python FIX_ALL_ISSUES.py

echo.
echo [STEP 5/7] Fixing scoring.json...
python << SCORING
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
print('[OK] scoring.json fixed')
SCORING

echo.
echo [STEP 6/7] Removing unused imports...
python << IMPORTS
content = open('backend/src/adapters/ml/tfidf_classifier.py', 'r', encoding='utf-8').read()
content = content.replace('from Sastrawi.Stopword.StopWordRemoverFactory import StopWordRemoverFactory\n', '')
open('backend/src/adapters/ml/tfidf_classifier.py', 'w', encoding='utf-8').write(content)
print('[OK] Removed Sastrawi import')
IMPORTS

echo.
echo [STEP 7/7] Training ML model...
cd backend
python -m src.adapters.ml.train_baseline
cd ..

echo.
echo ========================================================================
echo VERIFICATION
echo ========================================================================
echo.
echo Testing backend imports...
cd backend
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend imports successfully')"
cd ..

echo.
echo Checking files:
if exist backend\data\seed_corpus.jsonl (echo [OK] seed_corpus.jsonl) else (echo [ERROR] seed_corpus.jsonl missing)
if exist backend\models\baseline_model.pkl (echo [OK] baseline_model.pkl) else (echo [ERROR] baseline_model.pkl missing)
if exist frontend\tsconfig.node.json (echo [OK] tsconfig.node.json) else (echo [ERROR] tsconfig.node.json missing)
if exist backend\src\application\ports\classifier_port.py (echo [OK] classifier_port.py) else (echo [ERROR] classifier_port.py missing)
if exist backend\src\application\dtos\job_dtos.py (echo [OK] job_dtos.py) else (echo [ERROR] job_dtos.py missing)

echo.
echo ========================================================================
echo ALL FIXES COMPLETE!
echo ========================================================================
echo.
echo Next step: Run RUN_APP.bat to start the application
echo.
pause
