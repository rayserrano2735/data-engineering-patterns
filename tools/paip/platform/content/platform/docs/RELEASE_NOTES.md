# Release Notes

## v1.0.5-RC4 (Current)

**Released:** October 8, 2025
**Status:** Building

### RC4 Changes

**Stories Completed:** 2/2 (100%)

**Java/PySpark Automation (PAIP-035, PAIP-037):**
- Added `pyspark>=3.5.0` to requirements.txt
- Automated Java installation in bootstrap.py:
  - Detects if Java installed (checks JAVA_HOME and PATH)
  - Downloads OpenJDK 11 (Adoptium Temurin JRE) if missing
  - Silent install with msiexec
  - Sets JAVA_HOME system environment variable
  - Adds Java bin to PATH
  - Handles errors with fallback instructions
- PySpark now works out of box without manual Java setup

### Files Modified
- requirements.txt - Added pyspark>=3.5.0
- platform/tools/bootstrap.py - Added Java detection and installation methods

**Deferred to RC5:**
- PAIP-033: Move Interview Preps to Study Folder
- PAIP-034: Document Platform vs Personalized Content Separation
- PAIP-036: Document Manual Package Installation

---

## v1.0.5-RC3 

**Released:** October 8, 2025
**Status:** Delivered to QA

**Stories Completed:** 8/8 (100%)

**UTF-16 Encoding Fix (PAIP-028):**
- Added `-Encoding UTF8` parameter to all `Out-File` commands in PowerShell installer
- Fixes install.log displaying "I n s t a l l i n g   P A I P" with spaces between characters
- PowerShell defaults to UTF-16, now explicitly UTF-8

**Interview Prep Feature (PAIP-026 to PAIP-032):**
- Created INTERVIEW_PREP_TEMPLATE.md for JD-specific prep content
- Built Danaher Staff Data Engineer interview prep:
  - danaher_staff_de.md: PySpark fundamentals, tool selection, ETL/ELT patterns, interview scenarios
  - danaher_pyspark_flashcards.txt: 25+ flashcards for rapid review
  - INTERVIEW_MODE_DANAHER_STAFF_DE.md: CTO-level practice scenarios
- Built SimplePractice Senior Data Engineer interview prep:
  - simplepractice_senior_de.md: Airflow orchestration, data quality frameworks, API integration (Python focus)
  - simplepractice_python_flashcards.txt: 25+ flashcards for Airflow and Python patterns
  - INTERVIEW_MODE_SIMPLEPRACTICE_SENIOR_DE.md: Multi-round technical interview scenarios
- Established directory structure: docs/interview_preps/, data/interview_preps/
- Content maintains dependency directive (assumes Days 1-2, explains beyond)

**QA Automation Fix:**
- Fixed installer test to check .ps1 file instead of .bat file (zip reference location)

### Files Added
- platform/content/student/docs/INTERVIEW_PREP_TEMPLATE.md
- platform/content/student/docs/interview_preps/danaher_staff_de.md
- platform/content/student/docs/interview_preps/INTERVIEW_MODE_DANAHER_STAFF_DE.md
- platform/content/student/docs/interview_preps/simplepractice_senior_de.md
- platform/content/student/docs/interview_preps/INTERVIEW_MODE_SIMPLEPRACTICE_SENIOR_DE.md
- platform/content/student/data/interview_preps/danaher_pyspark_flashcards.txt
- platform/content/student/data/interview_preps/simplepractice_python_flashcards.txt

### Files Modified
- platform/tools/qa_automation.py - Fixed installer test logic
- paip-install-v1.0.5-RC4.ps1 - UTF-8 encoding on all Out-File commands

---

## v1.0.5-RC2

**Released:** October 8, 2025
**Status:** Delivered to QA

### RC1 Rejection

**Reason:** 24 content quality and process violations including content dependency violations, incomplete AC delivery, process documentation gaps

### RC2 Changes

**Stories Completed:** 21/24 (88%)

**PowerShell Hybrid Installer (PAIP-025):**
- Created paip-install-v1.0.5-RC2.ps1 with full installer logic
- Created paip-install-v1.0.5-RC2.bat launcher (1 line, calls .ps1 with ExecutionPolicy Bypass)
- Migrated all logic from .bat to PowerShell

**Process Improvements (PAIP-001 to PAIP-004):**
- Implemented immediate logging rule with handover activities documentation
- Created ONBOARDING.md for efficient session startup
- Integrated qa_automation.py into DEVELOPMENT_PROCESS
- Added AC verification step before QA delivery
- Added textbook/flashcard sync requirement

**Bootstrap Fixes (PAIP-005, PAIP-013):**
- Fixed f-string syntax error in Wing IDE window geometry
- Preserved .wpu user customizations (only generate on first install)

**Content Quality (PAIP-006 to PAIP-024):**
- Removed unused platform/content/patterns folder
- Created dependency violations tracker for QA automation test cases
- Added SQL analogies for set operations (EXCEPT, UNION)
- Fixed code block line lengths in sets section
- Added built-in types section (int, str, list, dict, set, tuple, bool)
- Added zip() for dict creation with function vs method explanation
- Updated comprehension preliminary intuition to include filtering
- Renamed Example 1.1 "Filter Evens" → "Filter Odds"
- Added validation logic to Example 1.3 with preservation comment

**Flashcards Added:**
- Empty dict/set gotcha ({} vs set())
- Built-in types and functions
- zip() for dict creation
- Function vs method distinction

**Deferred to RC3:** 4 high-effort stories
- Wing run arguments dialog suppression
- Global story ID system implementation
- Execution code audit for all function examples
- Example 1-4 replacement with appropriate debug example

### Files Modified
- platform/tools/bootstrap.py - Fixed f-string, added .wpu preservation
- platform/tools/dependency_violations_tracker.md - Created
- platform/content/platform/docs/ONBOARDING.md - Created
- platform/content/platform/docs/DEVELOPMENT_PROCESS.md - Process improvements
- platform/content/student/docs/PAIP_TEXTBOOK.md - Content improvements
- platform/content/student/docs/INTUITIONS.md - SQL analogies updated
- platform/content/student/data/day1-2_flashcards.txt - 4 new flashcards
- All docs - Updated version to 1.0.5-RC2

### Breaking Changes
None

### QA Automation
✓ All 5 tests passed

---

## v1.0.4-RC3 (Current)

**Released:** October 7, 2025
**Status:** In QA Testing

### RC1 Rejection

**Reason:** Installer referenced wrong zip filename (v1.0.4-RC3.zip instead of v1.0.4-RC1.zip)

### RC2 Changes

**Week 2 Day 1 - Modern Python Patterns:**
- Added 1-hour content bridging Python fundamentals to production patterns
- Decorators: Functions as objects, closures, @ syntax explanation (45 min)
- Flexible arguments: *args/**kwargs with SQL analogies (included in decorator section)
- Orchestration concepts: Task dependencies, orchestration vs transformation (15 min)
- Extracted from zero_to_decorators.py and airflow materials

**Pattern Library Expansion:**
- Added Pattern 30: Orchestration Task Dependencies to Category 9
- Real Airflow examples: sequential, parallel convergence, sensors
- Interview talking points for workflow coordination questions

**Documentation Fixes:**
- Fixed PLATFORM_ARCHITECTURE.md flashcard count (50 → 74)
- Added handover efficiency guidance to DEVELOPMENT_PROCESS.md
- Added unit testing mandate: "Dev owns testing - test everything testable"

**Installer Fix:**
- Corrected zip filename reference to v1.0.4-RC3.zip
- Added unit test for version consistency across installer and docs

### Files Modified
- PAIP_TEXTBOOK.md - Added Week 2 Day 1 content (decorators, orchestration)
- LEARNING_GUIDE.md - Added Pattern 30
- PLATFORM_ARCHITECTURE.md - Fixed flashcard count
- DEVELOPMENT_PROCESS.md - Added testing mandate, handover guidance
- ROADMAP.md - Moved RC1 to rejected, added RC2 in progress
- All docs - Updated version to 1.0.4-RC3

### Breaking Changes
None

---

## v1.0.4-RC1 (Rejected)

**Released:** October 7, 2025
**Status:** Rejected - Installer filename mismatch
**Rejection Reason:** Installer referenced v1.0.4-RC3.zip instead of v1.0.4-RC1.zip

### Major Changes

**Content Order & Confusion Framework:**
- Created INTUITIONS.md template capturing counterintuitive syntax with SQL mappings
- Added list comprehension deep-dive: execution vs syntax order, design evaluation, bracket types
- Added Essential Built-in Functions section (list, range, evaluation) before examples
- Clarified "ordered" (position preserved) vs "sorted" (arranged by value)
- Fixed content dependency violations (concepts introduced before use)

**Quick Reference Enhancements:**
- Added result examples to all operations (e.g., `lst.append(4)  # [1, 2, 3, 4]`)
- Students can verify syntax without running code

**Flashcard Completeness:**
- Expanded from 50 to 74 flashcards (+24)
- Added comprehensive method coverage: list/dict/set/string operations
- Covers insert, remove, pop, setdefault, update, discard, find, enumerate, zip, filter, map

**Wing IDE Integration:**
- Documented Git integration in GETTING_STARTED.md
- Source Control panel, diff view, commit UI
- Students can commit work without leaving IDE

**Process Improvements:**
- Token budget tracking with 80%/90% alerts
- Backlog refinement process documentation
- Build token cost reporting (this build: 2,005 tokens)

### User Stories Completed

1. **Content Order & Confusion Framework** (Large) - Fixed dependency violations, added confusion explanations
2. **Quick Reference Enhancements** (Small) - Result examples, ordered vs sorted
3. **Flashcard Completeness** (Small) - 24 new method cards
4. **Wing IDE Integration** (Small) - Git integration documented
5. **Process Improvements** (Small) - Token tracking, backlog refinement

### Files Added
- `/platform/content/docs/INTUITIONS.md` - Student insights template

### Files Modified
- PAIP_TEXTBOOK.md - Added built-in functions, comprehension deep-dive, ordered/sorted clarity
- quick_reference.md - Added result examples to all operations
- week1_flashcards.txt - Added 24 method flashcards (total 74)
- GETTING_STARTED.md - Wing Git integration section
- DEVELOPMENT_PROCESS.md - Token tracking, backlog refinement sections

### Breaking Changes
None

---

## v1.0.3 (Released)

**Released:** October 6, 2025

Testing infrastructure and content refinements with TDD structure.

**Key Features:**
- TDD structure: stubs, test harness, solutions
- 29 patterns (24 data + 5 testing)
- Python Prerequisites section
- 50 flashcards
- Extended thinking + voice mode for Interview Mode

---

## v1.0.2 (Released)

Week 1 foundation content with textbook and pattern library.

---

## v1.0.1 (Released)

Development environment with Wing IDE integration.

