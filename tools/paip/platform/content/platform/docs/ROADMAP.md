# PAIP Platform Roadmap
**Version:** 1.0.5-RC4

## Current Release: v1.0.5
Content quality improvements, QA automation, and textbook enhancements.

---

## In Progress

### v1.0.5-RC4 - Java/PySpark Dependencies
**Target:** Current release candidate  
**Status:** Building

**User Stories:**

**PAIP-035: Add PySpark to Platform Dependencies** (Small)
- As a student, I want PySpark automatically installed so I can test PySpark code in interview preps

**Context:** Ray got `ModuleNotFoundError: No module named 'pyspark'` when testing Danaher interview prep code. PySpark should be in requirements.txt and auto-installed.

**Acceptance Criteria:**
- Add `pyspark>=3.5.0` to requirements.txt
- Bootstrap already installs from requirements.txt (no changes needed)
- Verify PySpark available after bootstrap runs

**PAIP-037: Automate Java Installation for PySpark** (Large)
- As a user, I want Java automatically installed during bootstrap so PySpark works without manual setup

**Context:** PySpark requires Java (runs on JVM). Currently students must manually install Java and set JAVA_HOME. Since Ray is admin on his box, bootstrap can automate this.

**Acceptance Criteria:**
- Add Java detection to bootstrap: check JAVA_HOME and PATH
- If Java missing, download OpenJDK 11 (Adoptium Temurin JRE MSI)
- Silent install: `msiexec /i <msi> /qn ADDLOCAL=FeatureMain,FeatureEnvironment`
- Set JAVA_HOME system environment variable
- Add Java bin to PATH
- Verify Java accessible after installation
- Print clear status messages during installation
- Handle errors gracefully with manual install instructions
- Update documentation about Java requirement

**Deferred to RC5:**
- PAIP-033: Move Interview Preps to Study Folder
- PAIP-034: Document Platform vs Personalized Content Separation
- PAIP-036: Document Manual Package Installation

---

### v1.0.5-RC4 - Targeted Interview Prep Feature
**Target:** Delivered to QA October 8, 2025  
**Status:** Delivered

**User Stories:**

**PAIP-028: Fix PowerShell Installer UTF-16 Encoding** (Small)
- As a user, I want install.log to display correctly without extra spaces between characters

**Context:** PowerShell `Out-File` defaults to UTF-16 encoding, causing "I n s t a l l i n g   P A I P" instead of "Installing PAIP" in install.log. Discovered post-RC2 delivery, not blocking but should fix.

**Acceptance Criteria:**
- Add `-Encoding UTF8` parameter to ALL `Out-File` commands in paip-install-v1.0.5-RC4.ps1
- Test that install.log displays correctly
- Verify no other encoding issues in installer

**PAIP-026: Create Interview Prep Template System** (Medium)
- As a student, I want a template for creating JD-specific interview prep content so I can prepare for specific interviews efficiently

**Acceptance Criteria:**
- Create INTERVIEW_PREP_TEMPLATE.md in platform/content/student/docs/
- Document structure: interview context, Python focus areas, quick reference, scenarios, supporting materials
- Define file naming conventions for preps, flashcards, Interview Mode docs
- Document directory structure: docs/interview_preps/, data/interview_preps/
- Include content dependency compliance guidelines (assume Days 1-2, explain beyond)
- Provide template maintenance guidance

**PAIP-027: Build Danaher Staff DE Interview Prep** (Large)
- As a student interviewing at Danaher, I want targeted PySpark and data engineering content so I can prepare for the CTO interview

**Context:** Interview with Chris Wheeler (Interim CTO) on 10/09/2025, 1:00-1:30 PM EDT. JD titled "Data Engineer" but includes dbt as plus → actually Analytics Engineer role.

**Acceptance Criteria:**
- Create danaher_staff_de.md in platform/content/student/docs/interview_preps/
- PySpark fundamentals: lazy evaluation, DataFrame API, transformations, joins, window functions
- Common PySpark patterns: top N per group, deduplication, pivots, incremental processing
- Tool selection framework: PySpark vs dbt vs alternatives
- ETL/ELT patterns and data quality checks
- Performance optimization concepts
- Interview scenarios: system design, problem diagnosis, tool selection
- CTO-level talking points
- Quick reference commands
- Interview prep checklist

**PAIP-028: Create Danaher PySpark Flashcards** (Small)
- As a student, I want flashcards for rapid PySpark review before the Danaher interview

**Acceptance Criteria:**
- Create danaher_pyspark_flashcards.txt in platform/content/student/data/interview_preps/
- 25+ flashcards covering: lazy evaluation, DataFrame operations, aggregations, joins, window functions, performance, tool selection
- Include Danaher-specific guidance (when to use PySpark vs dbt)
- Follow existing flashcard format from day1-2_flashcards.txt

**PAIP-029: Create Danaher Interview Mode Document** (Medium)
- As a student, I want AI-guided practice scenarios for the Danaher CTO interview

**Acceptance Criteria:**
- Create INTERVIEW_MODE_DANAHER_STAFF_DE.md in platform/content/student/docs/interview_preps/
- Define interview context: CTO-level, 30 min, system design focus
- Provide 5 scenario examples: multi-source integration, performance optimization, tool selection, data quality, real-time requirements
- Include interviewer style guidelines for CTO persona
- Define evaluation criteria: technical competence, judgment, communication, strategic thinking
- Provide sample interview opening and closing
- Include post-interview feedback structure

**PAIP-030: Build SimplePractice Senior DE Interview Prep** (Large)
- As a student interviewing at SimplePractice, I want targeted Python content for Airflow, data quality, and APIs

**Context:** Interview on 10/10/2025 (Friday). JD titled "Senior Data Engineer" but lists dbt as core requirement → Analytics Engineer role. Python for orchestration, not transformations.

**Acceptance Criteria:**
- Create simplepractice_senior_de.md in platform/content/student/docs/interview_preps/
- Airflow fundamentals: DAGs, task dependencies, PythonOperator, XCom, branching, sensors
- Data quality framework pattern in Python (DataQualityChecker class)
- API integration patterns: extraction, pagination, rate limiting, loading to Snowflake
- Python vs dbt decision framework
- Interview scenarios: DAG design, data quality, API integration, customer-facing analytics
- Quick reference commands
- Interview prep checklist

**PAIP-031: Create SimplePractice Python Flashcards** (Small)
- As a student, I want flashcards for rapid Airflow and Python review before SimplePractice interview

**Acceptance Criteria:**
- Create simplepractice_python_flashcards.txt in platform/content/student/data/interview_preps/
- 25+ flashcards covering: Airflow (DAGs, operators, XCom, sensors), data quality patterns, API integration, tool selection
- Include SimplePractice-specific guidance (when Python vs dbt)
- Follow existing flashcard format

**PAIP-032: Create SimplePractice Interview Mode Document** (Medium)
- As a student, I want AI-guided practice scenarios for SimplePractice technical interviews

**Acceptance Criteria:**
- Create INTERVIEW_MODE_SIMPLEPRACTICE_SENIOR_DE.md in platform/content/student/docs/interview_preps/
- Define interview context: Senior level, Python focus (Airflow/quality/APIs)
- Provide 5 scenario examples: Airflow DAG design, data quality framework, API integration, customer-facing analytics, tool selection
- Include interviewer style guidelines
- Define evaluation criteria: Python proficiency, system design, tool selection judgment, communication
- Provide sample interview opening and closing
- Include post-interview feedback structure

---

### v1.0.5-RC4 - Process Documentation & Onboarding
**Target:** Delivered to QA October 8, 2025  
**Status:** QA Testing

**RC1 Rejection Reason:** 24 content quality and process violations discovered during QA testing including: content dependency violations (methods/modules used before explained), missing flashcard sync, incomplete AC delivery from RC1, process documentation gaps, and example quality issues.

**User Stories:**

**PAIP-025: PowerShell Hybrid Installer** (Small)
- As a user, I want to double-click the installer and have it run in PowerShell so I'm using standardized shell

**Acceptance Criteria:**
- Create paip-install-vX.X.X.bat (launcher, 1 line)
- Create paip-install-vX.X.X.ps1 (actual installer logic)
- .bat calls .ps1 with ExecutionPolicy Bypass
- User can double-click .bat to run

**User Stories (continued):**

**Story 1: Wing IDE Window Size Preference** (Small)
- As a user, I want Wing IDE to open at a default size instead of maximized so I don't have to resize it every time

**Acceptance Criteria:**
- Add window geometry settings to _generate_wpu_file() in bootstrap.py
- Configure default window size (e.g., 1400x900 or 80% screen size)
- Configure default position (centered or user-specified)
- Ensure settings apply on first Wing launch after installation

**Story 2: Clarify RC-to-Version Migration in Dev Process** (Small)
- As a developer, I want clear guidance on what happens to RC5+ items when an RC is certified so I know where to log new work

**Acceptance Criteria:**
- Update DEVELOPMENT_PROCESS.md "After QA Certification" section
- Document that items logged for RC5+ during RC4 testing migrate to next version's RC1 upon certification
- Document that items stay as RC5 if RC4 is rejected
- Add example workflow showing certification path vs rejection path

**Story 3: Complete Content Dependency Audit - Platform Wide** (Large)
- As a student, I want ALL concepts introduced before use throughout the entire platform so I'm never confused by undefined syntax or unexplained concepts

**Context:** This story was marked complete in RC1 and RC3 but only partial fixes were applied (dict.fromkeys). The comprehensive platform-wide audit has never been completed. This is the third time this issue has been incorrectly closed.

**Guiding Principle:** No concept, method, syntax pattern, or language feature may be used in any example, exercise, or explanation before it has been explicitly introduced and explained to the student.

**Acceptance Criteria:**
- Systematic audit: Inventory ALL methods, functions, syntax patterns, and concepts used across entire platform
- For each item: Document WHERE first used and WHERE (if at all) first explained
- Create violations checklist: Items used before explanation
- Fix ALL violations platform-wide (not just dict.fromkeys and Example 1.1)
- Verify no forward references exist in any student-facing content
- Add automated test that fails if new content dependency violations are introduced
- Document the audit methodology so future content additions can be validated

**Story 4: Clarify Lists vs Dicts as DataFrame Rows** (Small)
- As a student, I want a clear mental model of how lists and dicts map to DataFrames so I understand data structure conversion

**Acceptance Criteria:**
- Fix textbook explanation that says "both lists and dictionaries can be converted into Pandas rows"
- Clarify: List of dicts → table (each dict = row), List of lists → table (each list = row)
- Use mental model: List = Table, Dictionary = Row
- Map to SQL concepts: list of dicts → SELECT result set, dict → record/row, dict keys → column names
- Update in PAIP_TEXTBOOK.md Day 1-2 section where interview connection is mentioned

**Story 5: Add Intuition Entries for Core Concepts** (Small)
- As a student, I want intuition entries for confusing deduplication and data structure patterns so I understand the design rationale

**Acceptance Criteria:**
- Add INTUITIONS.md entry: "Deduplication: dict.fromkeys() vs set()" covering order preservation difference
- Add INTUITIONS.md entry: "Lists and Dicts as DataFrame Structures" covering List = Table, Dict = Row mental model
- Both entries follow template format with SQL mappings and interview strategy
- Explain when to use each approach and why it matters in analytics context

**Story 6: Add Iteration Patterns to Quick Reference** (Small)
- As a student, I want iteration syntax in the quick reference so I can quickly recall loop patterns during practice

**Acceptance Criteria:**
- Add iteration section to QUICK_REFERENCE.md
- Include: for loops, while loops, enumerate(), zip(), range()
- Include: break, continue, else clauses
- Include common patterns: iterating dicts (.items(), .keys(), .values())
- Keep concise quick-reference format (syntax only, minimal explanation)

**Story 7: Add Dict/Set Edge Cases to Textbook** (Small)
- As a student, I want to know edge cases like `{}` creating a dict not a set so I can handle interview gotcha questions

**Acceptance Criteria:**
- Add to PAIP_TEXTBOOK.md Day 1-2 Sets section: `{}` creates empty dict, use `set()` for empty set
- Explain why: dict came first in Python, gets precedence for `{}`
- Add to common interview questions/gotchas
- Include example showing the difference

**Story 8: Clarify Set Difference vs Symmetric Difference** (Small)
- As a student, I want clear explanation of set difference (-) vs symmetric difference (^) so I understand when to use each

**Acceptance Criteria:**
- Expand PAIP_TEXTBOOK.md Day 1-2 Sets section with clear examples
- Difference (a - b): Elements in a but NOT in b
- Symmetric difference (a ^ b): Elements in EITHER a or b but NOT BOTH (XOR logic)
- Include visual examples showing the difference
- Add use case for each operation
- Add INTUITIONS.md entry: "Set Difference vs Symmetric Difference" with SQL analogy and when to use each

**Story 9: Evaluate Better Approach for INTUITIONS.md Management** (Small)
- As platform developers, we need to determine the right location and update strategy for INTUITIONS.md

**Acceptance Criteria:**
- Evaluate current placement in platform/content/student/docs/
- Determine if location/update mechanism needs to change
- Document decision rationale in ROADMAP or DEVELOPMENT_PROCESS

**Story 10: Rename "Practice Problems" to "Practice Examples"** (Small)
- As a student, I want accurate heading that distinguishes examples from exercises

**Context:** This is the second time this has been raised and not fixed.

**Acceptance Criteria:**
- Find all instances of "Practice Problems" heading in PAIP_TEXTBOOK.md
- Rename to "Practice Examples" 
- Ensure consistency across entire textbook

**Story 11: Textbook Coordinates All Learning Activities** (Medium)
- As a student, I want the textbook to direct me to exercises, flashcards, and Interview Mode after each day's content so I have a clear study path

**Acceptance Criteria:**
- After each day's content section in PAIP_TEXTBOOK.md, add learning activity block
- Direct to specific exercises (e.g., "Complete Exercises 1.1-1.5 in week1_exercises.py")
- Direct to relevant flashcards (e.g., "Review day1-2_flashcards.txt")
- Direct to Interview Mode practice (e.g., "Practice with INTERVIEW_MODE_WEEK1.md focusing on dictionaries and lists")
- Make textbook the central coordinator for complete learning flow
- Apply to all 7 days in Week 1

**Story 12: QA Automation Framework** (Large)
- As QA, I want automated tests that validate content dependencies, version consistency, and file structure so manual testing is faster

**Acceptance Criteria:**
- Create platform/tools/qa_automation.py script
- Automated tests: version string consistency across all docs, installer references correct zip, content dependency violations (from Story 3 audit), file structure validation, unit test checklist presence
- Script returns exit code 0 (pass) or 1 (fail) for CI integration
- Generate test report with pass/fail details
- Add to DEVELOPMENT_PROCESS.md as pre-QA delivery step
- Update UNIT_TEST_CHECKLIST to reference automated tests

**QA Status:** Pending build

**Story 9 Resolution:** INTUITIONS.md remains in platform/content/student/docs/ as platform-maintained content. It updates with each platform release via normal zip extraction. Students can reference it but platform owns canonical content. Personal student notes go in study/notes/.

### v1.0.5-RC4 - Process Documentation & Onboarding
**Target:** Next release candidate
**Status:** Planned

**User Stories:**

**Story 1: Implement Immediate Logging Rule** (Small)
- As developers, we want all mentioned items logged immediately in ROADMAP so nothing gets lost between sessions

**Acceptance Criteria:**
- Update DEVELOPMENT_PROCESS.md with handover activities section
- Document immediate logging rule: any item mentioned in conversation gets logged as story before session ends
- Add onboarding activity: scan critical platform/student docs to understand guiding principles, process, goals
- Document that ROADMAP is single source of truth for all planned work
- Add to developer responsibilities: "Log any discussed item as story before session ends"
- Include guidance on efficient onboarding approach to minimize token usage

**Story 2: Create Platform Onboarding Document** (Medium)
- As a new Claude session, I want a consolidated onboarding document so I can quickly understand platform principles, goals, and process without scanning multiple documents

**Acceptance Criteria:**
- Create platform/content/platform/docs/ONBOARDING.md
- Extract and consolidate key sections from critical platform docs (DEVELOPMENT_PROCESS, PLATFORM_ARCHITECTURE, ROADMAP)
- Extract and consolidate key sections from critical student docs (LEARNING_GUIDE, PAIP_TEXTBOOK)
- Include: guiding principles, target audience (Analytics Engineers), platform goals, development process overview, quality standards, content philosophy
- Optimize for token efficiency: condensed format, essential information only
- Document what was selected and why (serves as template for future doc creation)
- Link to full documents for deep dives when needed

**Story 3: Complete QA Automation Integration** (Small)
- As developers and QA, we want QA automation properly integrated into process docs and checklists so it's actually used

**Context:** Story 12 from RC1 created qa_automation.py but didn't complete all acceptance criteria

**CRITICAL PROCESS VIOLATION:** Delivered automation feature without testing the automation itself. This type of self-referential gap (QA tools not QA'd) must be avoided at all costs - if we automate testing but don't test the automation, we've introduced risk instead of reducing it

**Acceptance Criteria:**
- Add to DEVELOPMENT_PROCESS.md as pre-QA delivery step (run qa_automation.py before creating deliverables)
- Update UNIT_TEST_CHECKLIST to reference automated tests (add test that runs qa_automation.py)
- Add v1.0.5-RC1 section to QA_CHECKLIST.md with qa_automation test step
- Verify qa_automation.py runs successfully as part of test

**Story 4: Implement AC Verification Before QA Delivery** (Small)
- As Dev, I want mandatory acceptance criteria verification before creating deliverables so incomplete stories don't reach QA

**Context:** Story 12 had explicit AC "Update UNIT_TEST_CHECKLIST to reference automated tests" but was delivered without completing it

**Acceptance Criteria:**
- Add "AC Verification" step to DEVELOPMENT_PROCESS.md "Building an RC" section
- Step must occur before "Create deliverables bundle"
- Process: Review each story's acceptance criteria, verify each is met, mark incomplete stories as such in ROADMAP
- If any AC incomplete, story status must reflect partial completion
- Document that partial completion is acceptable IF documented, but undocumented gaps are process violations

**Story 5: Fix bootstrap.py Wing IDE f-string Syntax Error** (Small)
- As a user, I want bootstrap.py to complete without errors so installation is clean

**Context:** Story 1 (Wing IDE window size) introduced f-string syntax error at line 435. Dictionary literal inside f-string needs escaped braces.

**Acceptance Criteria:**
- Fix line 435-436 in bootstrap.py: Change `{'dock-state':` to `{{'dock-state':`
- Change `'window-state': 'normal'}` to `'window-state': 'normal'}}`
- Verify bootstrap.py executes without ValueError
- Test Wing IDE opens with configured window geometry

**Story 6: Remove Unused platform/content/patterns Folder** (Small)
- As developers, we want clean folder structure with no undocumented artifacts

**Context:** platform/content/patterns exists with only .gitkeep and __init__.py. Not documented in PLATFORM_ARCHITECTURE. Pattern library is in platform/content/student/src/patterns_and_gotchas.py, not in separate folder.

**Acceptance Criteria:**
- Remove platform/content/patterns/ folder entirely
- Verify installer artifact cleaning doesn't reference it
- Verify PLATFORM_ARCHITECTURE.md structure diagram is accurate (docs/, src/, data/ only under platform/content/)

**Story 7: Convert TOCs to Clickable Anchor Links** (Small)
- As a reader, I want clickable TOC links so I can navigate directly to sections

**Context:** Current TOCs are plain text lists. Markdown supports anchor links: `[Section Name](#section-name)`

**Acceptance Criteria:**
- Convert TOCs in PAIP_TEXTBOOK.md to anchor links
- Convert TOCs in LEARNING_GUIDE.md to anchor links  
- Convert TOCs in INTERVIEW_MODE_WEEK1.md to anchor links
- Verify all links work (test clicking in markdown viewer)
- Format: `[Day 1-2: Data Structures](#day-1-2-data-structures-2-hours)` 

**Story 8: Fix Code Block Line Length in Sets Section** (Small)
- As a reader, I want all text visible in code blocks without horizontal scrolling

**Context:** Lines 185 and 196 in PAIP_TEXTBOOK.md sets section truncate "BOTH" in UI (content exists when copied, but display cuts off)

**Acceptance Criteria:**
- Shorten line 185: Break into multi-line comment or abbreviate
- Shorten line 196: Break into multi-line comment
- Keep all code block lines under 80 characters for readability
- Verify no truncation in markdown viewers

**Story 9: Add SQL Analogies to Set Operations** (Small)
- As a student, I want SQL analogies for set operations so I can map Python concepts to my SQL knowledge

**Acceptance Criteria:**
- Add SQL analogies to PAIP_TEXTBOOK.md sets section (a - b and a ^ b examples)
- Use concrete column name (customer_id) instead of SELECT *
- Show: a - b = EXCEPT, a ^ b = double EXCEPT with UNION
- Create INTUITIONS.md entry: "Set Operations and SQL Analogies"
- Include when to use each operation in analytics context

**Story 10: Add Flashcard for Empty Dict/Set Gotcha** (Small)
- As a student, I want a flashcard for the `{}` gotcha so I can practice this common interview trap

**Context:** Story 7 from RC1 added empty dict/set gotcha to textbook but didn't create corresponding flashcard

**Acceptance Criteria:**
- Add flashcard to day1-2_flashcards.txt
- Q: "What does `{}` create in Python? How do you create an empty set?"
- A: "`{}` creates empty dict (not set). Use `set()` for empty set. Dict came first in Python, gets precedence for `{}`"
- Follow flashcard format from existing cards

**Story 11: Add Textbook/Flashcard Sync Check to Process** (Small)
- As developers, we want mandatory flashcard sync checks when modifying textbook so students can practice all concepts

**Acceptance Criteria:**
- Add to DEVELOPMENT_PROCESS.md "Building an RC" section
- When modifying PAIP_TEXTBOOK.md: check if new concepts need flashcards
- When adding examples, gotchas, or key concepts: create corresponding flashcard
- Add to AC verification step: "Textbook changes include flashcard updates if needed"
- Document in process that textbook and flashcards must stay in sync

**Story 12: Suppress Wing IDE Run Arguments Dialog** (Small)
- As a user, I want Wing to execute scripts without prompting for run arguments every time

**Acceptance Criteria:**
- Research Wing IDE configuration options to suppress run arguments dialog
- Add configuration to bootstrap.py .wpu file generation if possible
- Test that scripts execute directly without dialog popup
- Document configuration in bootstrap.py comments

**Story 13: Preserve Wing .wpu User Customizations** (Small)
- As a user, I want my Wing IDE customizations (window docking, layout) preserved across reinstalls

**Context:** Bootstrap regenerates .wpu on every install, overwriting user customizations like window docking. .wpr (project file) preserves settings like font, but .wpu (user file) gets reset.

**Acceptance Criteria:**
- Modify bootstrap.py _generate_wpu_file() to check if .wpu exists before creating
- Only generate .wpu on first install (when file doesn't exist)
- On subsequent installs, skip .wpu generation to preserve user customizations
- Document in bootstrap.py: .wpu contains user-specific layout preferences

**Story 14: Update Comprehension Preliminary Intuition** (Small)
- As a student, I want accurate preliminary intuition for comprehensions that includes filtering

**Context:** Current preliminary intuition says "build a list by looping through something" but doesn't mention the optional condition/filter element

**Acceptance Criteria:**
- Update PAIP_TEXTBOOK.md comprehension preliminary intuition
- Change to: "build a list by looping through something and optionally filtering items"
- Ensure it appears before first comprehension example in Day 1-2

**Story 15: Clarify Built-in Types Don't Need Import** (Small)
- As a student, I want to understand which types are built-in so I know when imports are needed

**Context:** Example 1.2 uses `dict` and `list` without importing, but this isn't explained

**Acceptance Criteria:**
- Add to PAIP_TEXTBOOK.md Day 1-2: Section explaining built-in types
- List built-in types: int, str, list, dict, set, tuple, bool
- List built-in functions: print(), len(), range(), enumerate(), zip(), sorted(), sum(), max(), min()
- Explain these are always available without import
- Add flashcard to day1-2_flashcards.txt: "Which Python types and functions are built-in (don't need import)?"

**Story 16: Add zip() for Creating Dicts from Keys+Values** (Small)
- As a student, I want to understand how to create dicts from separate key and value lists

**Context:** dict.fromkeys() creates dict from keys only (values=None). Need to show zip() for pairing keys with values.

**Acceptance Criteria:**
- Add to PAIP_TEXTBOOK.md dict section (near dict.fromkeys())
- Show dict.fromkeys(keys) creates keys with None values
- Show dict(zip(keys, values)) creates keys paired with values
- Add example: keys=['a','b','c'], values=[1,2,3]
- Explain function vs method: zip() is a function (standalone), dict.fromkeys() is a method (attached to dict object)
- Functions called as: function(args). Methods called as: object.method(args)
- Add flashcard to day1-2_flashcards.txt: "How do you create a dict from separate key and value lists?"
- Add flashcard to day1-2_flashcards.txt: "What's the difference between a function and a method?"

**Story 17: Implement Global Sequential Story IDs** (Small)
- As developers, we want unique story identifiers that persist across version migrations so we can track stories without renumbering

**Context:** Current numbering (Story 1, Story 2) is version/RC-specific. When stories migrate from RC2 to next version's RC1, numbering creates ambiguity.

**Acceptance Criteria:**
- Implement global sequential ID system: PAIP-001, PAIP-002, etc.
- IDs never change regardless of version/RC migration
- Update ROADMAP.md story format to include ID: "**PAIP-XXX: Story Name** (Size)"
- Add to RELEASE_NOTES: Map story IDs to version where implemented
- Update DEVELOPMENT_PROCESS.md with story ID assignment process
- Retroactively assign IDs to existing RC2 stories (PAIP-001 through PAIP-018)

**Story 18: Rename Example 1-1 to "Filter Odds"** (Small)
- As a student, I want accurate example names that reflect what the filter blocks

**Context:** Example 1-1 currently named "Filter Evens" but filter blocks odds (lets evens through). Filter terminology means "block/remove."

**Acceptance Criteria:**
- Rename Example 1-1 in PAIP_TEXTBOOK.md from "Filter Evens" to "Filter Odds"
- Update any references to this example name elsewhere in textbook
- Verify naming is consistent with filter terminology (filter blocks what's named)

**Story 19: Add Validation Logic to Example 1.3** (Small)
- As a student, I want to understand why .copy() is used and see the merge validated

**Context:** Example 1.3 uses `.copy()` without explaining why (preserves dict1 for validation). Example ends without validating the merge worked correctly.

**Acceptance Criteria:**
- Add comment before `.copy()`: "# Copy dict1 to preserve original for validation"
- After merge loop, add validation logic that confirms operation
- Validation should check: all keys present, higher values kept per key
- Example: verify merged['b'] == 25 (not 20), merged['c'] == 30 (not 15)
- Complete example shows both operation AND verification pattern

**Story 20: Add Execution Code to All Function Examples** (Medium)
- As a student, I want to run function examples in debug mode and watch variables

**Context:** Examples that define functions (like Example 1-4) don't show how to execute them. Students need execution code to run in debug and observe behavior.

**Acceptance Criteria:**
- Audit PAIP_TEXTBOOK.md for all examples that define functions
- Add execution code after each function definition
- Execution code should: call the function with test data, show expected output
- Enable students to copy/paste example into IDE, set breakpoint, run in debug
- Apply to Week 1 examples first, document pattern for future weeks
- Example format: function def → test_data → function call → output comment

**Story 21: Document Debug Workflow in LG and TB** (Small)
- As a student, I want clear guidance on using debug mode to learn from examples

**Acceptance Criteria:**
- Add to LEARNING_GUIDE.md: Section explaining debug workflow benefits (see execution order, watch data transform, understand mutation)
- Add to PAIP_TEXTBOOK.md Day 1-2: Specific instructions for debug workflow
- Instructions: Create week1_examples.py in study/practice_work/, copy examples, set breakpoints, run in debug, watch variables
- Explain this is superior to passive reading for building mental models
- Apply pattern to each week's content introduction

**Story 22: Refocus GETTING_STARTED on Bootstrap Explanation** (Small)
- As a user, I want GETTING_STARTED.md to explain what bootstrap automates rather than manual setup steps

**Context:** Installation is now fully automated. GETTING_STARTED should explain what bootstrap does, not how to do manual setup.

**Acceptance Criteria:**
- Rewrite GETTING_STARTED.md to focus on bootstrap automation
- Explain: venv creation, PowerShell profile setup, Wing IDE configuration, git initialization
- Document what bootstrap configures automatically
- Remove manual step-by-step instructions (now obsolete)
- Keep troubleshooting section if applicable

**Story 23: Replace Example 1-4 with Appropriate Debug Example** (Small)
- As a student, I want Day 1-2 debug example that uses only covered concepts and shows clear wrong vs right

**Context:** Example 1-4 (iteration mutation) is edge case that doesn't reliably demonstrate bug and uses unexplained enumerate(). Need debug example matching comprehension/dict fundamentals level.

**Acceptance Criteria:**
- Replace Example 1-4 with debug example using only Day 1-2 concepts
- Example should show obvious wrong output vs correct output
- Candidate bugs: off-by-one indexing, wrong comparison operator in comprehension filter, dict KeyError handling, or simple logic error
- Must work with debug workflow (copy to week1_examples.py, run, observe wrong vs right)
- Keep "broken" vs "fixed" pattern but with reliable, clear demonstration
- Update corresponding exercise in week1_exercises.py if one exists
- Update corresponding flashcard in day1-2_flashcards.txt if one exists

**Story 24: Track Content Dependency Violations for Test Cases** (Small)
- As developers, we want discovered violations documented so they can become test cases for QA automation

**Context:** Manual review discovering violations: .items() before explained, import/string module before explained, enumerate() before explained

**Acceptance Criteria:**
- Create platform/tools/dependency_violations_tracker.md
- Document each discovered violation: what was used, where, what should have been explained first
- Format: location, violation description, severity
- Use tracked violations to create test cases for qa_automation.py
- Story 3's audit will find more violations - add all to tracker
- Feed tracker into automated tests to prevent regression

**QA Status:** Pending build

**Story 25: Document DE/AE Role Confusion Pattern in Onboarding** (Small)
- As a new Claude session, I want to understand the DE/AE role confusion pattern so I can recognize when "Data Engineer" JDs are actually Analytics Engineer roles

**Context:** Industry uses Data Engineer and Analytics Engineer titles interchangeably. JDs titled "Data Engineer" with dbt/Snowflake/Fivetran are actually Analytics Engineer roles where Python is gatekeeping, not core job function.

**Acceptance Criteria:**
- Update ONBOARDING.md with section on recognizing mislabeled roles
- Key signal: dbt listed as "plus" = actually Analytics Engineer role
- Pattern: Snowflake + Fivetran + dbt = warehouse-focused (not lake/swamp)
- Document that Python/PySpark appears as gatekeeping even when dbt handles real work
- Explain this is exactly what PAIP targets: getting past Python gatekeeping for dbt/SQL roles
- Add example JD showing this pattern (Staff Data Engineer with dbt as plus)

---

## Rejected RCs

### v1.0.5-RC1 - Content Quality & QA Automation (Rejected)
**Rejected:** October 8, 2025
**Reason:** 24 content quality and process violations: content dependency violations (.items(), import, string module, enumerate(), translate(), maketrans(), punctuation, split(), get(), sorted(), lambda, str() used before explained), missing flashcard sync, incomplete Story 12 AC delivery, process documentation gaps, Example 1-4 flawed, missing execution code for function examples

**Completed Work in RC1:**
- Story 1: Wing IDE window size preference (partial - f-string error)
- Story 2: RC-to-version migration documentation
- Story 3: Content dependency audit framework (not executed)
- Story 4: Lists vs dicts DataFrame mental model
- Story 5: Intuition entries for deduplication and data structures
- Story 6: Iteration patterns in quick reference
- Story 7: Dict/set edge cases (empty dict gotcha)
- Story 8: Set difference vs symmetric difference
- Story 9: INTUITIONS.md location resolution
- Story 10: "Practice Problems" rename (not completed)
- Story 11: Textbook coordinates learning activities
- Story 12: QA automation framework (partial - integration incomplete)

### v1.0.4-RC3 - RC2 Rejection Fixes (Rejected)
**Rejected:** October 7, 2025
**Reason:** Student folder structure missing from installation (files moved in workspace but not included in zip correctly; flawed unit test checked path string instead of actual files)

**Completed Work in RC3:**
- Documentation reorganization: Created platform/content/student/ and platform/content/platform/ folder structures
- Added TOCs to PAIP_TEXTBOOK, LEARNING_GUIDE, INTERVIEW_MODE
- Renamed quick_reference.md → QUICK_REFERENCE.md
- Renamed talking_points.md → TALKING_POINTS.md
- Split 74 flashcards into day1-2 through day7 files (daily learning packages)
- Created daily exercise wrappers (day1-2_exercises.py through day7_exercises.py)
- Fixed dict.fromkeys content dependency (added to Essential Built-in Functions section)
- Detailed comprehension evaluation order in PAIP_TEXTBOOK.md (lines 360-395)

### v1.0.4-RC2 - Airflow Integration & RC1 Fixes (Rejected)
**Rejected:** October 7, 2025
**Reason:** Installer referenced wrong zip filename (v1.0.4-RC3.zip instead of v1.0.4-RC3.zip)

**Completed Work in RC1:**
- Created INTUITIONS.md template with list comprehension entry
- Added comprehension deep-dive to textbook
- Added Essential Built-in Functions section before examples
- Clarified "ordered" vs "sorted" in lists section
- Added result examples to quick_reference.md
- Expanded flashcards from 50 to 74 (+24 method cards)
- Documented Wing IDE Git integration
- Added token budget tracking to DEVELOPMENT_PROCESS.md
- Added backlog refinement section to DEVELOPMENT_PROCESS.md

---

## Completed Versions

### v1.0.4 (Released - October 7, 2025)

Testing infrastructure and content refinements with student/platform folder reorganization.

**Delivered in RC4:**
- Student folder structure properly packaged (platform/content/student/ and platform/content/platform/)
- Documentation reorganization with TOCs
- Daily learning packages (flashcards and exercises split by day)
- Fixed dict.fromkeys content dependency
- Renamed quick_reference.md → QUICK_REFERENCE.md, talking_points.md → TALKING_POINTS.md
- Detailed comprehension evaluation order explanation
- Versioned unit test checklist (UNIT_TEST_CHECKLIST-vX.X.X-RCX.md)
- RC version shown in install.log

**Key Features:**
- TDD structure: week1_exercises.py (stubs), test_week1_exercises.py (harness), week1_solutions.py (solutions)
- 29 patterns (24 data manipulation + 5 testing/validation)
- Python Prerequisites section extracted from patterns
- 74 flashcards (expanded from 50)
- Extended thinking + voice mode for Interview Mode
- Exercise references in textbook
- DEVELOPMENT_PROCESS.md recreated
- PLATFORM_ARCHITECTURE.md updated

### v1.0.2 (Released)

Week 1 foundation content with textbook and pattern library.

**Key Features:**
- PAIP_TEXTBOOK.md with Week 1 Python fundamentals
- LEARNING_GUIDE.md with 24-pattern library
- 20 exercises, 35 flashcards
- Interview Mode framework and schedule

### v1.0.1 (Released)

Development environment with Wing IDE integration.

---

## Product Backlog (Unscheduled)

Items logged for future consideration, not yet assigned to a release version.

### Development Tools
- Jira/Claude Integration: Explore Atlassian Rovo MCP server for Claude Desktop (bi-directional sync between ROADMAP.md and Jira)

### Interview Mode Enhancements
- Pattern contribution workflow: "Submit New Pattern" form for interviewers/users
- Potential lead generation: interviewers who contribute become prospects

### Analytics & Reporting
- Interview Mode Analytics: Session data capture, CSV/JSON export, Snowflake schema, Tableau dashboards

### Content Gaps
- Multi-pattern capstone project (exercises currently isolated)
- Systematic debugging drill framework (current debug exercises ad-hoc)
- **Data Migration Validation Pattern:** Use symmetric difference (XOR) to detect migration defects between legacy and next-gen systems. Empty result = perfect migration, non-empty = report what's in legacy only vs next-gen only. Critical for Analytics Engineers on system migration projects.

### Platform Features
- **JD-Specific Interview Prep Packages:** Integrated feature for generating customized interview prep content based on job description and interview type. Includes JD parser, skill extraction, targeted content generation (quick reference, flashcards, Interview Mode scenarios), and packaging system.

### Content Expansion
- Weeks 2-3 content (DataFrame basics + aggregation patterns)
- Weeks 4-5 content (Ranking/windows + advanced patterns)
- Weeks 6-7 content (Integration + meta-patterns)
- **PySpark Basics (Week 8+):** DataFrame API fundamentals for "Data Analytics Engineer" JD screening
- **PySpark Basics (Week 8+):** DataFrame API fundamentals - select(), filter(), groupBy().agg(). Cover enough to pass "nice to have" screening in Data Analytics Engineer JDs. Map pandas patterns to PySpark equivalents.

---

## Future Releases

### v1.0.4 (In Progress)
Content order and learning framework improvements.

### v1.0.5 (Planned)
Week 2 content (DataFrame basics + first pattern versions).

