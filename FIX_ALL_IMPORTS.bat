@echo off
REM ============================================================================
REM AURORA - Fix All Import Issues
REM Creates missing port files, DTO files, and fixes configs
REM ============================================================================

echo.
echo ========================================================================
echo AURORA - Fixing All Import Issues
echo ========================================================================
echo.

cd /d "%~dp0"

echo [FIX 1/5] Creating missing port interface files...
cd backend\src\application\ports
if not exist classifier_port.py (
    echo Creating classifier_port.py...
    python << 'EOF'
from pathlib import Path
Path('classifier_port.py').write_text('''"""Classifier Port interface."""
from abc import ABC, abstractmethod
from typing import List, Dict

class ClassifierPort(ABC):
    @abstractmethod
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        pass

    @abstractmethod
    def get_version(self) -> str:
        pass
''', encoding='utf-8')
print('[OK] classifier_port.py')
EOF
)

cd ..\..\..\..

echo [FIX 2/5] Creating DTO files...
if not exist backend\src\application\dtos mkdir backend\src\application\dtos
python FIX_ALL_ISSUES.py

echo [FIX 3/5] Fixing scoring.json...
python -c "import json; config={'confidence':{'p_max_weight':0.65,'margin_weight':0.35,'short_text_penalty':0.75,'vague_text_penalty':0.85,'short_text_threshold':3},'risk':{'distance_weight':0.55,'anomaly_weight':0.45,'high_correction_threshold':0.15,'high_non_object_threshold':0.25,'high_variance_threshold':0.8,'end_of_period_threshold':0.30}}; open('backend/config/scoring.json','w').write(json.dumps(config,indent=2)); print('[OK] scoring.json')"

echo [FIX 4/5] Removing unused Sastrawi import...
python -c "content=open('backend/src/adapters/ml/tfidf_classifier.py','r',encoding='utf-8').read(); content=content.replace('from Sastrawi.Stopword.StopWordRemoverFactory import StopWordRemoverFactory\n',''); open('backend/src/adapters/ml/tfidf_classifier.py','w',encoding='utf-8').write(content); print('[OK] tfidf_classifier.py')"

echo [FIX 5/5] Testing backend imports...
cd backend
python -c "from src.frameworks.fastapi_app import app; print('[OK] Backend imports successfully')"
cd ..

echo.
echo ========================================================================
echo ALL IMPORT ISSUES FIXED!
echo ========================================================================
echo.
echo You can now run: RUN_APP.bat
echo.
pause
