#!/usr/bin/env python3
"""
QA Automation Framework v1.0.5-RC1
Automated validation of platform consistency and structure
"""

import sys
import re
from pathlib import Path
import zipfile


class QAAutomation:
    """Automated QA tests for platform release validation."""
    
    def __init__(self, platform_dir):
        self.platform_dir = Path(platform_dir)
        self.errors = []
        self.warnings = []
        self.tests_run = 0
        self.tests_passed = 0
        
    def run_all_tests(self):
        """Execute all automated QA tests."""
        print("=" * 60)
        print("PAIP Platform QA Automation")
        print("=" * 60)
        print()
        
        # Run test suites
        self.test_version_consistency()
        self.test_installer_zip_reference()
        self.test_file_structure()
        self.test_unit_checklist_presence()
        self.test_content_dependencies()
        
        # Report results
        self.print_report()
        
        # Return exit code
        return 0 if len(self.errors) == 0 else 1
    
    def test_version_consistency(self):
        """Test that version strings are consistent across all docs."""
        print("Testing version consistency...")
        self.tests_run += 1
        
        # Extract version from ROADMAP
        roadmap = self.platform_dir / "content" / "platform" / "docs" / "ROADMAP.md"
        if not roadmap.exists():
            self.errors.append("ROADMAP.md not found")
            return
            
        roadmap_version = None
        with open(roadmap) as f:
            for line in f:
                if line.startswith("**Version:**"):
                    roadmap_version = line.split("**Version:**")[1].strip()
                    break
        
        if not roadmap_version:
            self.errors.append("Could not extract version from ROADMAP.md")
            return
        
        # Check all doc files for version consistency
        docs_to_check = [
            "content/platform/docs/DEVELOPMENT_PROCESS.md",
            "content/platform/docs/QA_CHECKLIST.md",
            "content/platform/docs/PLATFORM_ARCHITECTURE.md",
            "content/platform/docs/GETTING_STARTED.md",
            "content/student/docs/PAIP_TEXTBOOK.md",
            "content/student/docs/INTUITIONS.md"
        ]
        
        version_mismatches = []
        for doc_path in docs_to_check:
            full_path = self.platform_dir / doc_path
            if full_path.exists():
                with open(full_path) as f:
                    content = f.read()
                    if roadmap_version not in content:
                        version_mismatches.append(doc_path)
        
        if version_mismatches:
            self.errors.append(f"Version mismatch in: {', '.join(version_mismatches)}")
        else:
            self.tests_passed += 1
            print("  ✓ Version strings consistent")
    
    def test_installer_zip_reference(self):
        """Test that installer references correct zip filename."""
        print("\nTesting installer zip reference...")
        self.tests_run += 1
        
        # Find PowerShell installer file (contains zip reference)
        installer_patterns = ["paip-install-v*.ps1"]
        installer_file = None
        
        # Check in parent of platform dir
        parent_dir = self.platform_dir.parent
        for pattern in installer_patterns:
            matches = list(parent_dir.glob(pattern))
            if matches:
                installer_file = matches[0]
                break
        
        if not installer_file:
            self.warnings.append("Installer .ps1 file not found (may not be built yet)")
            return
        
        # Extract version from installer filename
        installer_match = re.search(r'v(\d+\.\d+\.\d+-RC\d+)', installer_file.name)
        if not installer_match:
            self.errors.append(f"Could not extract version from installer filename: {installer_file.name}")
            return
        
        installer_version = installer_match.group(1)
        
        # Read installer content
        with open(installer_file) as f:
            installer_content = f.read()
        
        # Check that installer references correct zip filename
        expected_zip = f"paip-platform-v{installer_version}.zip"
        if expected_zip not in installer_content:
            self.errors.append(f"Installer does not reference correct zip: {expected_zip}")
        else:
            self.tests_passed += 1
            print(f"  ✓ Installer references correct zip: {expected_zip}")
    
    def test_file_structure(self):
        """Test that required file structure exists."""
        print("\nTesting file structure...")
        self.tests_run += 1
        
        required_structure = {
            "content/student/docs": ["PAIP_TEXTBOOK.md", "LEARNING_GUIDE.md", "INTUITIONS.md", "QUICK_REFERENCE.md"],
            "content/student/src": ["week1_exercises.py", "test_week1_exercises.py", "week1_solutions.py"],
            "content/student/data": ["flashcards_complete.txt"],
            "content/platform/docs": ["ROADMAP.md", "DEVELOPMENT_PROCESS.md", "QA_CHECKLIST.md"]
        }
        
        missing_files = []
        for folder, files in required_structure.items():
            folder_path = self.platform_dir / folder
            if not folder_path.exists():
                missing_files.append(f"Folder missing: {folder}")
                continue
            
            for file in files:
                file_path = folder_path / file
                if not file_path.exists():
                    missing_files.append(f"{folder}/{file}")
        
        if missing_files:
            self.errors.append(f"Missing required files: {', '.join(missing_files)}")
        else:
            self.tests_passed += 1
            print("  ✓ All required files present")
    
    def test_unit_checklist_presence(self):
        """Test that unit test checklist exists with version."""
        print("\nTesting unit test checklist...")
        self.tests_run += 1
        
        # Look for versioned unit test checklist in parent dir
        parent_dir = self.platform_dir.parent
        checklist_pattern = "UNIT_TEST_CHECKLIST-v*.md"
        checklists = list(parent_dir.glob(checklist_pattern))
        
        if not checklists:
            self.errors.append("Unit test checklist not found (should be UNIT_TEST_CHECKLIST-vX.X.X-RCX.md)")
        else:
            self.tests_passed += 1
            print(f"  ✓ Unit test checklist found: {checklists[0].name}")
    
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
        
        with open(textbook) as f:
            content = f.read()
        
        # Check for list comprehension before explanation section
        comprehension_explanation = re.search(r'\*\*List Comprehension Basics:\*\*', content)
        if comprehension_explanation:
            before_explanation = content[:comprehension_explanation.start()]
            
            # Check for comprehension usage before explanation (excluding the evaluation order example)
            practice_examples_start = re.search(r'#### Practice Examples:', before_explanation)
            if practice_examples_start:
                examples_section = before_explanation[practice_examples_start.start():]
                if re.search(r'\[.+for .+ in .+\]', examples_section):
                    violations.append("List comprehension used in practice examples before basics explained")
        
        if violations:
            self.errors.append(f"Content dependency violations: {', '.join(violations)}")
        else:
            self.tests_passed += 1
            print("  ✓ No content dependency violations found")
    
    def print_report(self):
        """Print test execution report."""
        print("\n" + "=" * 60)
        print("QA Automation Report")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print()
        
        if self.errors:
            print("ERRORS:")
            for error in self.errors:
                print(f"  ✗ {error}")
            print()
        
        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
            print()
        
        if len(self.errors) == 0:
            print("✓ ALL TESTS PASSED")
        else:
            print("✗ TESTS FAILED - Fix errors before QA delivery")
        
        print("=" * 60)


def main():
    """Run QA automation from command line."""
    if len(sys.argv) > 1:
        platform_dir = Path(sys.argv[1])
    else:
        # Default: assume running from platform/tools/
        platform_dir = Path(__file__).parent.parent
    
    qa = QAAutomation(platform_dir)
    exit_code = qa.run_all_tests()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
