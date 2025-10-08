@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM Python Analytics Interview Prep v1.0.4-RC4
REM Silent installer with error display
REM Use /interactive flag for prompted installation
REM ============================================================

REM Check for interactive flag
set INTERACTIVE=0
if /i "%~1"=="/interactive" set INTERACTIVE=1

REM Determine repo directory first (needed for log path)
set DEFAULT_INSTALL=%USERPROFILE%\Dropbox\Projects\GitHub\python-analytics-interview-prep
if not exist "%USERPROFILE%\Dropbox\Projects\GitHub" (
    set DEFAULT_INSTALL=%USERPROFILE%\GitHub\python-analytics-interview-prep
)
set REPO_DIR=%DEFAULT_INSTALL%

REM Create parent directories if needed
for %%F in ("%REPO_DIR%") do set PARENT_DIR=%%~dpF
if not exist "%PARENT_DIR%" mkdir "%PARENT_DIR%" 2>nul

REM Create repo directory if needed
if not exist "%REPO_DIR%" mkdir "%REPO_DIR%"

REM Set log file path
set LOG_FILE=%REPO_DIR%\install.log

REM Start installation
echo ===============================================
echo Python Analytics Interview Prep v1.0.4-RC4
echo ===============================================
echo.
echo Installing to: %REPO_DIR%
echo Installation log: %LOG_FILE%
echo.

REM Log start time
echo Installing PAIP v1.0.4-RC4 > "%LOG_FILE%" 2>&1
echo Installation started at %DATE% %TIME% >> "%LOG_FILE%" 2>&1

REM Call main installation (logs to file, displays errors)
call :MAIN_INSTALL

REM Show completion
echo.
echo ===============================================
echo Installation complete
echo ===============================================
echo.
echo Installation log: %LOG_FILE%
echo.
if %INTERACTIVE%==1 (
    pause
)
exit /b 0

:MAIN_INSTALL
REM Main installation logic with logging

REM Check git availability
echo Checking prerequisites... >> "%LOG_FILE%" 2>&1
git --version >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo ERROR: Git is not installed or not in PATH >> "%LOG_FILE%" 2>&1
    echo Please install Git from https://git-scm.com
    if %INTERACTIVE%==1 pause
    exit /b 1
)
echo Git found >> "%LOG_FILE%" 2>&1

REM Change to repo directory
cd /d "%REPO_DIR%" >> "%LOG_FILE%" 2>&1

REM Initialize git if needed
echo Configuring git... >> "%LOG_FILE%" 2>&1
if not exist .git (
    git init >> "%LOG_FILE%" 2>&1
    git config core.autocrlf false >> "%LOG_FILE%" 2>&1
) else (
    git config core.autocrlf false >> "%LOG_FILE%" 2>&1
)
echo Git configured >> "%LOG_FILE%" 2>&1

REM Check for old structure
echo Checking for old structure... >> "%LOG_FILE%" 2>&1
set OLD_STRUCTURE_FOUND=0

for /d %%D in (*) do (
    if /i not "%%D"=="platform" (
        if /i not "%%D"=="study" (
            if /i not "%%D"==".git" (
                set OLD_STRUCTURE_FOUND=1
            )
        )
    )
)

for %%F in (*) do (
    if /i not "%%F"==".gitignore" (
        if /i not "%%F"=="README.md" (
            if /i not "%%F"=="requirements.txt" (
                if /i not "%%F"=="activate_env.txt" (
                    set OLD_STRUCTURE_FOUND=1
                )
            )
        )
    )
)

REM Handle old structure if found
if %OLD_STRUCTURE_FOUND%==1 (
    echo Old structure detected, moving to rollback... >> "%LOG_FILE%" 2>&1
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set DATESTR=%%c%%a%%b)
    set ROLLBACK_DIR=%USERPROFILE%\Downloads\paip-rollback-%DATESTR%
    
    mkdir "!ROLLBACK_DIR!" 2>nul
    echo Moving old structure to !ROLLBACK_DIR! >> "%LOG_FILE%" 2>&1
    
    for /d %%D in (*) do (
        if /i not "%%D"=="platform" (
            if /i not "%%D"=="study" (
                if /i not "%%D"==".git" (
                    move "%%D" "!ROLLBACK_DIR!\" >> "%LOG_FILE%" 2>&1
                )
            )
        )
    )
    for %%F in (*) do (
        if /i not "%%F"==".gitignore" (
            if /i not "%%F"=="README.md" (
                if /i not "%%F"=="requirements.txt" (
                    if /i not "%%F"=="activate_env.txt" (
                        move "%%F" "!ROLLBACK_DIR!\" >> "%LOG_FILE%" 2>&1
                    )
                )
            )
        )
    )
    
    echo Old structure moved to: !ROLLBACK_DIR! >> "%LOG_FILE%" 2>&1
    echo Old files moved to: !ROLLBACK_DIR!
)

REM Find the zip file
set SCRIPT_DIR=%~dp0
set ZIP_FILE=%SCRIPT_DIR%paip-platform-v1.0.4-RC4.zip

if not exist "%ZIP_FILE%" (
    echo ERROR: Cannot find paip-platform-v1.0.4-RC4.zip
    echo ERROR: Cannot find paip-platform-v1.0.4-RC4.zip >> "%LOG_FILE%" 2>&1
    echo Expected location: %ZIP_FILE%
    if %INTERACTIVE%==1 pause
    exit /b 1
)
echo Platform zip found >> "%LOG_FILE%" 2>&1

REM Remove old platform folder
echo Extracting platform... >> "%LOG_FILE%" 2>&1
if exist platform (
    rd /s /q platform >> "%LOG_FILE%" 2>&1
)

REM Remove old .gitignore to ensure it gets updated
if exist .gitignore (
    del /f .gitignore >> "%LOG_FILE%" 2>&1
)

REM Extract platform zip
powershell -command "Expand-Archive -Path '%ZIP_FILE%' -DestinationPath . -Force" >> "%LOG_FILE%" 2>&1
if errorlevel 1 (
    echo ERROR: Failed to extract platform files
    echo ERROR: Failed to extract platform files >> "%LOG_FILE%" 2>&1
    if %INTERACTIVE%==1 pause
    exit /b 1
)
echo Platform extracted >> "%LOG_FILE%" 2>&1

REM Clean artifacts
echo Cleaning artifacts... >> "%LOG_FILE%" 2>&1
for /d %%D in (study\*) do (
    if /i not "%%D"=="study\practice_work" (
        if /i not "%%D"=="study\notes" (
            if /i not "%%D"=="study\mock_interviews" (
                rd /s /q "%%D" >> "%LOG_FILE%" 2>&1
            )
        )
    )
)

if exist platform\content (
    for /d %%D in (platform\content\*) do (
        if /i not "%%D"=="platform\content\src" (
            if /i not "%%D"=="platform\content\docs" (
                if /i not "%%D"=="platform\content\patterns" (
                    if /i not "%%D"=="platform\content\data" (
                        if /i not "%%D"=="platform\content\student" (
                            if /i not "%%D"=="platform\content\platform" (
                                rd /s /q "%%D" >> "%LOG_FILE%" 2>&1
                            )
                        )
                    )
                )
            )
        )
    )
)

REM Create study workspace
if not exist study mkdir study
if not exist study\practice_work mkdir study\practice_work
if not exist study\notes mkdir study\notes
if not exist study\mock_interviews mkdir study\mock_interviews

echo. > study\practice_work\.gitkeep
echo. > study\notes\.gitkeep
echo. > study\mock_interviews\.gitkeep

echo Workspace created >> "%LOG_FILE%" 2>&1

REM Run bootstrap
echo Running bootstrap... >> "%LOG_FILE%" 2>&1
echo.
if %INTERACTIVE%==1 (
    python platform\tools\bootstrap.py --interactive >> "%LOG_FILE%" 2>&1
) else (
    python platform\tools\bootstrap.py >> "%LOG_FILE%" 2>&1
)
if errorlevel 1 (
    echo WARNING: Bootstrap encountered issues
    echo WARNING: Bootstrap encountered issues >> "%LOG_FILE%" 2>&1
    echo Check install.log for details
)
echo Bootstrap complete >> "%LOG_FILE%" 2>&1

REM Copy to version control (silent, no prompts)
set DEFAULT_VC=%USERPROFILE%\Dropbox\Projects\GitHub\data-engineering-patterns\tools\paip
if not exist "%USERPROFILE%\Dropbox\Projects\GitHub\data-engineering-patterns" (
    set DEFAULT_VC=%USERPROFILE%\GitHub\data-engineering-patterns\tools\paip
)

if exist "%DEFAULT_VC%\.." (
    echo Copying to version control... >> "%LOG_FILE%" 2>&1
    if not exist "%DEFAULT_VC%" mkdir "%DEFAULT_VC%" 2>nul
    copy "%~f0" "%DEFAULT_VC%\" >nul 2>&1
    copy "%ZIP_FILE%" "%DEFAULT_VC%\" >nul 2>&1
    copy "%SCRIPT_DIR%UNIT_TEST_CHECKLIST-v1.0.4-RC4.md" "%DEFAULT_VC%\" >nul 2>&1
    if errorlevel 1 (
        echo WARNING: Failed to copy to version control >> "%LOG_FILE%" 2>&1
    ) else (
        echo Copied to: %DEFAULT_VC% >> "%LOG_FILE%" 2>&1
        echo Copied to version control: %DEFAULT_VC%
    )
)

echo.
echo Installation completed successfully
echo.
echo NEXT STEPS:
echo.
echo   If using Wing IDE (recommended):
echo     1. Open PowerShell
echo     2. Run: Open-Wing
echo     3. Start coding in study/ directory
echo.
echo   Alternative: Manual Wing launch
echo     cd $env:PAIP_HOME
echo     ^& "C:\Program Files\Wing Pro 11\bin\wing.exe" python-analytics-interview-prep.wpr
echo.
echo   If working from command line:
echo     1. Restart your terminal to load environment variables
echo     2. Activate venv: %USERPROFILE%\.venvs\paip\Scripts\activate
echo     3. Run: python platform/content/src/exercises.py
echo.
echo After QA certification, manually run git commands:
echo   git add platform/ .gitignore README.md requirements.txt activate_env.txt study/
echo   git commit -m "Platform v1.0.4-RC4"
echo   git tag -a v1.0.4 -m "Release v1.0.4"
echo   git push
echo.

goto :eof
