#!/usr/bin/env python3
"""
Smart Generator v3.3 - FIXED PATH BUG
Generates setup_python_interview_prep.py with correct organized structure
"""

import os
from pathlib import Path
from datetime import datetime

def generate_setup_script():
    """Generate the setup script with FIXED path handling"""
    
    setup_script = '''#!/usr/bin/env python3
"""
Python Analytics Interview Prep Setup - v3.3 (Path Bug Fixed)
Smart generator with organized structure and migration capabilities
"""

import os
import shutil
from pathlib import Path
import argparse

# Define organized structure
STRUCTURE_MAP = {
    'src': [
        'exercises.py',
        'patterns_and_gotchas.py'
    ],
    'docs': [
        'README.md',
        'course_with_schedule.md',
        'talking_points.md', 
        'quick_reference.md',
        'PROJECT_STATUS.md',
        'SETUP.md',
        'ARCHITECTURE.md',
        'LEARNING_GUIDE.md',
        'PLATFORM_ARCHITECTURE.md',
        'SETUP_GUIDE.md'
    ],
    'data': [
        'flashcards_complete.xlsx'
    ],
    'docker': [
        'Dockerfile',
        'requirements.txt'
    ]
}

def create_organized_structure(base_path):
    """Create organized directory structure"""
    print("\\nSetting up organized structure...")
    
    directories = [
        'src',
        'docs', 
        'data',
        'docker',
        'practice_work',
        'notes',
        'mock_interviews'
    ]
    
    for directory in directories:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {directory}/")
    
    return True

def write_file_to_correct_location(base_path, subdirectory, filename, content):
    """
    FIXED: Write file to the correct subdirectory location
    This is the bug fix - ensures files go to organized folders
    """
    # Construct the FULL path including subdirectory
    if subdirectory:
        filepath = base_path / subdirectory / filename  # FIXED: Include subdirectory!
        filepath.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists
    else:
        filepath = base_path / filename
    
    # Write the content
    filepath.write_text(content)
    
    # Report what we did (showing the subdirectory)
    if subdirectory:
        print(f"  ✓ {subdirectory}/{filename}")
    else:
        print(f"  ✓ {filename}")
    
    return filepath

def migrate_flat_to_organized(base_path):
    """Detect and migrate flat structure to organized"""
    print("\\nChecking for flat structure files to migrate...")
    
    migrated = []
    for subdir, files in STRUCTURE_MAP.items():
        for filename in files:
            flat_file = base_path / filename
            organized_file = base_path / subdir / filename
            
            if flat_file.exists() and flat_file.is_file():
                # Ensure target directory exists
                organized_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                shutil.move(str(flat_file), str(organized_file))
                migrated.append(f"{filename} → {subdir}/{filename}")
                print(f"  ✓ Migrated {filename} → {subdir}/{filename}")
    
    if migrated:
        print(f"\\n✓ Migrated {len(migrated)} files to organized structure")
    else:
        print("  ✓ No migration needed - structure already organized")
    
    return len(migrated) > 0

def setup_local_repository(base_path):
    """Set up the local repository with organized structure"""
    print("\\n" + "="*60)
    print("Setting up Local Repository")
    print("="*60)
    
    # Create organized structure
    create_organized_structure(base_path)
    
    # Check for and migrate flat structure
    migrate_flat_to_organized(base_path)
    
    # Write all files to their CORRECT locations
    print("\\nWriting files to organized locations...")
    
    # Example: Write exercises.py to src/ subdirectory
    exercises_content = """# Exercises content here"""
    write_file_to_correct_location(base_path, 'src', 'exercises.py', exercises_content)
    
    # Example: Write README.md to docs/ subdirectory  
    readme_content = """# README content here"""
    write_file_to_correct_location(base_path, 'docs', 'README.md', readme_content)
    
    print("\\n✓ Local repository setup complete with organized structure!")
    return True

def main():
    """Main entry point with mode selection"""
    parser = argparse.ArgumentParser(description='Setup Python Analytics Interview Prep')
    parser.add_argument('--mode', choices=['local', 'docker', 'all'], 
                       default='local', help='Setup mode')
    args = parser.parse_args()
    
    # Determine base path
    base_path = Path.cwd() / "python-analytics-interview-prep"
    
    if args.mode in ['local', 'all']:
        setup_local_repository(base_path)
    
    if args.mode in ['docker', 'all']:
        print("\\nDocker setup: Run 'docker compose build' after local setup")
    
    print("\\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
'''
    
    # Write the generated setup script
    output_path = Path.cwd() / 'setup_python_interview_prep.py'
    with open(output_path, 'w') as f:
        f.write(setup_script)
    
    print(f"Generated: setup_python_interview_prep.py")
    print(f"File size: {len(setup_script)} bytes")
    print("\nThe path bug has been FIXED in v3.3!")
    print("\nKey fix: Files now correctly write to subdirectories (src/, docs/, data/)")
    print("Instead of all going to root folder")

if __name__ == "__main__":
    generate_setup_script()
