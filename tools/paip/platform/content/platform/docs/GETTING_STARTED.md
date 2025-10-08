# Getting Started
**Version: 1.0.5-RC4

## Installation

1. Download `paip-install-v1.0.1.bat` and `paip-platform-v1.0.1.zip`
2. Run the installer
3. Confirm installation when prompted
4. Choose installation location (default: Dropbox/Projects/GitHub or GitHub folder)
5. Allow old structure rollback if detected

The installer automatically runs bootstrap to configure your environment.

## First Steps

After installation:

1. **Restart your terminal** to load environment variables

2. **Activate virtual environment**
   ```bash
   # Windows
   ~/.venvs/paip/Scripts/activate
   
   # Mac/Linux
   source ~/.venvs/paip/bin/activate
   ```

3. **Review the structure**
   ```
   platform/
     tools/       - Bootstrap script, Docker setup
     content/     - Learning materials
       src/       - Exercises and patterns
       docs/      - Guides and curriculum
       patterns/  - Pattern library
       data/      - Datasets and flashcards
   study/         - Your workspace
   ```

4. **Start learning**
   - Browse `platform/content/docs/` for curriculum
   - Try exercises in `platform/content/src/`
   - Study patterns in `platform/content/patterns/`

5. **Work in study/**
   - Solutions: `study/practice_work/`
   - Notes: `study/notes/`
   - Interview practice: `study/mock_interviews/`

## Your Workspace

The `study/` directory:
- Never overwritten by platform updates
- Not tracked in git (except .gitkeep files)
- Safe place for all your work

## Environment Setup

The installer automatically runs `platform/tools/bootstrap.py` which configures:
- Virtual environment at `~/.venvs/paip` (user-level, survives git operations)
- Shell profile (PowerShell/Bash)
- Environment variables (GITHUB_HOME, PAIP_HOME, PATTERNS_REPO, PATTERNS_TOOLS)
- Wing IDE project and preferences
- Git settings

**No manual setup required** - bootstrap runs automatically during installation.

## Wing IDE Setup

Bootstrap automatically generates:
- `.wpr` - Project file with proper source paths (platform/content) and exclusions
- `.wpu` - User preferences with Python interpreter pointing to `~/.venvs/paip`
- `Open-Wing` - PowerShell function for easy launch
- Desktop shortcut - "PAIP - Wing IDE" on your desktop

To use Wing:
1. **Double-click the desktop shortcut**, or
2. **Open PowerShell and run:** `Open-Wing`

**Alternative:** Manually launch Wing:
```powershell
cd $env:PAIP_HOME
& "C:\Program Files\Wing Pro 11\bin\wing.exe" python-analytics-interview-prep.wpr
```

**Note:** Wing must inherit PYTHONPATH from PowerShell environment. The desktop shortcut and `Open-Wing` function handle this automatically.

## Daily Use

### Activate Environment
```bash
# Windows
~/.venvs/paip/Scripts/activate

# Mac/Linux
source ~/.venvs/paip/bin/activate
```

### Run Exercises
```bash
python platform/content/src/exercises.py
```

### Practice Patterns
Work in `study/practice_work/`, commit your progress.

## Updates

To update platform:
1. Download new release files (install.bat + zip)
2. Run installer
3. Old platform backed up to Downloads/paip-rollback-[date]
4. Your study/ workspace preserved
5. Virtual environment at `~/.venvs/paip` unaffected

## Common Issues

### Git CRLF Warnings
Already fixed - installer sets `core.autocrlf false`.

### Zip Artifacts
Brace-expansion folders automatically cleaned by installer.

### Virtual Environment Not Found
If Wing can't find Python interpreter:
1. Check install.log for bootstrap errors
2. Manually run: `python platform/tools/bootstrap.py`
3. Or set in Wing: Edit → Preferences → Python Executable → `~/.venvs/paip/Scripts/python.exe` (Windows) or `~/.venvs/paip/bin/python` (Unix)

### Import Errors
If `from src.patterns_and_gotchas import CorePatterns` fails:
- Verify Wing project file (.wpr) includes `proj.pypath` with platform/content
- Bootstrap should set this automatically
- Check install.log for Wing configuration errors

## Troubleshooting

**Installation fails:**
- Ensure Git installed and in PATH
- Check write permissions to install location
- Review install.log for errors
- Check rollback folder in Downloads if needed

**Bootstrap fails:**
- Ensure Python 3.x installed
- Check permissions to create `~/.venvs/` directory
- Review install.log for specific error
- Manually configure shell profile if needed

**Virtual environment issues:**
- Delete `~/.venvs/paip/` folder and run bootstrap again
- Verify Python version compatibility (3.8+)
- Check requirements.txt exists at repo root

**Wing IDE issues:**
- Ensure Wing Pro 9+ installed
- Delete .wpr and .wpu files, run bootstrap again
- Check Python interpreter path in Wing preferences
- Verify PYTHONPATH includes platform/content

## Quick Commands

```bash
# Activate environment
source ~/.venvs/paip/bin/activate  # Unix
~/.venvs/paip/Scripts/activate     # Windows

# Run exercises
python platform/content/src/exercises.py

# Install new packages
pip install package-name
pip freeze > requirements.txt

# Git workflow (after QA certification)
git add platform/ study/ .gitignore README.md requirements.txt
git commit -m "Completed exercise X"
git push
```



### Wing IDE Git Integration

Wing automatically detects the Git repository and provides:
- **Source Control panel** (View → Version Control → Source Control)
- **Diff view** for file changes
- **Commit UI** for staging and committing
- **Branch management**

**To use:**
1. Open project in Wing
2. View → Version Control → Source Control (or Ctrl+Shift+G)
3. See changed files, diffs, commit messages
4. Stage files and commit directly from Wing

**Note:** All Git operations also work from PowerShell/command line.

## Next Steps

1. Environment already configured by installer
2. Review `platform/content/docs/course_with_schedule.md` for curriculum
3. Read `platform/content/docs/LEARNING_GUIDE.md` for study strategies
4. Review `platform/content/docs/ROADMAP.md` for upcoming features
5. Start with beginner exercises in `platform/content/src/`
