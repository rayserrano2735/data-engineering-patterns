# PAIP Development Process
**Version: 1.0.5-RC4

This document defines the complete development workflow for PAIP platform, including RC builds, unit testing, QA testing, and release cycles.

## Table of Contents

1. [Process Overview](#process-overview)
2. [Dev Responsibilities](#dev-responsibilities)
3. [QA Responsibilities](#qa-responsibilities)
4. [Key Principles](#key-principles)

---

## Process Overview

```
Dev builds RC → Unit tests → Delivers to QA → QA tests → Certification or Rejection
```

**Key stages:**
1. Dev logs changes in ROADMAP
2. Dev builds RC and runs unit tests
3. Dev delivers to QA with unit test results
4. QA tests against QA_CHECKLIST
5. QA certifies or rejects
6. If rejected: Dev logs reasons, builds next RC
7. If certified: Tag release, start next version

---

## Dev Responsibilities

### Autonomous vs Go-Ahead Decisions

**Autonomous:**
- Technical implementation
- Code structure
- Unit test design
- Documentation
- Bug fixes from QA
- RC increments

**Requires go-ahead:**
- New features not in ROADMAP
- Process changes
- Breaking changes
- Major architecture decisions
- Scope changes

**Principle:** Optimize for velocity within scope. When uncertain, do it and note in ROADMAP.

### Handover Activities

**Onboarding (New Session):**
1. Read ONBOARDING.md for quick orientation
2. Check ROADMAP.md "In Progress" section for current RC
3. Check dependency_violations_tracker.md for known issues
4. Orient to current process state before asking questions

**Immediate Logging Rule:**
- **Any item mentioned in conversation → logged as story before session ends**
- ROADMAP is single source of truth for all planned work
- No items should be lost between sessions
- If discussion leads to new work, log it immediately

**Developer Responsibilities:**
- Log discussed items as stories before session ends
- Verify all acceptance criteria before delivery
- Run qa_automation.py before creating deliverables
- **Sync flashcards when modifying textbook:** New concepts/gotchas/examples require corresponding flashcards
- Check textbook changes include flashcard updates in AC verification

### User Story Format (Standard as of v1.0.4)

All ROADMAP entries must use user story format:

**Structure:**
```
**Story N: [Name]** (Size: Small/Medium/Large)
- As a [role], I want [feature] so that [benefit]

**Acceptance Criteria:**
- Specific deliverable 1
- Specific deliverable 2
- Testable outcome 3
```

**Sizing:**
- **Small:** <2 hours, single file/section changes
- **Medium:** 2-4 hours, multiple related changes
- **Large:** 4+ hours, significant new content or features

**Good story names:**
- "Installer Version Consistency Fix"
- "Week 2 Day 1 - Modern Python Patterns"
- "Documentation Updates"

**Poor story names:**
- "Fix stuff"
- "Updates"
- "RC2 changes"

**Example:**
```
**Story 1: PowerShell Hybrid Installer** (Small)
- As a user, I want to double-click the installer and have it run in PowerShell so I'm using our standardized shell

**Acceptance Criteria:**
- Create paip-install-vX.X.X.bat (launcher, 1 line)
- Create paip-install-vX.X.X.ps1 (actual installer logic)
- .bat calls .ps1 with ExecutionPolicy Bypass
- User can double-click .bat to run
```

### Building an RC

**Critical: Copy previous RC files, don't recreate from scratch**

When building a new RC:
1. Copy previous RC installer → new RC installer
2. Copy previous RC platform zip → workspace (will rebuild)
3. Change only version strings in copied files
4. Apply new changes to platform files
5. **AC Verification:** Review each story's acceptance criteria, verify all met, mark partial completion if any AC incomplete
6. **Run qa_automation.py** before creating deliverables to validate:
   - Version string consistency
   - File structure
   - Content dependencies (from violations tracker)
7. Rebuild platform zip
8. Never recreate installer from memory - prevents introducing new bugs

**Example:**
```bash
# Copy RC1 installer to RC2
cp paip-install-v1.0.4-RC1.bat paip-install-v1.0.4-RC3.bat

# Update only version strings, apply changes, rebuild
```

**Build steps:**
1. Log changes in ROADMAP using user story format
2. Copy previous RC files (installer, platform)
3. Update doc versions
4. Build deliverables (platform zip, installer)
5. Run unit tests
6. Copy unit test checklist to outputs
7. Deliver to QA

### Unit Testing

**Mandate:** Dev owns unit testing. Test everything that can be tested automatically.

Run automated tests before QA delivery. Document results in UNIT_TEST_CHECKLIST.md.

**Standard tests:**
- Installer version consistency (filename matches zip filename)
- Installer references correct zip file
- Platform zip contents
- Doc version consistency across all files
- QA_CHECKLIST structure
- ROADMAP structure
- Python syntax check
- File counts
- Content validation
- Version string alignment

Only deliver to QA when all tests pass.

### After QA Reports Findings

1. Review findings
2. Log rejection reasons in ROADMAP
3. Log fixes in new RC section
4. Apply fixes
5. Increment RC number
6. Run unit tests
7. Deliver new RC

### After QA Certification

1. Move certified RC to "Completed Versions" in ROADMAP
2. QA tags release (e.g., v1.0.4)
3. Migrate any RC5+ items to next version RC1
4. Start new version (e.g., v1.0.5-RC1)

**RC Migration Pattern:**

When RC4 is certified:
- RC4 → v1.0.4 (completed/tagged)
- RC5 items → v1.0.5-RC1 (migrated to next version)
- RC6+ items → v1.0.5-RC4, RC3, etc. (migrate sequentially)

When RC4 is rejected:
- RC4 → Rejected RCs (logged with rejection reason)
- RC5 items → Stay as RC5 (become next candidate)
- Continue RC sequence within same version

**Example - Certification Path:**
```
During RC4 testing: Log new items to RC5, RC6, etc.
QA certifies RC4 → Tag as v1.0.4
Next build: v1.0.5-RC1 (contains all RC5 items)
           v1.0.5-RC4 (contains all RC6 items)
           etc.
```

**Example - Rejection Path:**
```
During RC4 testing: Log new items to RC5, RC6, etc.
QA rejects RC4 → Log rejection reason, move to Rejected RCs
Next build: v1.0.4-RC5 (fix RC4 issues + implement RC5 items)
Continue: RC6, RC7, etc. stay within v1.0.4 until certified
```

---

## QA Responsibilities

### Testing an RC

Test against QA_CHECKLIST.md using:
- Windows environment
- Fresh installation
- Complete checklist walkthrough

### Reporting Findings

Document:
- Specific failures
- Reproduction steps
- Severity

### Certification Decision

**Certify:** All critical items pass
**Reject:** Any critical item fails

### Notification Protocol

**QA will notify Dev of certification or rejection.** Dev does not ask for status updates - QA testing takes as long as needed and QA will communicate when determination is reached.

---

## Key Principles

1. **No Piecemeal Changes:** New RC for any change after QA delivery
2. **Explicit QA Decision:** Certify or reject explicitly
3. **Complete Logging:** All rejections logged with reasons
4. **Unit Tests Gate QA:** Only deliver passing unit tests
5. **Historical Preservation:** Complete RC history in ROADMAP/QA_CHECKLIST


---

## Token Budget Tracking

**Purpose:** Monitor conversation token usage to prepare for handover before hitting limits.

**Tracking intervals:**
- Before/after builds (show cost)
- At milestone requests
- At 80% threshold (152k tokens) → Start wrapping up
- At 90% threshold (171k tokens) → Prepare handover immediately

**Not tracked:** Routine messages to reduce token overhead

**Build token cost reporting:**
```
Starting build at 75,000 tokens...
[build process]
Build complete at 85,000 tokens. Cost: 10,000 tokens
```

---

## Backlog Refinement

**Purpose:** Review, prioritize, and prepare backlog items for future sprints.

**When to refine:**
- After RC certification (before starting next version)
- When backlog reaches 10+ items
- When priorities shift

**Refinement activities:**
1. **Review items:** Read each backlog item, clarify requirements
2. **Estimate size:** Small/Medium/Large
3. **Prioritize:** Which items next version? Which later?
4. **Break down:** Split large items into manageable stories
5. **Group related:** Combine related items into single story
6. **Archive old:** Remove obsolete or rejected items

**Example refinement:**
```
Before: 15 unorganized backlog items
After: 
- 5 items ready for v1.0.5 (sized, prioritized)
- 7 items remain in backlog
- 3 items archived (obsolete)
```

---

## Handover Efficiency

**Purpose:** Minimize token waste and ramp-up time when continuing work after conversation limits.

**Handover Document Requirements:**

1. **Current State:**
   - Actual file structure (Day counts, line numbers, section locations)
   - Accurate metrics (hours, flashcards, patterns)
   - RC rejection reasons if applicable

2. **No Conflicts:**
   - Verify Day/section numbers against actual files
   - Check version strings match reality
   - Resolve any numbering/naming inconsistencies before handover

3. **Explicit Decisions:**
   - Pre-resolve ambiguities where possible
   - Document assumptions made
   - Specify "requires decision" vs "already decided"

4. **Autonomous Execution Zones:**
   - Clearly mark what Dev can decide independently
   - Separate "build this" from "discuss approach first"

**AI Execution Guidelines:**

1. **Make reasonable decisions autonomously:**
   - Industry standard approaches
   - Consistency with existing patterns
   - Technical implementation details

2. **Batch questions:**
   - Group 3-5 related questions
   - Don't sequential-interview through decisions

3. **Execute first, ask when blocked:**
   - Build with reasonable assumptions
   - Document decisions made
   - Only stop for true blockers

4. **Minimize context dump:**
   - Read docs systematically (one at a time)
   - Don't dump full analysis unless requested
   - Focus on execution over theorizing

