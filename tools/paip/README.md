# Python Analytics Interview Prep Platform
**Version:** 1.0.1-RC8

## Quick Start

**Fresh Install:**
```bash
# Download paip-platform-v1.0.1.zip and paip-install-v1.0.1.bat
# Run paip-install-v1.0.1.bat
# Platform installed and configured automatically!
```

## v1.0.1 Structure

```
python-analytics-interview-prep/
├── platform/
│   ├── tools/            # Setup scripts and utilities
│   │   ├── bootstrap.py  # Environment automation
│   │   └── docker/       # Docker environment (future)
│   └── content/          # Learning materials (exercises, patterns, curriculum)
└── study/                # YOUR workspace (never overwritten)
    ├── practice_work/    # Your solutions
    ├── notes/            # Your notes
    └── mock_interviews/  # Practice sessions
```

## What's in v1.0.1

**Development Environment:**
- User-level virtual environment at `~/.venvs/paip`
- Wing IDE auto-configuration (.wpr and .wpu generation with PYTHONPATH)
- Automated bootstrap during installation
- PAIP_HOME environment variable
- requirements.txt at repository root

**Complete Curriculum (from v1.0.0):**
- 60 exercises across 6 modules
- 20+ core pandas patterns
- Complete 8-week schedule
- Interview flashcards
- Full documentation suite
- Roadmap for upcoming features

## Getting Started

1. Run installer - it automatically configures everything
2. Restart terminal to load environment variables
3. Activate venv: `~/.venvs/paip/Scripts/activate`
4. Open Wing IDE: `python-analytics-interview-prep.wpr`
5. Start coding in `study/` directory

## Environment Variables

Bootstrap automatically sets:
- `GITHUB_HOME` - Your GitHub master folder
- `PAIP_HOME` - This repository path
- `PATTERNS_REPO` - data-engineering-patterns repo
- `PATTERNS_TOOLS` - Patterns tools directory

## Updates

Download new releases and run install.bat.
Your work in `study/` is always preserved.
Old versions automatically moved to rollback folder.

## Support

Review platform/content/docs/ for detailed guides and curriculum.
Installation log saved to: install.log
