@echo off
REM AURORA Tax Classifier - Create Initial Git Commit
REM This script helps create the initial commit for the project

echo ================================================
echo AURORA Tax Classifier - Initial Commit Setup
echo ================================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo ERROR: Git repository not initialized!
    echo Please run init_git.bat first.
    echo.
    pause
    exit /b 1
)

echo Step 1: Checking Git status...
echo ------------------------------------------------
git status
echo.

echo Step 2: Reviewing files to be committed...
echo ------------------------------------------------
echo The following files will be EXCLUDED (see .gitignore):
echo   - venv/ (Python virtual environment)
echo   - node_modules/ (Node dependencies)
echo   - .env (Environment secrets - only .env.example will be committed)
echo   - *.pyc, __pycache__/ (Python cache)
echo   - *.log, logs/ (Log files)
echo   - build/, dist/ (Build artifacts)
echo   - .DS_Store, Thumbs.db (OS files)
echo.

echo IMPORTANT: Please verify that:
echo   1. .env file is NOT in the staged files list above
echo   2. No sensitive credentials or secrets are being committed
echo   3. Only .env.example is being committed (safe template)
echo.

set /p CONTINUE="Do you want to continue? (Y/N): "
if /i not "%CONTINUE%"=="Y" (
    echo.
    echo Commit cancelled by user.
    pause
    exit /b 0
)

echo.
echo Step 3: Staging all files...
echo ------------------------------------------------
git add .
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to stage files!
    pause
    exit /b 1
)
echo Files staged successfully.
echo.

echo Step 4: Showing staged files...
echo ------------------------------------------------
git status
echo.

set /p VERIFY="Do the staged files look correct? (Y/N): "
if /i not "%VERIFY%"=="Y" (
    echo.
    echo Unstaging files...
    git reset
    echo Files unstaged. Please review and try again.
    pause
    exit /b 0
)

echo.
echo Step 5: Creating initial commit...
echo ------------------------------------------------
echo Commit message:
echo "Initial commit: AURORA Tax Classifier project structure"
echo.

git commit -m "Initial commit: AURORA Tax Classifier project structure" -m "- Set up clean architecture with Domain-Driven Design" -m "- Configure backend API with FastAPI" -m "- Set up frontend with React and TypeScript" -m "- Add Docker support for containerized deployment" -m "- Include comprehensive documentation" -m "- Configure development environment with example configs"

if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to create commit!
    pause
    exit /b 1
)

echo.
echo ================================================
echo SUCCESS: Initial commit created!
echo ================================================
echo.

echo Commit details:
echo ------------------------------------------------
git log -1 --stat
echo.

echo ================================================
echo Next Steps:
echo ================================================
echo 1. Create a repository on GitHub
echo 2. Add the remote: git remote add origin <your-repo-url>
echo 3. Push to GitHub: git push -u origin main
echo.
echo For detailed instructions, see GITHUB_SETUP.md
echo.

pause
