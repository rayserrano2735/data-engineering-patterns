@echo off
REM Windows batch wrapper for generate_tree.py
REM Makes it easy to run the Python tree generator with a double-click

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
if not exist "generate_tree.py" (
    echo ERROR: generate_tree.py not found in current directory
    echo Please ensure generate_tree.py is in the same folder as this batch file
    pause
    exit /b 1
)

REM Run the Python script in interactive mode
echo Starting Folder Tree Generator...
echo.
python generate_tree.py -i

REM Keep window open to see results
echo.
pause