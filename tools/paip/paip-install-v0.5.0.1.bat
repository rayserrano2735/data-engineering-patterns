@echo off
setlocal enabledelayedexpansion

echo ===============================================
echo Python Analytics Interview Prep v0.5.0.1
echo ===============================================
echo.

REM Check if git is available
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)

REM Determine default installation location
REM Try Dropbox location first, fallback to GitHub folder
set DEFAULT_INSTALL=%USERPROFILE%\Dropbox\Projects\GitHub\python-analytics-interview-prep
if not exist "%USERPROFILE%\Dropbox\Projects\GitHub" (
    set DEFAULT_INSTALL=%USERPROFILE%\GitHub\python-analytics-interview-prep
)

REM Prompt for installation location
echo Default installation location:
echo %DEFAULT_INSTALL%
echo.
set /p USE_DEFAULT="Install to default location? (Y/n): "

if /i "%USE_DEFAULT%"=="n" (
    set /p CUSTOM_INSTALL="Enter custom installation path: "
    set REPO_DIR=!CUSTOM_INSTALL!
) else (
    set REPO_DIR=%DEFAULT_INSTALL%
)

echo.
echo Installing to: %REPO_DIR%
echo.

REM Create parent directories if they don't exist
for %%F in ("%REPO_DIR%") do set PARENT_DIR=%%~dpF
if not exist "%PARENT_DIR%" (
    echo Creating parent directories...
    mkdir "%PARENT_DIR%" 2>nul
)

REM Create repo directory if it doesn't exist
if not exist "%REPO_DIR%" (
    echo Creating repository directory...
    mkdir "%REPO_DIR%"
)

REM Change to repo directory
cd /d "%REPO_DIR%"

REM Initialize git if needed
if not exist .git (
    echo Initializing git repository...
    git init
)

REM Find the zip file (look in script's directory)
set SCRIPT_DIR=%~dp0
set ZIP_FILE=%SCRIPT_DIR%paip-platform-v0.5.0.1.zip

if not exist "%ZIP_FILE%" (
    echo ERROR: Cannot find paip-platform-v0.5.0.1.zip
    echo Expected location: %ZIP_FILE%
    echo Please ensure the zip file is in the same directory as this installer
    pause
    exit /b 1
)

REM Extract platform zip
echo Extracting platform files...
powershell -command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath . -Force"
if errorlevel 1 (
    echo ERROR: Failed to extract platform files
    pause
    exit /b 1
)
echo.

REM Create study workspace structure (idempotent)
echo Setting up study workspace...
if not exist study mkdir study
if not exist study\practice_work mkdir study\practice_work
if not exist study\notes mkdir study\notes
if not exist study\mock_interviews mkdir study\mock_interviews

REM Create .gitkeep files
echo. > study\practice_work\.gitkeep
echo. > study\notes\.gitkeep
echo. > study\mock_interviews\.gitkeep
echo.

REM Check if repo has any commits (brand new repo case)
git rev-parse HEAD >nul 2>&1
if errorlevel 1 (
    REM Brand new repo - create initial commit
    echo Creating initial commit...
    git add platform/
    git add .gitignore
    git add README.md
    git add study/
    git commit -m "Platform v0.5.0.1"
    
    REM Create tag
    git tag -a v0.5.0.1 -m "Release v0.5.0.1"
    echo Created tag v0.5.0.1
) else (
    REM Existing repo - check for staged changes
    git diff --cached --quiet
    if errorlevel 1 (
        echo Unstaging previous install...
        git reset HEAD
    )
    
    REM Stage platform files
    echo Committing platform files...
    git add platform/
    git add .gitignore
    git add README.md
    git add study/
    
    REM Commit
    git commit -m "Platform v0.5.0.1" >nul 2>&1
    if errorlevel 1 (
        echo No changes to commit
    ) else (
        echo Committed platform v0.5.0.1
    )
    
    REM Tag (silently fail if exists)
    git tag -a v0.5.0.1 -m "Release v0.5.0.1" 2>nul
    if errorlevel 1 (
        echo Note: Tag v0.5.0.1 already exists
    ) else (
        echo Created tag v0.5.0.1
    )
)

echo.
echo ===============================================
echo Installation complete!
echo ===============================================
echo.
echo Repository: %REPO_DIR%
echo.

REM Optional: Copy to version control
echo.
set /p COPY_TO_VC="Copy installer and platform to version control? (y/N): "

if /i "%COPY_TO_VC%"=="y" (
    REM Determine default VC location
    set DEFAULT_VC=%USERPROFILE%\Dropbox\Projects\GitHub\data-engineering-patterns\tools\paip
    if not exist "%USERPROFILE%\Dropbox\Projects\GitHub\data-engineering-patterns" (
        set DEFAULT_VC=%USERPROFILE%\GitHub\data-engineering-patterns\tools\paip
    )
    
    echo.
    echo Default version control location:
    echo !DEFAULT_VC!
    echo.
    set /p USE_VC_DEFAULT="Use default VC location? (Y/n): "
    
    if /i "!USE_VC_DEFAULT!"=="n" (
        set /p CUSTOM_VC="Enter custom VC path: "
        set VC_DIR=!CUSTOM_VC!
    ) else (
        set VC_DIR=!DEFAULT_VC!
    )
    
    REM Create VC directory if it doesn't exist
    if not exist "!VC_DIR!" (
        echo Creating VC directory: !VC_DIR!
        mkdir "!VC_DIR!" 2>nul
    )
    
    REM Copy installer and platform zip to VC location
    echo Copying to version control...
    copy "%SCRIPT_DIR%paip-install-v0.5.0.1.bat" "!VC_DIR!\" >nul
    copy "%ZIP_FILE%" "!VC_DIR!\" >nul
    
    if errorlevel 1 (
        echo WARNING: Failed to copy to version control
    ) else (
        echo Successfully copied to: !VC_DIR!
    )
)

echo.
echo Next steps:
echo   1. Review README.md for getting started guide
echo   2. Start learning: python platform/src/exercises.py
echo   3. Upload flashcards to Cram.com from platform/data/
echo.
echo Your work goes in the study/ directory
echo It will never be overwritten by platform updates
echo.

REM Prompt to open README
set /p OPEN_README="Open README.md now? (y/N): "
if /i "%OPEN_README%"=="y" (
    cd /d "%REPO_DIR%"
    start README.md
)

echo.
pause
