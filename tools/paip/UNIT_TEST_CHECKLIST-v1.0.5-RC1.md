# Unit Test Checklist - v1.0.5-RC1
**Date:** October 7, 2025
**Platform Version:** 1.0.5-RC1
**Tester:** QA

---

## Pre-Installation Tests

### T1: Deliverables Present
- [ ] paip-install-v1.0.5-RC1.bat exists
- [ ] paip-platform-v1.0.5-RC1.zip exists  
- [ ] UNIT_TEST_CHECKLIST-v1.0.5-RC1.md exists
- [ ] All files in same directory

### T2: Installer Version Check
- [ ] Open paip-install-v1.0.5-RC1.bat in text editor
- [ ] Line 6 shows "REM Python Analytics Interview Prep v1.0.5-RC1"
- [ ] Line 43 shows "echo Python Analytics Interview Prep v1.0.5-RC1"
- [ ] Line 49 shows correct log message with RC version

### T3: Platform Zip Contents
```bash
unzip -l paip-platform-v1.0.5-RC1.zip | head -30
```
- [ ] Contains platform/ directory
- [ ] Contains README.md
- [ ] Contains requirements.txt
- [ ] Contains .gitignore

### T4: Student Folder Structure in Zip (CRITICAL - RC3 FAILURE POINT)
```bash
# Count student folder files - should be 30+
unzip -l paip-platform-v1.0.5-RC1.zip | grep "platform/content/student/" | wc -l
```
- [ ] Count is greater than 30 (RC3 had 0, RC1 should have 36+)
- [ ] Verify student/docs/ files present
- [ ] Verify student/src/ files present
- [ ] Verify student/data/ files present

### T5: Platform Folder Structure in Zip
```bash
# Count platform docs files - should be 6+
unzip -l paip-platform-v1.0.5-RC1.zip | grep "platform/content/platform/" | wc -l
```
- [ ] Count is greater than 6
- [ ] Verify platform/docs/ files present

---

## Installation Tests

### T6: Silent Installation
```bash
# Run installer
.\paip-install-v1.0.5-RC1.bat
```
- [ ] No interactive prompts appear
- [ ] Completes without errors
- [ ] Shows installation path
- [ ] Shows completion message

### T7: Installation Log
```bash
# Check install log
cat $env:USERPROFILE\Dropbox\Projects\GitHub\python-analytics-interview-prep\install.log
# OR
cat $env:USERPROFILE\GitHub\python-analytics-interview-prep\install.log
```
- [ ] Log file created
- [ ] First line shows "Installing PAIP v1.0.5-RC1"
- [ ] Contains timestamp
- [ ] Contains "Git found"
- [ ] Contains "Platform extracted"
- [ ] Contains "Bootstrap complete"
- [ ] No ERROR entries

### T8: Directory Structure (CRITICAL - RC3 FAILURE POINT)
```bash
cd $env:USERPROFILE\Dropbox\Projects\GitHub\python-analytics-interview-prep
# OR
cd $env:USERPROFILE\GitHub\python-analytics-interview-prep

# Check structure
tree platform\content -L 2
# OR
ls -R platform\content
```
- [ ] platform/ directory exists
- [ ] platform/content/student/ exists
- [ ] platform/content/student/docs/ exists
- [ ] platform/content/student/src/ exists
- [ ] platform/content/student/data/ exists
- [ ] platform/content/platform/ exists
- [ ] platform/content/platform/docs/ exists
- [ ] study/ directory exists
- [ ] README.md exists
- [ ] requirements.txt exists
- [ ] .gitignore exists

### T9: Student Documentation Files
```bash
ls platform\content\student\docs\
```
- [ ] PAIP_TEXTBOOK.md
- [ ] LEARNING_GUIDE.md
- [ ] INTERVIEW_MODE_WEEK1.md
- [ ] QUICK_REFERENCE.md (uppercase)
- [ ] TALKING_POINTS.md (uppercase)
- [ ] INTUITIONS.md
- [ ] course_with_schedule.md

### T10: Student Source Files
```bash
ls platform\content\student\src\
```
- [ ] week1_exercises.py (consolidated)
- [ ] day1-2_exercises.py
- [ ] day3_exercises.py
- [ ] day4_exercises.py
- [ ] day5_exercises.py
- [ ] day6_exercises.py
- [ ] day7_exercises.py
- [ ] exercises.py
- [ ] patterns_and_gotchas.py
- [ ] week1_solutions.py
- [ ] test_week1_exercises.py

### T11: Student Data Files
```bash
ls platform\content\student\data\
```
- [ ] flashcards_complete.txt (74 cards)
- [ ] day1-2_flashcards.txt
- [ ] day3_flashcards.txt
- [ ] day4_flashcards.txt
- [ ] day5_flashcards.txt
- [ ] day6_flashcards.txt
- [ ] day7_flashcards.txt

### T12: Platform Documentation Files
```bash
ls platform\content\platform\docs\
```
- [ ] ROADMAP.md (version 1.0.5-RC1)
- [ ] DEVELOPMENT_PROCESS.md
- [ ] QA_CHECKLIST.md
- [ ] PLATFORM_ARCHITECTURE.md
- [ ] GETTING_STARTED.md
- [ ] RELEASE_NOTES.md

---

## Functional Tests

### T13: Python Environment
```bash
# Activate environment
& "$env:USERPROFILE\.venvs\paip\Scripts\Activate.ps1"

# Check Python
python --version
```
- [ ] Virtual environment activates
- [ ] Python 3.12+ installed

### T14: Exercise Execution
```bash
# Run main exercises file
python platform\content\student\src\exercises.py
```
- [ ] File executes without import errors
- [ ] No undefined name errors
- [ ] Exercises run (may show assertion errors - expected)

### T15: Test Harness Execution
```bash
# Run test suite
python -m pytest platform\content\student\src\test_week1_exercises.py -v
```
- [ ] Tests execute
- [ ] Shows pass/fail results (failures expected for incomplete exercises)
- [ ] No import errors
- [ ] No undefined function errors

### T16: Content Dependency Check
```bash
# Check that dict.fromkeys is documented before use
grep -n "fromkeys" platform\content\student\docs\PAIP_TEXTBOOK.md
```
- [ ] fromkeys appears in Essential Built-in Functions section (early in file)
- [ ] fromkeys appears before first usage in examples

### T17: Daily Exercise Wrappers
```bash
# Test day 1-2 wrapper
python platform\content\student\src\day1-2_exercises.py
```
- [ ] Wrapper executes
- [ ] Imports from week1_exercises work
- [ ] No module errors

---

## Documentation Tests

### T18: TOC Verification
Open each file and verify table of contents exists:
- [ ] platform/content/student/docs/PAIP_TEXTBOOK.md has TOC
- [ ] platform/content/student/docs/LEARNING_GUIDE.md has TOC
- [ ] platform/content/student/docs/INTERVIEW_MODE_WEEK1.md has TOC

### T19: Uppercase Naming Verification
```bash
ls platform\content\student\docs\
```
- [ ] QUICK_REFERENCE.md (not quick_reference.md)
- [ ] TALKING_POINTS.md (not talking_points.md)

### T20: ROADMAP Version
```bash
head -2 platform\content\platform\docs\ROADMAP.md
```
- [ ] Shows "Version: 1.0.5-RC1"
- [ ] In Progress section shows v1.0.5-RC1
- [ ] Rejected RCs section shows RC3 rejection with correct reason

---

## Version Control Tests

### T21: Git Status
```bash
cd $env:USERPROFILE\Dropbox\Projects\GitHub\python-analytics-interview-prep
# OR
cd $env:USERPROFILE\GitHub\python-analytics-interview-prep

git status
```
- [ ] Git repository initialized
- [ ] Shows untracked files (platform/, README.md, etc.)
- [ ] No errors

### T22: Rollback Created (if applicable)
If old structure existed:
```bash
ls $env:USERPROFILE\Downloads\paip-rollback-*
```
- [ ] Rollback directory created
- [ ] Old files moved successfully

---

## RC1-Specific Tests

### T23: Installation Shows RC Version
```bash
cat install.log | Select-String "Installing PAIP"
```
- [ ] Shows "Installing PAIP v1.0.5-RC1" as first line

### T24: Unit Test Checklist Filename
```bash
ls UNIT_TEST_CHECKLIST-v1.0.5-RC1.md
```
- [ ] Filename includes version suffix

### T25: Student Folder Installation Verification
```bash
# Verify actual file counts match zip contents
(ls -R platform\content\student\).Count
```
- [ ] Count matches expected (~40+ files including subdirectories)
- [ ] Tree structure shows all three subdirectories (docs/, src/, data/)

---

## Regression Tests

### T26: Bootstrap Script
- [ ] bootstrap.py exists in platform/tools/
- [ ] Executes without errors
- [ ] Creates venv if missing
- [ ] Installs requirements

### T27: Wing IDE Integration
- [ ] .wpr file exists (if applicable)
- [ ] Open-Wing command works (if configured)
- [ ] Project opens in Wing IDE

---

## Test Summary

**Total Tests:** 27
**Passed:** _____
**Failed:** _____
**Blocked:** _____

**Critical Failures (RC rejection triggers):**
- T4: Student folder structure missing from zip
- T8: Student folder structure missing from installation
- T16: Content dependency violations
- T20: Version inconsistencies

**RC1 Certification:**
- [ ] All critical tests pass
- [ ] Student folder structure present in zip (T4)
- [ ] Student folder structure present in installation (T8)
- [ ] Install log shows RC version (T23)
- [ ] Unit test checklist filename includes version (T24)
- [ ] Ready for production

**QA Sign-off:**
- Tester: _________________
- Date: _________________
- Status: [ ] PASS [ ] FAIL
- Notes: _________________

---

## RC3 Failure Analysis

**What went wrong in RC3:**
1. Files were correctly moved to platform/content/student/ in workspace
2. But zip command did not include these files
3. Unit test checked for path string "platform/content/student/" not file count
4. Test passed incorrectly, missing the packaging failure

**RC1 Fixes:**
1. Verified folder structure exists in workspace before zipping
2. Built zip correctly: `zip -r paip-platform-v1.0.5-RC1.zip platform/ README.md requirements.txt .gitignore -q`
3. Fixed unit test to count files: `unzip -l ... | grep "platform/content/student/" | wc -l` (should be 30+)
4. Added verification that count > 30, not just path string exists
