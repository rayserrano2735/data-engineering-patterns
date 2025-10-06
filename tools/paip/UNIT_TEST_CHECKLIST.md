# PAIP Unit Test Checklist
**Purpose:** Pre-QA unit tests run by dev before delivering RC to QA

---

## Test Summary

| Test | RC6 | Description |
|------|-----|-------------|
| 1. Installer version consistency | PASS | Git tag v1.0.2, all RC refs correct |
| 2. Platform zip contents | PASS | All Week 1 files present |
| 3. Doc version consistency | PASS | All docs show RC6 |
| 4. QA_CHECKLIST structure | PASS | RC6 at top, history preserved |
| 5. ROADMAP structure | PASS | RC6 in progress, rejections logged |
| 6. Python syntax check | PASS | No syntax errors |
| 7. File count verification | PASS | 20 exercises, 35 flashcards |
| 8. Textbook filename | PASS | PAIP_TEXTBOOK.md (uppercase) |
| 9. IM schedule in textbook | PASS | Interview Mode section in Week 1 |
| 10. IM framework in guide | PASS | Framework section in LEARNING_GUIDE.md |
| 11. RELEASE_NOTES updated | PASS | RC6 changes documented |

---

## RC6 Test Results

### Test 1: Installer Version Consistency - PASS
**Commands:**
```bash
grep "git tag" paip-install-v1.0.2-RC6.bat
grep "RC6" paip-install-v1.0.2-RC6.bat
```
**Result:** Git tag shows v1.0.2, all references show RC6

### Test 2: Platform Zip Contents - PASS
**Command:**
```bash
unzip -l paip-platform-v1.0.2-RC6.zip | grep -E "PAIP_TEXTBOOK|week1_exercises|week1_flashcards|INTERVIEW_MODE_WEEK1|LEARNING_GUIDE|quick_reference|talking_points"
```
**Result:** All 7 Week 1 files present

### Test 3: Doc Version Consistency - PASS
**Command:**
```bash
unzip -p paip-platform-v1.0.2-RC6.zip "platform/content/docs/*.md" | grep "^\\*\\*Version" | sort -u
```
**Result:** All docs show v1.0.2-RC6

### Test 4: QA_CHECKLIST Structure - PASS
**Command:**
```bash
unzip -p paip-platform-v1.0.2-RC6.zip platform/content/docs/QA_CHECKLIST.md | grep "^## v1.0" | head -5
```
**Result:** RC6 at top, RC5/RC4/RC3/RC2/RC1 historical sections preserved

### Test 5: ROADMAP Structure - PASS
**Command:**
```bash
unzip -p paip-platform-v1.0.2-RC6.zip platform/content/docs/ROADMAP.md | grep "^### v1.0.2-RC"
```
**Result:** RC6 in progress, RC5/RC4/RC3/RC2/RC1 in rejected sections

### Test 6: Python Syntax Check - PASS
**Command:**
```bash
python -m py_compile platform/content/src/week1_exercises.py
```
**Result:** No errors

### Test 7: File Count Verification - PASS
**Commands:**
```bash
grep "^def exercise_" platform/content/src/week1_exercises.py | wc -l
grep -c "^Q:" platform/content/data/week1_flashcards.txt
```
**Result:** 20 exercises, 35 flashcards

### Test 8: Textbook Filename - PASS
**Command:**
```bash
unzip -l paip-platform-v1.0.2-RC6.zip | grep -i "textbook.md"
```
**Result:** File is PAIP_TEXTBOOK.md (uppercase)

### Test 9: IM Schedule in Textbook - PASS
**Command:**
```bash
unzip -p paip-platform-v1.0.2-RC6.zip platform/content/docs/PAIP_TEXTBOOK.md | grep -A 5 "Interview Mode Practice"
```
**Result:** Interview Mode section exists in Week 1 conclusion with:
- Explanation of Interview Mode
- When to practice
- How to use
- What to expect
- Example scenario

### Test 10: IM Framework in LEARNING_GUIDE - PASS
**Command:**
```bash
unzip -p paip-platform-v1.0.2-RC6.zip platform/content/docs/LEARNING_GUIDE.md | grep -A 3 "For Course Designers: Creating Week-Specific IM Documents"
```
**Result:** LEARNING_GUIDE.md contains:
- Interview Mode section explaining the concept
- Framework for creating week-specific IM docs
- Template structure
- Required elements
- Example from Week 1

### Test 11: RELEASE_NOTES Updated - PASS
**Command:**
```bash
unzip -p paip-platform-v1.0.2-RC6.zip platform/content/docs/RELEASE_NOTES.md | grep "RC6"
```
**Result:** RELEASE_NOTES.md documents RC6 changes

---

## RC6 Change Manifest

**From rejected RC5:**
- Created brand new QA_CHECKLIST.md with clean structure
- Deprecated old problematic QA_CHECKLIST.md

**From rejected RC4 (carried forward):**
- Renamed paip_textbook.md → PAIP_TEXTBOOK.md
- Added Interview Mode schedule to PAIP_TEXTBOOK.md Week 1 conclusion
- Added Interview Mode framework section to LEARNING_GUIDE.md
- Updated RELEASE_NOTES.md with RC6 changes

**All tests passed - RC6 ready for QA**

