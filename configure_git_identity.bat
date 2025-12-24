@echo off
REM Configure Git Identity for AURORA Tax Classifier
REM This script helps you set up your Git user information

echo ================================================
echo Git Identity Configuration
echo ================================================
echo.
echo Git needs to know who you are before you can commit.
echo This information will appear in your commit history.
echo.

REM Prompt for name
set /p GIT_NAME="Enter your full name (e.g., John Doe): "
if "%GIT_NAME%"=="" (
    echo ERROR: Name cannot be empty!
    pause
    exit /b 1
)

REM Prompt for email
set /p GIT_EMAIL="Enter your email (e.g., john@example.com): "
if "%GIT_EMAIL%"=="" (
    echo ERROR: Email cannot be empty!
    pause
    exit /b 1
)

echo.
echo Configuring Git with:
echo   Name:  %GIT_NAME%
echo   Email: %GIT_EMAIL%
echo.

REM Ask for scope
echo Do you want to set this globally (for all repositories)?
echo   Y - Set globally (recommended)
echo   N - Set only for this repository
set /p GLOBAL_CHOICE="Your choice (Y/N): "

if /i "%GLOBAL_CHOICE%"=="Y" (
    echo.
    echo Setting Git identity globally...
    git config --global user.name "%GIT_NAME%"
    git config --global user.email "%GIT_EMAIL%"
    echo.
    echo Global Git identity configured successfully!
    echo This will be used for all your Git repositories.
) else (
    echo.
    echo Setting Git identity for this repository only...
    git config user.name "%GIT_NAME%"
    git config user.email "%GIT_EMAIL%"
    echo.
    echo Local Git identity configured successfully!
    echo This will be used only for the AURORA Tax Classifier repository.
)

echo.
echo ================================================
echo Verification
echo ================================================
git config user.name
git config user.email
echo.

echo ================================================
echo Next Steps:
echo ================================================
echo 1. Run: create_initial_commit.bat
echo    OR manually: git commit -m "Initial commit"
echo.
echo 2. Create GitHub repository at: https://github.com/new
echo.
echo 3. Connect to GitHub:
echo    git remote add origin git@github.com:YOUR_USERNAME/aurora-tax-classifier.git
echo    git branch -M main
echo    git push -u origin main
echo.

pause
