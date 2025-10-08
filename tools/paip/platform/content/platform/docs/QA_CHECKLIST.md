# QA Checklist
**Version: 1.0.5-RC4

This document maintains testing criteria for each PAIP release.

---

## v1.0.4-RC3 - Testing Infrastructure & Content Refinements

### Installation
- [ ] Run installer (silent mode)
- [ ] Check install.log for full output
- [ ] Verify git repo initialized

### Bootstrap Execution  
- [ ] Verify bootstrap ran successfully
- [ ] Check install.log shows "Updated PowerShell profile"
- [ ] Check venv exists at `~/.venvs/paip`

### PowerShell Profile Verification
- [ ] Open PowerShell profile: `notepad $PROFILE`
- [ ] Verify contains PAIP environment variables
- [ ] Verify NO duplicate PAIP entries

### Environment Variables
- [ ] Restart PowerShell
- [ ] Run: `echo $env:PYTHONPATH`
- [ ] Should show path ending in `\platform\content`

### Wing IDE Configuration
- [ ] Verify .wpu has only `proj.pyexec`
- [ ] Verify .wpr contains proj.pypath
- [ ] Check desktop for "PAIP - Wing IDE" shortcut
- [ ] Launch Wing, test imports

### Week 1 Content Verification
- [ ] Verify PAIP_TEXTBOOK.md (uppercase)
- [ ] Verify Week 1 complete
- [ ] Verify exercise references in textbook
- [ ] Verify week1_exercises.py (stubs only)
- [ ] Verify test_week1_exercises.py (test harness)
- [ ] Verify week1_solutions.py (reference solutions)
- [ ] Run tests: `python test_week1_exercises.py`
- [ ] Verify week1_flashcards.txt (50 cards)
- [ ] Verify LEARNING_GUIDE.md has 29 patterns
- [ ] Verify Python Prerequisites section exists
- [ ] Verify Interview Mode enhancements (extended thinking, voice)

### QA Certification
**After ALL checklist items pass:**
- [ ] Git operations:
  ```
  git add platform/ .gitignore README.md requirements.txt
  git commit -m "Platform v1.0.4-RC3"
  git tag -a v1.0.4 -m "Release v1.0.4"
  ```

---

## v1.0.4-RC3 - Testing Infrastructure & Content Refinements (Rejected)

**Why Rejected:**
- Installer git tag incorrect
- QA_CHECKLIST historical versions wrong
- ROADMAP erroneous "v1.0.4 (Released)"
- Exercise references missing from textbook

---

## v1.0.2 (Released)

Week 1 foundation content with textbook, pattern library, Interview Mode.

---

## v1.0.1 (Released)

Development environment with Wing IDE integration.

