# PAIP Platform Onboarding
**Version: 1.0.5-RC4**

Quick reference for new Claude sessions to understand platform principles, goals, and process.

---

## Platform Mission

**Target Audience:** Analytics Engineers with SQL/dbt background facing Python/pandas interviews

**Core Problem:** Companies interview Analytics Engineers with Data Engineer skills (Python/pandas) despite role using dbt/SQL stack

**Solution:** Pattern-based prep for interview gatekeeping - 29 pandas patterns over 7 weeks

---

## Development Process

**RC Cycle:** Dev builds RC → Unit tests → Delivers to QA → QA tests → Certify/Reject

**Key Principles:**
1. No changes after QA delivery (new RC required)
2. Explicit QA decisions (Certify or Reject explicitly)
3. Complete logging (all work in ROADMAP stories)
4. Unit tests gate QA delivery
5. **Immediate logging:** Anything discussed → logged as story before session ends
6. **QA notification:** QA will notify Dev - don't ask for status

**Decision Framework:**
- **Autonomous:** Implementation, bugs, docs, RC increments
- **Requires go-ahead:** New features, process changes, scope changes

**Story Format:**
```
**PAIP-XXX: Story Name** (Size: Small/Medium/Large)
- As a [role], I want [feature] so that [benefit]

**Acceptance Criteria:**
- Specific deliverable 1
- Testable outcome 2
```

**Sizing:** Small (<2hr), Medium (2-4hr), Large (4+hr)

---

## Content Philosophy

**Guiding Principle:** No concept, method, syntax, or feature used before explained to student

**Week 1:** Python fundamentals (7 hours, 0 patterns)
- Foundation: lists, dicts, sets, comprehensions, functions, lambda, strings

**Weeks 2-7:** 29 pandas patterns (introduce → expand → integrate)

**Learning Materials:**
- **PAIP_TEXTBOOK.md:** Week-by-week content with examples
- **LEARNING_GUIDE.md:** 29-pattern library + Interview Mode + prerequisites
- **Exercises:** TDD structure (stubs, test harness, solutions)
- **Flashcards:** Daily packages aligned with textbook
- **Interview Mode:** AI interviewer practice with extended thinking

**Content Sync Rule:** Textbook changes → flashcard sync check

---

## Platform Structure

```
platform/
├── content/
│   ├── student/           # Student-facing content
│   │   ├── docs/          # Textbook, guides, interview mode
│   │   ├── src/           # Exercises, patterns
│   │   └── data/          # Flashcards
│   └── platform/          # Process documentation
│       └── docs/          # ROADMAP, DEVELOPMENT_PROCESS, etc.
└── tools/
    ├── bootstrap.py       # Environment setup automation
    └── qa_automation.py   # Automated validation tests

study/                     # Student workspace (git-tracked)
├── practice_work/         # Student practice files
├── notes/                 # Personal notes
└── mock_interviews/       # Interview practice
```

---

## Quality Standards

1. **Content Dependencies:** Enforce strict ordering - nothing used before explained
2. **Version Consistency:** All docs must have matching version strings
3. **RC History:** Complete rejection reasons logged in ROADMAP
4. **QA Automation:** qa_automation.py validates structure, versions, dependencies
5. **AC Verification:** Check all acceptance criteria before delivery

---

## Current State Orientation

**Current Version:** v1.0.5-RC4 (building)
**Current Process State:** Building RC2 after RC1 rejection

**Quick Actions:**
1. Check ROADMAP.md → "In Progress" section for current RC stories
2. Check DEVELOPMENT_PROCESS.md for workflow details
3. Check dependency_violations_tracker.md for known content issues

---

## Interview Criteria (What Drives Content)

**Content inclusion rule:** What gets tested in Analytics Engineer interviews, NOT what's used on the job

**Example:** PySpark is "nice to have" in JDs → include in Week 8+ 
**Example:** Tuple rarely tested → minimal coverage despite being built-in

---

## Debug Workflow (Student Learning Pattern)

1. Create week1_examples.py in study/practice_work/
2. Copy example code from textbook
3. Set breakpoints
4. Run in debug mode
5. Watch variables transform

**Why:** See execution order, understand mutation, build accurate mental models

---

## For Deep Dives

- Process details → DEVELOPMENT_PROCESS.md
- Architecture → PLATFORM_ARCHITECTURE.md
- Release history → ROADMAP.md
- Content structure → LEARNING_GUIDE.md
- Week 1 content → PAIP_TEXTBOOK.md
