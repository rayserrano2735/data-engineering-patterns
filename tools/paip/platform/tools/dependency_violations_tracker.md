# Content Dependency Violations Tracker
**Version: 1.0.5-RC3**

This document tracks discovered content dependency violations for use in QA automation test cases.

## Violation Format
- **Location**: File and line/section
- **Violation**: What was used before being explained
- **Severity**: Critical/High/Medium/Low
- **Fix Required**: What needs to be explained first

---

## Discovered Violations (Day 1-2)

### Example 1-3: dict.items()
- **Location**: PAIP_TEXTBOOK.md, Example 1.3, line ~341
- **Violation**: `.items()` method used without prior explanation
- **Severity**: High
- **Fix Required**: Explain `.items()`, `.keys()`, `.values()` before Example 1.3

### Example 1-4: enumerate()
- **Location**: PAIP_TEXTBOOK.md, Example 1.4, line ~351
- **Violation**: `enumerate()` used without prior explanation
- **Severity**: High
- **Fix Required**: Explain `enumerate()` in iteration section before Example 1.4

### Example 1-5: Multiple violations
- **Location**: PAIP_TEXTBOOK.md, Example 1.5
- **Violations**:
  - `import` statement not explained
  - `string` module not explained
  - `str()` function not explained
  - `translate()` method not explained
  - `maketrans()` function not explained
  - `punctuation` constant not explained
  - `split()` method not explained
  - `get()` dict method not explained
  - `sorted()` function not explained
  - `lambda` not explained
- **Severity**: Critical (10 violations in one example)
- **Fix Required**: Add "Essential Built-in Functions" and "Imports and Modules" sections before Example 1.5

---

## Systematic Audit Results (Story 3)
*To be populated by comprehensive platform-wide audit*

---

## Test Case Generation
These violations feed into qa_automation.py test cases:
- Test that each concept appears in textbook before first use
- Test that imports are explained before use
- Test that methods are documented before examples use them

