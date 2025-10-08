# Content Dependency Audit Methodology
**Version: 1.0.5-RC4
**Status:** In Progress
**Priority:** Critical - Third attempt at completion

## Guiding Principle

No concept, method, syntax pattern, or language feature may be used in any example, exercise, or explanation before it has been explicitly introduced and explained to the student.

## Audit Process

### Phase 1: Inventory (Automated)

Create inventory of ALL language features used across student-facing content:

**Files to audit:**
- platform/content/student/docs/PAIP_TEXTBOOK.md (PRIMARY)
- platform/content/student/docs/LEARNING_GUIDE.md
- platform/content/student/docs/QUICK_REFERENCE.md
- platform/content/student/src/*.py (exercise files)

**Categories to inventory:**
1. Built-in functions (len, sum, min, max, sorted, range, enumerate, zip, etc.)
2. String methods (.split, .join, .strip, .lower, .upper, .replace, etc.)
3. List methods (.append, .extend, .insert, .remove, .pop, .sort, etc.)
4. Dict methods (.get, .keys, .values, .items, .update, .fromkeys, etc.)
5. Set methods (.add, .remove, .discard, .union, .intersection, etc.)
6. Comprehension syntax (list, dict, set comprehensions)
7. Control flow (if/else, for, while, break, continue)
8. Function syntax (def, return, lambda, parameters, *args, **kwargs)
9. Operators (arithmetic, comparison, logical, membership)
10. Special syntax (slicing, unpacking, f-strings, etc.)

### Phase 2: Track First Usage vs First Explanation

For each item in inventory:
- WHERE first used (file, line number, context)
- WHERE first explained (file, section, line number)
- VIOLATION if used before explained

### Phase 3: Fix Violations

Priority order:
1. Critical: Textbook violations (students read linearly)
2. High: Exercise file violations  
3. Medium: Quick reference violations
4. Low: Learning guide violations (read non-linearly)

### Phase 4: Automated Testing

Add to qa_automation.py:
- Parse all student content
- Build usage/explanation index
- Flag violations automatically

## Known Violations (From Previous RCs)

### Fixed in RC1-RC3:
- ✓ dict.fromkeys - Added to Essential Built-in Functions before usage

### Fixed in RC4:
- ✓ Example 1.1 uses list comprehension before Day 3 explanation - Still needs fix

### Open Violations Requiring Fix:

**PAIP_TEXTBOOK.md:**

1. **List comprehension in Example 1.1 (Line ~270)**
   - Used: Day 1-2 section
   - Explained: Day 3 section (Line 372+)
   - Fix: Add comprehension basics before Example 1.1 OR change Example 1.1 to use for loop

2. **enumerate() usage**
   - Check if used before explained in Essential Built-in Functions

3. **String methods in examples**
   - Verify .split(), .join(), .strip() explained before first usage

4. **F-strings**
   - Check if used in examples before explained

5. **Lambda expressions**
   - Verify not used before Day 5 Lambda section

## Audit Status by File

### PAIP_TEXTBOOK.md
- Status: Partial audit completed
- Critical violations: List comprehension in Example 1.1
- Recommended: Full systematic audit needed

### LEARNING_GUIDE.md
- Status: Not yet audited
- Priority: Medium (non-linear reading)

### QUICK_REFERENCE.md
- Status: Not yet audited
- Priority: Medium (reference material, not instructional)

### Exercise files
- Status: Not yet audited
- Priority: High (students write code)

## Automated Test Implementation

Add to platform/tools/qa_automation.py:

```python
def test_content_dependencies(self):
    """Test that no concepts are used before explanation."""
    print("\nTesting content dependencies...")
    self.tests_run += 1
    
    # Parse PAIP_TEXTBOOK.md
    textbook = self.platform_dir / "content" / "student" / "docs" / "PAIP_TEXTBOOK.md"
    if not textbook.exists():
        self.errors.append("PAIP_TEXTBOOK.md not found")
        return
    
    violations = []
    
    # Check for list comprehension before Day 3
    with open(textbook) as f:
        content = f.read()
        
    # Find Day 3 start
    day3_match = re.search(r'### Day 3: Comprehensions', content)
    if day3_match:
        day3_start = day3_match.start()
        
        # Check for comprehension syntax before Day 3
        before_day3 = content[:day3_start]
        if re.search(r'\[.+for .+ in .+\]', before_day3):
            violations.append("List comprehension used before Day 3 explanation")
    
    if violations:
        self.errors.append(f"Content dependency violations: {', '.join(violations)}")
    else:
        self.tests_passed += 1
        print("  ✓ No content dependency violations found")
```

## Next Steps

1. Complete full systematic audit of PAIP_TEXTBOOK.md
2. Fix all critical violations
3. Implement automated testing
4. Audit remaining files
5. Document methodology for future content additions

## Progress Tracking

- [ ] Phase 1: Complete inventory
- [ ] Phase 2: Track all first usage vs explanation
- [x] Phase 3: Fix dict.fromkeys violation
- [ ] Phase 3: Fix list comprehension violation
- [ ] Phase 3: Fix remaining violations
- [ ] Phase 4: Implement automated testing

**Last Updated:** October 7, 2025 (v1.0.5-RC1)
