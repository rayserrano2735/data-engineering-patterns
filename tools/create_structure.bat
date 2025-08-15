@echo off
REM Filename: create_structure.bat
REM Windows batch wrapper for create_structure.py
REM Makes it easy to create folder structures from YAML/JSON definitions

REM Store the original directory
set ORIGINAL_DIR=%CD%

REM Determine if we're in tools folder and need to go up
if exist "create_structure.py" (
    if exist "..\tools" (
        REM We're in the tools folder, go to parent (repo root)
        cd ..
        set SCRIPT_PATH=tools\create_structure.py
        set YAML_PATH=tools\structures\
    ) else (
        REM We're somewhere else with create_structure.py
        set SCRIPT_PATH=create_structure.py
        set YAML_PATH=structures\
    )
) else if exist "tools\create_structure.py" (
    REM We're already in repo root
    set SCRIPT_PATH=tools\create_structure.py
    set YAML_PATH=tools\structures\
) else (
    echo ERROR: Cannot find create_structure.py
    echo Please run this from the repository root or tools folder
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3 from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if the Python script exists
if not exist "%SCRIPT_PATH%" (
    echo ERROR: %SCRIPT_PATH% not found
    echo Current directory: %CD%
    cd %ORIGINAL_DIR%
    pause
    exit /b 1
)

REM Check if PyYAML is installed (needed for YAML support)
python -c "import yaml" 2>nul
if errorlevel 1 (
    echo PyYAML not found. Installing...
    pip install pyyaml
    if errorlevel 1 (
        echo ERROR: Failed to install PyYAML
        echo Please run: pip install pyyaml
        pause
        exit /b 1
    )
    echo PyYAML installed successfully!
    echo.
)

REM If no arguments, show interactive menu
if "%~1"=="" goto interactive_menu

REM If arguments provided, pass them through
python %SCRIPT_PATH% %*
cd %ORIGINAL_DIR%
goto end

:interactive_menu
echo ============================================
echo    Folder Structure Generator
echo ============================================
echo.
echo Available options:
echo   1. Create full repository structure (structure_full_repo.yaml)
echo   2. Create table-comparison structure only
echo   3. Create example structure files
echo   4. Specify a custom structure file
echo   5. Create quick structure with inline JSON
echo   6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto full_repo
if "%choice%"=="2" goto table_comparison
if "%choice%"=="3" goto examples
if "%choice%"=="4" goto custom
if "%choice%"=="5" goto inline
if "%choice%"=="6" goto end
goto interactive_menu

:full_repo
if exist "%YAML_PATH%structure_full_repo.yaml" (
    echo.
    echo Creating full repository structure in repo root...
    echo Current directory: %CD%
    python %SCRIPT_PATH% %YAML_PATH%structure_full_repo.yaml
) else (
    echo.
    echo ERROR: structure_full_repo.yaml not found!
    echo Looking in: %YAML_PATH%
    echo Current directory: %CD%
)
cd %ORIGINAL_DIR%
pause
goto end

:table_comparison
if exist "%YAML_PATH%structure_table_comparison.yaml" (
    echo.
    echo Creating table-comparison structure in repo root...
    python %SCRIPT_PATH% %YAML_PATH%structure_table_comparison.yaml
) else (
    echo.
    echo structure_table_comparison.yaml not found.
    echo Creating it from inline definition...
    python %SCRIPT_PATH% --inline "{\"sql-patterns\": {\"table-comparison\": {\"examples\": null, \"database-specific\": null, \"mappings\": null, \"tests\": null}}}"
)
cd %ORIGINAL_DIR%
) else (
    echo.
    echo structure_table_comparison.yaml not found.
    echo Creating it from inline definition...
    python create_structure.py --inline "{\"sql-patterns\": {\"table-comparison\": {\"examples\": null, \"database-specific\": null, \"mappings\": null, \"tests\": null}}}"
)
pause
goto end

:examples
echo.
echo Creating example structure files in current directory...
python %SCRIPT_PATH% --examples
echo.
echo Example files created! You can now edit them and run:
echo   %0 [filename]
cd %ORIGINAL_DIR%
pause
goto end

:custom
echo.
set /p yaml_file="Enter the structure file name (YAML or JSON): "
if exist "%yaml_file%" (
    python %SCRIPT_PATH% "%yaml_file%"
) else (
    echo ERROR: File '%yaml_file%' not found!
)
cd %ORIGINAL_DIR%
pause
goto end

:inline
echo.
echo Enter JSON structure (e.g., {"folder1": {"subfolder": null}}):
set /p json_structure="JSON: "
python %SCRIPT_PATH% --inline "%json_structure%"
cd %ORIGINAL_DIR%
pause
goto end

:end
echo.
echo ============================================
echo Structures are created in the repository root
echo Tip: You can also drag and drop a YAML/JSON file onto this batch file!
echo ============================================