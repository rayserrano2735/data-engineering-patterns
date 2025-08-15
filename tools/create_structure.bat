@echo off
REM Filename: create_structure.bat
REM Windows batch wrapper for create_structure.py
REM Makes it easy to create folder structures from YAML/JSON definitions

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
if not exist "create_structure.py" (
    echo ERROR: create_structure.py not found in current directory
    echo Please ensure create_structure.py is in the same folder as this batch file
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
python create_structure.py %*
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
if exist "structures\structure_full_repo.yaml" (
    echo.
    echo Creating full repository structure...
    python create_structure.py structures\structure_full_repo.yaml
) else if exist "..\tools\structures\structure_full_repo.yaml" (
    echo.
    echo Creating full repository structure from parent directory...
    cd ..
    python tools\create_structure.py tools\structures\structure_full_repo.yaml
) else (
    echo.
    echo ERROR: structure_full_repo.yaml not found!
    echo Please ensure the YAML file is in tools\structures\ directory.
)
pause
goto end

:table_comparison
if exist "structures\structure_table_comparison.yaml" (
    echo.
    echo Creating table-comparison structure...
    python create_structure.py structures\structure_table_comparison.yaml
) else if exist "..\tools\structures\structure_table_comparison.yaml" (
    echo.
    echo Creating table-comparison structure from parent directory...
    cd ..
    python tools\create_structure.py tools\structures\structure_table_comparison.yaml
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
echo Creating example structure files...
python create_structure.py --examples
echo.
echo Example files created! You can now edit them and run:
echo   create_structure.bat [filename]
pause
goto end

:custom
echo.
set /p yaml_file="Enter the structure file name (YAML or JSON): "
if exist "%yaml_file%" (
    python create_structure.py "%yaml_file%"
) else (
    echo ERROR: File '%yaml_file%' not found!
)
pause
goto end

:inline
echo.
echo Enter JSON structure (e.g., {"folder1": {"subfolder": null}}):
set /p json_structure="JSON: "
python create_structure.py --inline "%json_structure%"
pause
goto end

:end
echo.
echo ============================================
echo Tip: You can also drag and drop a YAML/JSON file onto this batch file!
echo ============================================