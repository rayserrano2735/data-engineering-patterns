@echo off
REM Filename: add_pattern.bat
REM Interactive pattern selector for easy structure generation
REM Place in tools/ folder

setlocal enabledelayedexpansion

REM Colors for better UI
REM Note: Windows 10+ supports ANSI colors

echo.
echo ============================================
echo         PATTERN STRUCTURE GENERATOR
echo ============================================
echo.

REM Check if we're in tools folder or repo root
if exist "structures" (
    set STRUCTURES_PATH=structures
    set SCRIPT_PATH=create_structure.py
) else if exist "tools\structures" (
    set STRUCTURES_PATH=tools\structures
    set SCRIPT_PATH=tools\create_structure.py
) else (
    echo ERROR: Cannot find structures folder
    echo Please run from repository root or tools folder
    pause
    exit /b 1
)

REM List available structure files
echo Available Pattern Structures:
echo ------------------------------
set /a count=0

REM Store files in array
for %%f in (%STRUCTURES_PATH%\*.yaml %STRUCTURES_PATH%\*.yml) do (
    set /a count+=1
    set "file[!count!]=%%~nxf"
    echo   !count!. %%~nxf
)

REM Check if any files found
if %count%==0 (
    echo.
    echo No structure files found in %STRUCTURES_PATH%
    echo Please create .yaml or .yml structure files first
    pause
    exit /b 1
)

REM Add special options
set /a count+=1
set "file[!count!]=CREATE_NEW"
echo   !count!. [Create new structure file]

set /a count+=1  
set "file[!count!]=CUSTOM_PATH"
echo   !count!. [Specify custom path]

set /a count+=1
set "file[!count!]=INLINE"
echo   !count!. [Enter inline JSON structure]

set /a count+=1
set "file[!count!]=EXIT"
echo   !count!. Exit

echo.
echo ============================================
echo.

REM Get user choice
set /p choice="Select pattern structure to generate (1-%count%): "

REM Validate input
if "%choice%"=="" goto invalid_choice
if %choice% LSS 1 goto invalid_choice
if %choice% GTR %count% goto invalid_choice

REM Get selected file
set selected=!file[%choice%]!

REM Handle special options
if "!selected!"=="EXIT" (
    echo Exiting...
    exit /b 0
)

if "!selected!"=="CREATE_NEW" (
    echo.
    echo Creating new structure file...
    echo.
    set /p pattern_name="Enter pattern name (e.g., window-functions): "
    if "!pattern_name!"=="" (
        echo Error: Pattern name cannot be empty
        pause
        exit /b 1
    )
    
    REM Create basic structure template
    echo # Structure for !pattern_name! pattern > %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo # Generated on %date% >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo. >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo sql-patterns: >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo   !pattern_name!: >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo     __files__: >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo       - README.md >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo       - main_solution.sql >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo     examples: null >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo     database-specific: null >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo     tests: null >> %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    
    echo.
    echo Created: %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    echo Edit this file to customize the structure, then run this script again.
    echo.
    
    REM Open in notepad for editing
    set /p edit_now="Open in notepad to edit? (y/n): "
    if /i "!edit_now!"=="y" (
        notepad %STRUCTURES_PATH%\structure_!pattern_name!.yaml
    )
    pause
    exit /b 0
)

if "!selected!"=="CUSTOM_PATH" (
    echo.
    set /p custom_file="Enter full path to structure file: "
    if not exist "!custom_file!" (
        echo Error: File not found: !custom_file!
        pause
        exit /b 1
    )
    set selected=!custom_file!
    set full_path=!custom_file!
    goto generate
)

if "!selected!"=="INLINE" (
    echo.
    echo Enter inline JSON structure
    echo Example: {"sql-patterns": {"my-pattern": {"examples": null}}}
    echo.
    set /p json_structure="JSON: "
    python %SCRIPT_PATH% --inline "!json_structure!"
    pause
    exit /b 0
)

REM Build full path for regular selection
set full_path=%STRUCTURES_PATH%\!selected!

:generate
REM Show what will be generated
echo.
echo ============================================
echo Generating structure from: !selected!
echo ============================================
echo.

REM Ask for confirmation
set /p confirm="Proceed with generation? (y/n): "
if /i not "!confirm!"=="y" (
    echo Generation cancelled.
    pause
    exit /b 0
)

REM Run the structure generator
echo.
python %SCRIPT_PATH% !full_path!

REM Check if successful
if %errorlevel%==0 (
    echo.
    echo ============================================
    echo Structure generated successfully!
    echo ============================================
    echo.
    echo Next steps:
    echo 1. Navigate to the created folders
    echo 2. Add your pattern code files
    echo 3. Update the README.md with documentation
    echo 4. Commit and push to GitHub
    echo.
) else (
    echo.
    echo ERROR: Structure generation failed
    echo Check the error message above
)

pause
exit /b 0

:invalid_choice
echo.
echo Invalid choice. Please enter a number between 1 and %count%
pause
exit /b 1