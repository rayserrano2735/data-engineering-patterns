# PAIP Platform Architecture
**Version: 1.0.5-RC4

## System Overview

PAIP is a local-first Python learning platform optimized for Analytics Engineers preparing for technical interviews.

**Core components:**
- Windows development environment
- Wing IDE integration
- Git-tracked study workspace
- Curated content library
- Test-driven exercise system
- AI-powered Interview Mode

---

## Directory Structure

```
python-analytics-interview-prep/
├── platform/
│   └── content/
│       ├── docs/           # Course documentation
│       ├── src/            # Python exercises and patterns
│       └── data/           # Flashcards and reference data
├── study/
│   ├── practice_work/      # Student practice files
│   ├── notes/              # Personal notes
│   └── mock_interviews/    # Interview practice sessions
├── activate_env.txt        # Environment activation instructions
├── requirements.txt        # Python dependencies
└── python-analytics-interview-prep.wpr  # Wing IDE project

C:\Users\{username}\
└── .venvs/
    └── paip/              # Python virtual environment
```

---

## Content Architecture

### Documentation (platform/content/docs/)

**Core Learning Materials:**
- **PAIP_TEXTBOOK.md** - Week 1 Python fundamentals (7 hours content with examples)
- **LEARNING_GUIDE.md** - 29-pattern library + Interview Mode framework + Python prerequisites
- **INTERVIEW_MODE_WEEK1.md** - AI interviewer guidelines for Week 1 practice

**Support Documentation:**
- **quick_reference.md** - Syntax quick reference
- **talking_points.md** - Communication strategies
- **course_with_schedule.md** - Legacy schedule

**Process Documentation:**
- **ROADMAP.md** - Release planning and version history
- **QA_CHECKLIST.md** - Testing criteria per release
- **DEVELOPMENT_PROCESS.md** - Dev/QA workflow
- **PLATFORM_ARCHITECTURE.md** - This document
- **RELEASE_NOTES.md** - Change log
- **GETTING_STARTED.md** - New user onboarding

### Exercises (platform/content/src/)

**TDD Structure:**
- **week1_exercises.py** - 20 exercise stubs with docstrings (students write solutions)
- **test_week1_exercises.py** - Test harness with expected outputs
- **week1_solutions.py** - Reference solutions for self-checking

**Pattern Library:**
- **patterns_and_gotchas.py** - 29 patterns with implementations
- **exercises.py** - Additional practice problems

### Data (platform/content/data/)

- **week1_flashcards.txt** - 74 flashcards (comprehensive method coverage)

---

## Learning Flow

```
1. TEXTBOOK
   Read PAIP_TEXTBOOK.md section
   Study examples (solutions shown)
   ↓
2. EXERCISES
   Complete week1_exercises.py stubs
   Run test_week1_exercises.py to validate
   Check week1_solutions.py if stuck
   ↓
3. FLASHCARDS
   Review week1_flashcards.txt for retention
   Practice daily with spaced repetition
   ↓
4. INTERVIEW MODE
   Practice with AI interviewer
   Unlimited scenario generation
   Real-time feedback
   ↓
5. ASSESSMENT
   Ready for real interviews
```

---

## Interview Mode Architecture

**Components:**
1. **INTERVIEW_MODE_WEEK1.md** - Instructions for AI on:
   - Learning objectives
   - Question categories
   - Difficulty progression
   - Evaluation criteria
   - Teaching approach

2. **LEARNING_GUIDE.md IM section** - Student-facing:
   - What Interview Mode is
   - When to use it
   - How it works
   - Framework for creating new week IM docs

3. **Future: Extended thinking + Voice mode** (RC1+)
   - AI uses extended thinking for scenario planning
   - Bidirectional voice for realistic interviews

**Session flow:**
```
User: "Interview me on Week 1"
  ↓
AI reads INTERVIEW_MODE_WEEK1.md
  ↓
Generates unique scenario
  ↓
Student responds
  ↓
AI evaluates + provides feedback
  ↓
Repeat with new scenarios
```

---

## Pattern Library

**29 patterns across 9 categories:**

1. **Selection & Filtering** (3 patterns)
2. **Aggregation & Summarization** (3 patterns)
3. **Time-Based Analysis** (3 patterns)
4. **Ranking & Ordering** (3 patterns)
5. **Data Quality** (3 patterns)
6. **Data Combination** (3 patterns)
7. **Advanced Transformations** (3 patterns)
8. **Performance & Integration** (2 patterns)
9. **Testing & Validation** (5 patterns) - NEW in v1.0.4

Each pattern documents:
- When to recognize it in interviews
- Implementation approach
- Common gotchas
- SQL equivalent (where applicable)

---

## Development Environment

**Wing IDE Configuration:**
- Project file: `python-analytics-interview-prep.wpr` (tracked)
- User preferences: `python-analytics-interview-prep.wpu` (ignored)
- Python path: `PYTHONPATH=platform/content` (inherited from PowerShell)
- Virtual env: `~/.venvs/paip/Scripts/python.exe`

**PowerShell Profile:**
```powershell
$env:PAIP_HOME = "path\to\repo"
$env:PYTHONPATH = "$env:PAIP_HOME\platform\content"
$env:PATH += ";$env:PAIP_HOME\.venvs\paip\Scripts"

function Open-Wing {
    & "C:\Program Files (x86)\Wing Pro 10\bin\wing.exe" `
      "$env:PAIP_HOME\python-analytics-interview-prep.wpr"
}
```

**Git Configuration:**
```gitignore
# Track
*.wpr (project file)
study/ (workspace)
platform/ (content)

# Ignore
*.wpu (user prefs)
.venvs/ (virtual env)
__pycache__/
```

---

## Testing Infrastructure

**Unit Tests (Dev):**
- UNIT_TEST_CHECKLIST.md documents all tests
- Tests run before QA delivery
- Validates versions, structure, content

**QA Tests:**
- QA_CHECKLIST.md per-release testing
- Installation validation
- Feature regression testing
- Content verification

**Exercise Tests:**
- test_week1_exercises.py validates student solutions
- TDD approach teaches testing from Week 1

---

## Build & Release Process

**RC Build:**
```
1. Dev logs changes in ROADMAP
2. Apply changes to source
3. Update doc versions
4. Build: paip-platform-v1.0.X-RCY.zip
5. Build: paip-install-v1.0.X-RCY.bat
6. Run unit tests
7. Deliver to QA
```

**QA Certification:**
```
1. QA tests against QA_CHECKLIST
2. Certify or Reject
3. If certified: git tag v1.0.X
4. Move to Completed in ROADMAP
5. Start next version RC1
```

**Deliverables:**
- Platform zip (content + structure)
- Installer batch script
- UNIT_TEST_CHECKLIST.md

---

## Future Architecture

**Product Backlog:**
- Week 2+ content (DataFrames + patterns)
- Pattern contribution workflow
- Interview Mode analytics (Snowflake + Tableau)
- Additional testing patterns

**Versioning:**
- v1.0.X = Week 1 refinements
- v1.1.X = Week 2 content
- v1.2.X = Weeks 3-4
- v2.0.X = Full 7-week course

---

## Key Design Principles

1. **Local-first** - No cloud dependencies, works offline
2. **Git-tracked** - Complete version control for learning
3. **Pattern-based** - Focus on problem recognition over memorization
4. **Test-driven** - TDD from Week 1
5. **AI-enhanced** - Unlimited practice via Interview Mode
6. **Minimal scope** - Only what's needed for interviews

