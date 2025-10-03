#!/usr/bin/env python3
"""
Setup Python Analytics Interview Prep Repository
VERSION: 3.2.6

Smart installer with runtime merge intelligence.
Detects existing state and applies appropriate updates.

USAGE:
    cd to your GitHub directory (or wherever you want the repo)
    python path/to/setup_python_interview_prep.py [options]
    
OPTIONS:
    --mode local   : Create/update local repository only (default)
    --mode docker  : Build Docker image only
    --mode all     : Create repository and build Docker image

PRESERVES:
    Your work in practice_work/, notes/, mock_interviews/ is never overwritten
    
UPDATES:
    All course materials to latest version
    Migrates flat structure to organized if needed
    Removes obsolete files automatically
"""

import os
import sys
import argparse
import base64
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Repository name
REPO_NAME = "python-analytics-interview-prep"

# Version
VERSION = "3.2.6"

# ============================================================================
# EMBEDDED CONTENT DEFINITIONS
# All learning materials are defined here
# ============================================================================

# Course content files
COURSE_CONTENT = {
    'docs/course_with_schedule.md': '''# Python Analytics Engineering Interview Prep Course

## Course Overview

This comprehensive course teaches Python from fundamentals through interview-ready patterns in 21 days.

**Structure:**
- 6 Learning Modules (concepts with examples)
- 60 Progressive Exercises (10 per module)
- 70 Flashcards (aligned with modules)
- 21-Day Study Schedule

**Daily Commitment:** 90-120 minutes

---

# Module 1: Python Data Structures & Operations

## Lists and List Operations

Lists are ordered, mutable collections - the foundation of data manipulation in Python.

```python
# Creating and accessing lists
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# Indexing and slicing
first = numbers[0]         # 1
last = numbers[-1]         # 5
subset = numbers[1:3]      # [2, 3]
reversed = numbers[::-1]   # [5, 4, 3, 2, 1]
```

[Content continues...]
''',

    'docs/talking_points.md': '''# Talking Points - How to Discuss Your Solutions Professionally

## The Meta-Strategy

Remember: They're not just evaluating your code. They're evaluating whether they want to work with you for the next 2+ years.

[Content continues...]
''',

    'docs/quick_reference.md': '''# Quick Reference - Python Analytics Engineering Syntax

Rapid lookup during interviews. No explanations, just syntax.

## Lists

```python
lst = [1, 2, 3]
lst.append(4)                 # Add single item
lst.extend([5, 6])            # Add multiple items
[Content continues...]
```
''',

    # Note: README.md will be in root, not docs/

    'docs/GETTING_STARTED.md': '''# Getting Started - Python Analytics Interview Prep Platform

## Quick Start (5 Minutes)

[Full getting started content...]
''',

    # README goes in root, not docs
    'README.md': '''# Python Analytics Interview Prep Platform

## Quick Start

1. Review the Pattern Matcher for problem recognition
2. Study Group A patterns (critical for interviews)  
3. Practice with exercises.py
4. Drill flashcards daily

## Repository Structure

```
python-analytics-interview-prep/
├── README.md              # This file (in root)
├── src/                   # Python source code
├── docs/                  # Documentation
├── data/                  # Data files
├── docker/                # Docker configuration
├── practice_work/         # Your work (preserved)
├── notes/                 # Your notes (preserved)
└── docker-compose.yml
```

[Content continues...]
''',
}

# Python source files
PYTHON_SOURCE = {
    'src/exercises.py': '''#!/usr/bin/env python3
"""
Python Analytics Interview Prep - Progressive Exercises
60 exercises mapped to course modules with solutions
"""

import pandas as pd
import numpy as np

# Module 1 Exercises: Data Structures
def exercise_1_1():
    """EASY: Create a list of numbers 1-10 and return only even numbers."""
    numbers = list(range(1, 11))
    evens = [x for x in numbers if x % 2 == 0]
    return evens

[Content continues with all 60 exercises...]
''',

    'src/patterns_and_gotchas.py': '''#!/usr/bin/env python3
"""
Patterns and Gotchas - Complete Implementation Reference
Analytics Engineering Interview Patterns
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple

class CorePatterns:
    """The 20 patterns that solve 80% of interview problems."""
    
    @staticmethod
    def top_n_by_group(df: pd.DataFrame, group_col: str, value_col: str, n: int = 5) -> pd.DataFrame:
        """Find top N items by value within each group."""
        return (df
                .sort_values(value_col, ascending=False)
                .groupby(group_col)
                .head(n))

[Content continues with all patterns...]
''',
}

# Documentation files (already embedded above in COURSE_CONTENT, but separating key platform docs)
PLATFORM_DOCS = {
    'docs/RELEASE_NOTES.md': '''# RELEASE NOTES - Python Analytics Interview Prep Platform

## Current Production Version: 3.2.3

[Full release notes content...]
''',

    'docs/PLATFORM_ARCHITECTURE.md': '''# Platform Architecture - Python Analytics Interview Prep

Technical architecture of the interview prep platform.

[Full content from the file we just created]
''',
}

# Docker configuration
DOCKER_CONFIG = {
    'docker/requirements.txt': '''numpy==2.3.3
pandas==2.3.3
python-dateutil==2.9.0.post0
pytz==2025.2
six==1.17.0
tzdata==2025.2
openpyxl==3.1.2
''',

    'docker/Dockerfile': '''FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/New_York

# Install desktop environment and dependencies
RUN apt-get update && apt-get install -y \\
    xfce4 xfce4-terminal xfce4-goodies \\
    tightvncserver novnc websockify \\
    supervisor sudo wget curl git nano \\
    build-essential software-properties-common \\
    && apt-get clean

[Full Dockerfile content...]
''',

    'docker-compose.yml': '''version: '3.8'

services:
  interview-prep:
    build:
      context: .
      dockerfile: docker/Dockerfile
    image: interview-prep:latest
    container_name: python-interview-prep
    ports:
      - "5901:5901"
      - "6901:6901"
    volumes:
      - ./practice_work:/home/student/interview-prep/practice_work
      - ./notes:/home/student/interview-prep/notes
    environment:
      - DISPLAY=:1
      - VNC_PASSWORD=student
    restart: unless-stopped
''',
}

# Binary files (base64 encoded)
BINARY_FILES = {
    'data/flashcards_complete.xlsx': '''[BASE64_ENCODED_EXCEL_CONTENT_HERE]''',
}

# ============================================================================
# RUNTIME MERGE ENGINE
# ============================================================================

class SmartMergeEngine:
    """Intelligent merge engine that makes runtime decisions."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.repo_path = base_path / REPO_NAME
        self.existing_structure = None
        self.user_modifications = set()
        
    def detect_structure(self) -> str:
        """Detect current repository structure."""
        if not self.repo_path.exists():
            return 'none'
        
        # Check for organized structure markers
        if (self.repo_path / 'src').exists() and (self.repo_path / 'docs').exists():
            return 'organized'
        
        # Check for flat structure markers
        if (self.repo_path / 'exercises.py').exists():
            return 'flat'
            
        return 'unknown'
    
    def scan_user_modifications(self):
        """Identify files that user has modified."""
        # For now, preserve all files in protected directories
        protected_dirs = ['practice_work', 'notes', 'mock_interviews']
        for dir_name in protected_dirs:
            dir_path = self.repo_path / dir_name
            if dir_path.exists():
                for file_path in dir_path.rglob('*'):
                    if file_path.is_file():
                        self.user_modifications.add(str(file_path.relative_to(self.repo_path)))
    
    def should_update_file(self, relative_path: str) -> bool:
        """Determine if a file should be updated."""
        # Never update user work
        protected_dirs = ['practice_work', 'notes', 'mock_interviews']
        for protected in protected_dirs:
            if relative_path.startswith(protected):
                return False
        
        # Update everything else
        return True
    
    def create_file_with_subdirs(self, relative_path: str, content: str, binary: bool = False):
        """
        Create a file, ensuring all subdirectories exist.
        
        FIXED: Properly handles nested paths like 'docs/guides/advanced.md'
        """
        full_path = self.repo_path / relative_path
        
        # Ensure parent directories exist
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        if binary:
            # Decode base64 for binary files
            import base64
            decoded_content = base64.b64decode(content)
            full_path.write_bytes(decoded_content)
        else:
            full_path.write_text(content, encoding='utf-8')
    
    def migrate_flat_to_organized(self):
        """Migrate from flat structure to organized structure."""
        print("  → Migrating from flat to organized structure...")
        
        migrations = {
            'exercises.py': 'src/exercises.py',
            'patterns_and_gotchas.py': 'src/patterns_and_gotchas.py',
            'flashcards_complete.xlsx': 'data/flashcards_complete.xlsx',
            'course_with_schedule.md': 'docs/course_with_schedule.md',
            'talking_points.md': 'docs/talking_points.md',
            'quick_reference.md': 'docs/quick_reference.md',
            'README.md': 'docs/README.md',
        }
        
        for old_path, new_path in migrations.items():
            old_file = self.repo_path / old_path
            if old_file.exists():
                new_file = self.repo_path / new_path
                new_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(old_file), str(new_file))
                print(f"    Moved {old_path} → {new_path}")
    
    def clean_obsolete_files(self):
        """Remove files that no longer exist in the platform."""
        obsolete = [
            'ARCHITECTURE.md',  # Old, replaced by PLATFORM_ARCHITECTURE.md
            'consolidator.py',  # Old approach, no longer used
            'docs/ARCHITECTURE.md',  # Might be in docs folder
            'setup_complete.py',  # Old generated file
            'docs/SETUP.md',  # Duplicate - using GETTING_STARTED.md
            'SETUP.md',  # Old location
            'docs/README.md',  # README should be in root
            'PROJECT_STATUS.md',  # Renamed to RELEASE_NOTES.md
            'docs/PROJECT_STATUS.md',  # Old name
            'docs/SETUP_GUIDE.md',  # Replaced by GETTING_STARTED.md
            'SETUP_GUIDE.md',  # Old location
        ]
        
        for file_path in obsolete:
            full_path = self.repo_path / file_path
            if full_path.exists():
                full_path.unlink()
                print(f"  ✓ Removed obsolete file: {file_path}")
    
    def apply_updates(self):
        """Apply all updates based on runtime analysis."""
        
        # Detect current state
        structure = self.detect_structure()
        print(f"\\n📁 Detected structure: {structure}")
        
        if structure == 'none':
            print("\\n🚀 Performing fresh installation...")
            self.fresh_install()
        else:
            print("\\n🔄 Updating existing repository...")
            
            # Scan for user modifications
            self.scan_user_modifications()
            
            # Migrate if needed
            if structure == 'flat':
                self.migrate_flat_to_organized()
            
            # Update files
            self.update_files()
            
            # Clean obsolete
            self.clean_obsolete_files()
        
        # Ensure user directories exist
        self.ensure_user_directories()
        
        # Offer to create git tag for this version
        self.offer_git_tag()
        
        print("\\n✅ Platform setup complete!")
    
    def fresh_install(self):
        """Perform a fresh installation."""
        self.repo_path.mkdir(parents=True, exist_ok=True)
        
        # Create all files
        all_content = {
            **COURSE_CONTENT,
            **PYTHON_SOURCE,
            **PLATFORM_DOCS,
            **DOCKER_CONFIG,
        }
        
        for relative_path, content in all_content.items():
            self.create_file_with_subdirs(relative_path, content)
            print(f"  ✓ Created {relative_path}")
        
        # Create binary files
        for relative_path, content in BINARY_FILES.items():
            self.create_file_with_subdirs(relative_path, content, binary=True)
            print(f"  ✓ Created {relative_path} (binary)")
    
    def update_files(self):
        """Update existing files selectively."""
        all_content = {
            **COURSE_CONTENT,
            **PYTHON_SOURCE,
            **PLATFORM_DOCS,
            **DOCKER_CONFIG,
        }
        
        for relative_path, content in all_content.items():
            if self.should_update_file(relative_path):
                self.create_file_with_subdirs(relative_path, content)
                print(f"  ✓ Updated {relative_path}")
        
        # Update binary files
        for relative_path, content in BINARY_FILES.items():
            if self.should_update_file(relative_path):
                self.create_file_with_subdirs(relative_path, content, binary=True)
                print(f"  ✓ Updated {relative_path} (binary)")
    
    def ensure_user_directories(self):
        """Ensure user work directories exist."""
        user_dirs = [
            'practice_work',
            'notes',
            'mock_interviews',
        ]
        
        for dir_name in user_dirs:
            dir_path = self.repo_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                # Add .gitkeep
                (dir_path / '.gitkeep').write_text('')
                print(f"  ✓ Created user directory: {dir_name}/")
    
    def offer_git_tag(self):
        """Offer to create git tag for this version."""
        # Check if we're in a git repo
        if not (self.repo_path / '.git').exists():
            return
        
        print("\n📌 Git Tagging")
        
        # Check for uncommitted changes
        os.chdir(self.repo_path)
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("  ℹ Uncommitted changes detected")
            response = input(f"  Create commit for v{VERSION}? (y/n): ").strip().lower()
            
            if response == 'y':
                # Stage all changes
                subprocess.run(['git', 'add', '.'], check=True)
                
                # Create commit
                commit_msg = f"Release v{VERSION} - Automated setup"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                print(f"  ✓ Created commit for v{VERSION}")
        
        # Check if tag exists
        result = subprocess.run(['git', 'tag', '-l', f'v{VERSION}'],
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print(f"  ℹ Tag v{VERSION} already exists")
        else:
            response = input(f"  Create tag v{VERSION}? (y/n): ").strip().lower()
            
            if response == 'y':
                # Create annotated tag
                tag_msg = f"Production Release {VERSION}"
                subprocess.run(['git', 'tag', '-a', f'v{VERSION}', '-m', tag_msg], 
                             check=True)
                print(f"  ✓ Created tag v{VERSION}")
                
                # Offer to push
                response = input("  Push tag to origin? (y/n): ").strip().lower()
                if response == 'y':
                    try:
                        subprocess.run(['git', 'push', 'origin', f'v{VERSION}'], 
                                     check=True)
                        print(f"  ✓ Pushed tag v{VERSION} to origin")
                    except:
                        print("  ⚠ Could not push tag (check remote configuration)")

# ============================================================================
# DOCKER BUILDER
# ============================================================================

class DockerBuilder:
    """Handles Docker image building."""
    
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        
    def find_wing_deb(self) -> Path:
        """Search for Wing Pro .deb file."""
        search_locations = [
            Path.home() / 'Downloads',
            Path.cwd(),
            Path(__file__).parent,
        ]
        
        for location in search_locations:
            if location.exists():
                for file in location.glob('wing-pro*.deb'):
                    return file
        
        return None
    
    def build_image(self):
        """Build Docker image."""
        print("\\n🐳 Building Docker image...")
        
        # Check if Wing .deb exists
        wing_deb = self.find_wing_deb()
        if wing_deb:
            # Copy to docker directory
            docker_wing = self.repo_path / 'docker' / wing_deb.name
            shutil.copy2(wing_deb, docker_wing)
            print(f"  ✓ Found Wing Pro: {wing_deb.name}")
        else:
            print("  ⚠ Wing Pro not found, will use JupyterLab instead")
        
        # Build image
        os.chdir(self.repo_path)
        result = os.system('docker compose build')
        
        if result == 0:
            print("\\n✅ Docker image built successfully!")
            print("\\nTo start the container:")
            print("  docker compose up")
            print("\\nThen access at: http://localhost:6901")
            print("  Password: student")
        else:
            print("\\n⚠ Docker build failed. Check Docker is running.")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point for setup script."""
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Setup Python Analytics Interview Prep Platform')
    parser.add_argument('--mode', 
                       choices=['local', 'docker', 'all'],
                       default='local',
                       help='Setup mode: local (default), docker, or all')
    
    args = parser.parse_args()
    
    # Display header
    print("=" * 60)
    print(f"Python Analytics Interview Prep Platform Setup v{VERSION}")
    print("=" * 60)
    
    # Determine base path
    base_path = Path.cwd()
    repo_path = base_path / REPO_NAME
    
    # Initialize merge engine
    merger = SmartMergeEngine(base_path)
    
    # Apply updates based on mode
    if args.mode in ['local', 'all']:
        merger.apply_updates()
    
    # Build Docker if requested
    if args.mode in ['docker', 'all']:
        if not repo_path.exists():
            print("\\n⚠ Repository must exist before building Docker image.")
            print("  Run with --mode local first.")
            sys.exit(1)
        
        builder = DockerBuilder(repo_path)
        builder.build_image()
    
    # Final instructions
    if args.mode == 'local':
        print(f"\\n📂 Repository ready at: {repo_path}")
        print("\\nNext steps:")
        print("  1. cd python-analytics-interview-prep")
        print("  2. pip install -r requirements.txt")
        print("  3. Start with docs/README.md")
    
    print("\\n" + "=" * 60)
    print("🎯 Ready for interview prep!")
    print("=" * 60)

if __name__ == "__main__":
    main()
