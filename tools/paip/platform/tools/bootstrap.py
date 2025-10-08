#!/usr/bin/env python3
"""
Bootstrap Script - Automated Environment Setup v1.0.1-RC14
Handles all the manual steps automatically

This script:
1. Sets up PowerShell/Bash profile
2. Configures environment variables (including PAIP_HOME)
3. Creates virtual environment at user level (~/.venvs/paip)
4. Installs requirements
5. Generates Wing IDE configuration with PYTHONPATH
"""

import os
import sys
import platform
import subprocess
import json
import urllib.request
import tempfile
from pathlib import Path

class EnvironmentBootstrapper:
    """Automates all environment setup steps."""
    
    def __init__(self, interactive=False):
        self.system = platform.system()
        self.home = Path.home()
        self.patterns_repo = None
        self.github_home = None
        self.repo_path = Path.cwd()  # Assume running from repo root
        self.venv_path = self.home / ".venvs" / "paip"
        self.interactive = interactive
        
    def detect_github_home(self):
        """Find or set the GitHub master folder."""
        # Common locations to check
        search_paths = [
            self.home / "GitHub",
            self.home / "Documents" / "GitHub",
            self.home / "Projects" / "GitHub",
            self.home / "Dropbox" / "Projects" / "GitHub",
            Path("C:/Users") / os.environ.get('USERNAME', '') / "GitHub",
            Path("C:/Users") / os.environ.get('USERNAME', '') / "Dropbox" / "Projects" / "GitHub",
        ]
        
        # Check existing environment variable
        if os.environ.get('GITHUB_HOME'):
            self.github_home = Path(os.environ['GITHUB_HOME'])
            print(f"Using GITHUB_HOME from environment: {self.github_home}")
            return True
        
        # Auto-detect
        for path in search_paths:
            if path.exists():
                self.github_home = path
                print(f"Found GitHub folder: {path}")
                return True
        
        # Ask user
        print("Could not auto-detect GitHub master folder.")
        user_path = input("Enter path to your GitHub folder (e.g., C:\\Users\\[name]\\GitHub): ").strip()
        if user_path and Path(user_path).exists():
            self.github_home = Path(user_path)
            return True
        
        return False
    
    def detect_patterns_repo(self):
        """Find the data-engineering-patterns repo."""
        if not self.github_home:
            return False
            
        # First check in GitHub home
        patterns_path = self.github_home / "data-engineering-patterns"
        if patterns_path.exists() and (patterns_path / "tools").exists():
            self.patterns_repo = patterns_path
            print(f"Found patterns repo: {patterns_path}")
            return True
        
        # Fallback to other locations
        search_paths = [
            self.home / "GitHub" / "data-engineering-patterns",
            self.home / "Documents" / "GitHub" / "data-engineering-patterns",
            self.home / "Dropbox" / "Projects" / "GitHub" / "data-engineering-patterns",
        ]
        
        for path in search_paths:
            if path.exists() and (path / "tools").exists():
                self.patterns_repo = path
                print(f"Found patterns repo: {path}")
                return True
        
        # Ask user
        print("Could not find data-engineering-patterns repo.")
        user_path = input("Enter full path to data-engineering-patterns (or press Enter to skip): ").strip()
        if user_path and Path(user_path).exists():
            self.patterns_repo = Path(user_path)
            return True
        
        return False
    
    def get_powershell_profile_path(self):
        """Query PowerShell for actual $PROFILE path to handle OneDrive."""
        try:
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "echo $PROFILE"],
                capture_output=True,
                text=True,
                check=True
            )
            profile_path = Path(result.stdout.strip())
            print(f"PowerShell profile path: {profile_path}")
            return profile_path
        except Exception as e:
            print(f"Could not query PowerShell profile path: {e}")
            # Fallback to standard location
            return self.home / "Documents" / "WindowsPowerShell" / "Microsoft.PowerShell_profile.ps1"
    
    def setup_powershell_profile(self):
        """Configure PowerShell profile on Windows."""
        if self.system != 'Windows':
            return
        
        print("\nConfiguring PowerShell profile...")
        
        # Get actual profile path (handles OneDrive)
        ps_profile = self.get_powershell_profile_path()
        
        # Create directory if needed
        ps_profile.parent.mkdir(parents=True, exist_ok=True)
        
        # Profile content
        profile_content = ps_profile.read_text() if ps_profile.exists() else ""
        
        # Always remove old PAIP entries and regenerate with current version
        # This ensures new environment variables (like PYTHONPATH) get added
        lines = profile_content.splitlines()
        
        # Remove all PAIP-related lines
        lines = [line for line in lines if not any([
            '$env:PATTERNS_REPO' in line,
            '$env:PATTERNS_TOOLS' in line,
            '$env:GITHUB_HOME' in line,
            '$env:PAIP_HOME' in line,
            '$env:PYTHONPATH' in line,
            '$env:PYSPARK_PYTHON' in line,
            'PATTERNS_REPO\\tools' in line,
            'Python Interview Prep Environment' in line,
            'function Open-Wing' in line,
            'Wing Pro 11\\bin\\wing.exe' in line,
            'python-analytics-interview-prep.wpr' in line,
            'Set-Location $env:PAIP_HOME' in line,
            'Wing IDE launcher function' in line
        ])]
        
        # Remove orphaned braces (from incomplete function cleanup)
        lines = [line for line in lines if line.strip() not in ['{', '}']]
        
        # Add our environment variables (current version)
        venv_python = self.venv_path / "Scripts" / "python.exe"
        lines.extend([
            '',
            '# Python Interview Prep Environment (auto-generated)',
            f'$env:GITHUB_HOME = "{self.github_home}"',
            f'$env:PAIP_HOME = "{self.repo_path}"',
            f'$env:PYTHONPATH = "{self.repo_path}\\platform\\content"',
            f'$env:PYSPARK_PYTHON = "{venv_python}"',
            f'$env:PATTERNS_REPO = "{self.patterns_repo}"',
            f'$env:PATTERNS_TOOLS = "{self.patterns_repo}\\tools"',
            '$env:PATH = "$env:PATTERNS_TOOLS;$env:PATH"',
            '',
            '# Wing IDE launcher function',
            'function Open-Wing {',
            '    Set-Location $env:PAIP_HOME',
            '    & "C:\\Program Files\\Wing Pro 11\\bin\\wing.exe" python-analytics-interview-prep.wpr',
            '}',
            ''
        ])
        
        ps_profile.write_text('\n'.join(lines))
        print(f"  Updated PowerShell profile: {ps_profile}")
        
        ps_profile.write_text('\n'.join(lines))
        print(f"  Updated PowerShell profile: {ps_profile}")
        
        # Set execution policy (idempotent - won't fail if already set)
        try:
            subprocess.run([
                "powershell", "-Command",
                "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"
            ], check=True, capture_output=True)
            print("  PowerShell execution policy configured")
        except:
            pass  # Already set or no permissions
    
    def setup_bash_profile(self):
        """Configure bash profile on Mac/Linux."""
        if self.system == 'Windows':
            return
        
        print("\nConfiguring shell profile...")
        
        # Determine which shell config to use
        shell = os.environ.get('SHELL', '/bin/bash')
        if 'zsh' in shell:
            profile_file = self.home / ".zshrc"
        else:
            profile_file = self.home / ".bashrc"
        
        # Profile content
        profile_content = profile_file.read_text() if profile_file.exists() else ""
        
        # Always remove old PAIP entries and regenerate with current version
        lines = profile_content.splitlines()
        
        # Remove all PAIP-related lines
        lines = [line for line in lines if not any([
            'PATTERNS_REPO' in line,
            'PATTERNS_TOOLS' in line,
            'GITHUB_HOME' in line,
            'PAIP_HOME' in line,
            'PYTHONPATH' in line and 'platform/content' in line,
            'PYSPARK_PYTHON' in line,
            'Python Interview Prep Environment' in line
        ])]
        
        # Add our environment variables (current version)
        venv_python = self.venv_path / "bin" / "python"
        lines.extend([
            '',
            '# Python Interview Prep Environment (auto-generated)',
            f'export GITHUB_HOME="{self.github_home}"',
            f'export PAIP_HOME="{self.repo_path}"',
            f'export PYTHONPATH="{self.repo_path}/platform/content"',
            f'export PYSPARK_PYTHON="{venv_python}"',
            f'export PATTERNS_REPO="{self.patterns_repo}"',
            f'export PATTERNS_TOOLS="{self.patterns_repo}/tools"',
            'export PATH="$PATTERNS_TOOLS:$PATH"',
            ''
        ])
        
        profile_file.write_text('\n'.join(lines))
        print(f"  Updated shell profile: {profile_file}")
        
        profile_file.write_text('\n'.join(lines))
        print(f"  Updated shell profile: {profile_file}")
    
    def setup_virtual_environment(self):
        """Create and configure Python virtual environment at user level."""
        print("\nSetting up Python virtual environment...")
        
        if not self.repo_path.exists():
            print("  Repository doesn't exist yet. Run installer first.")
            return False
        
        # Create .venvs directory if it doesn't exist
        venvs_dir = self.home / ".venvs"
        venvs_dir.mkdir(parents=True, exist_ok=True)
        
        if self.venv_path.exists():
            print(f"  Virtual environment already exists: {self.venv_path}")
        else:
            # Create venv at user level
            print(f"  Creating virtual environment at: {self.venv_path}")
            subprocess.run([sys.executable, "-m", "venv", str(self.venv_path)], check=True)
            print(f"  Created virtual environment: {self.venv_path}")
        
        # Determine pip path
        if self.system == 'Windows':
            pip_path = self.venv_path / "Scripts" / "pip.exe"
            python_path = self.venv_path / "Scripts" / "python.exe"
        else:
            pip_path = self.venv_path / "bin" / "pip"
            python_path = self.venv_path / "bin" / "python"
        
        # Install requirements (check if needed first)
        requirements_file = self.repo_path / "requirements.txt"
        if requirements_file.exists():
            # Check if requirements are already satisfied
            print("  Checking requirements...")
            check_result = subprocess.run(
                [str(pip_path), "show", "pandas", "numpy"], 
                capture_output=True, text=True
            )
            
            if check_result.returncode != 0:
                print("  Installing requirements...")
                subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], check=True)
                print("  Requirements installed")
            else:
                # Verify all requirements are met
                verify_result = subprocess.run(
                    [str(pip_path), "install", "--dry-run", "-r", str(requirements_file)],
                    capture_output=True, text=True
                )
                
                if "Would install" in verify_result.stdout:
                    print("  Updating requirements...")
                    subprocess.run([str(pip_path), "install", "-r", str(requirements_file)], check=True)
                    print("  Requirements updated")
                else:
                    print("  Requirements already satisfied")
        
        # Create activation helper
        if self.system == 'Windows':
            activate_cmd = f"{self.venv_path}\\Scripts\\activate"
        else:
            activate_cmd = f"source {self.venv_path}/bin/activate"
        
        helper_script = self.repo_path / "activate_env.txt"
        helper_script.write_text(f"""
To activate the virtual environment, run:
  {activate_cmd}

Then you can run:
  python platform/content/src/exercises.py

Virtual environment location: {self.venv_path}
""")
        
        print(f"\n  To activate virtual environment:")
        print(f"     {activate_cmd}")
        
        return True
    
    def setup_wing_ide(self):
        """Generate Wing IDE project and user configuration files."""
        print("\nConfiguring Wing IDE...")
        
        if not self.repo_path.exists():
            print("  Repository path not set")
            return False
        
        # Check if Wing IDE is installed
        wing_installed = self._check_wing_installed()
        
        if not wing_installed:
            print("  Wing Pro not detected")
            print("  Download from: https://wingware.com/downloads/wing-pro")
            response = input("  Continue with configuration anyway? (y/n): ").strip().lower()
            if response != 'y':
                return False
        
        # Generate .wpr (project file)
        wpr_path = self.repo_path / "python-analytics-interview-prep.wpr"
        self._generate_wpr_file(wpr_path)
        print(f"  Generated Wing project file: {wpr_path.name}")
        
        # Generate .wpu (user preferences file) - only on first install
        wpu_path = self.repo_path / "python-analytics-interview-prep.wpu"
        if not wpu_path.exists():
            self._generate_wpu_file(wpu_path)
            print(f"  Generated Wing user preferences: {wpu_path.name}")
        else:
            print(f"  Preserving existing Wing user preferences: {wpu_path.name}")
        
        print(f"\n  To use Wing IDE:")
        print(f"     1. Open Wing Pro")
        print(f"     2. File -> Open Project -> {wpr_path}")
        print(f"     3. Start coding in study/ directory")
        
        return True
    
    def _check_wing_installed(self):
        """Check if Wing IDE is installed."""
        if self.system == 'Windows':
            # Check common Windows installation paths
            wing_paths = [
                Path("C:/Program Files/Wing Pro 11"),
                Path("C:/Program Files/Wing Pro 10"),
                Path("C:/Program Files/Wing Pro 9"),
            ]
            for path in wing_paths:
                if path.exists():
                    return True
        else:
            # Check if wing executable is in PATH
            try:
                subprocess.run(["which", "wing"], capture_output=True, check=True)
                return True
            except:
                pass
        
        return False
    
    def _generate_wpr_file(self, wpr_path):
        """Generate Wing project file with PYTHONPATH for platform/content."""
        # Convert paths to forward slashes for Wing
        repo_path_str = str(self.repo_path.absolute()).replace('\\', '/')
        content_path = f"{repo_path_str}/platform/content"
        study_path = f"{repo_path_str}/study"
        
        # Build WPR content with proper escaping
        wpr_content = "#!wing\n"
        wpr_content += "#!version=11.0\n"
        wpr_content += "##################################################################\n"
        wpr_content += "# Wing project file                                              #\n"
        wpr_content += "##################################################################\n"
        wpr_content += "[project attributes]\n"
        wpr_content += "proj.directory-list = [{'dirloc': loc('.'),\n"
        wpr_content += "                        'excludes': ('venv',\n"
        wpr_content += "                                     '__pycache__',\n"
        wpr_content += "                                     '.git',\n"
        wpr_content += "                                     '.pytest_cache',\n"
        wpr_content += "                                     '.venvs',\n"
        wpr_content += "                                     '*.pyc'),\n"
        wpr_content += "                        'filter': '*',\n"
        wpr_content += "                        'include_hidden': False,\n"
        wpr_content += "                        'recursive': True,\n"
        wpr_content += "                        'watch_for_changes': True}]\n"
        wpr_content += "proj.file-type = 'shared'\n"
        wpr_content += f"proj.pypath = {{None: ('{content_path}',)}}\n"
        wpr_content += f"debug.project-home = '{study_path}'\n"
        
        wpr_path.write_text(wpr_content)
    
    def _generate_wpu_file(self, wpu_path):
        """Generate Wing user preferences with Python interpreter path.
        
        Note: PYTHONPATH is set in PowerShell profile, Wing inherits it from shell.
        We don't use proj.env-vars because it causes Wing internal command errors.
        """
        # Delete old .wpu file if it exists to avoid corruption
        if wpu_path.exists():
            wpu_path.unlink()
            print(f"  Removed old {wpu_path.name}")
        
        # Determine Python executable path in venv
        if self.system == 'Windows':
            python_exe = self.venv_path / "Scripts" / "python.exe"
        else:
            python_exe = self.venv_path / "bin" / "python"
        
        # Convert to absolute path and use forward slashes for Wing
        python_exe_str = str(python_exe.absolute()).replace('\\', '/')
        
        wpu_content = f"""#!wing
#!version=11.0
##################################################################
# Wing project file : User-specific branch                       #
##################################################################
[user attributes]
proj.pyexec = {{None: ('custom',
                      '{python_exe_str}')}}
guimgr.overall-gui-state = {{'dock-state': ['(0, 0, 800, 600)'],
                             'window-state': 'normal'}}
"""
        wpu_path.write_text(wpu_content)
    
    def setup_git_config(self):
        """Configure git settings for the repo."""
        if not self.repo_path.exists():
            return
        
        print("\nConfiguring Git...")
        
        os.chdir(self.repo_path)
        
        # Check if it's a git repo
        if not (self.repo_path / ".git").exists():
            response = input("  Initialize git repository? (y/n): ").strip().lower()
            if response == 'y':
                subprocess.run(["git", "init"], check=True)
                print("  Initialized git repository")
        else:
            print("  Git repository already initialized")
        
        # Set up .gitignore (idempotent - always overwrites with correct content)
        gitignore = self.repo_path / ".gitignore"
        gitignore_content = """# Python
__pycache__/
*.pyc
.pytest_cache/

# Virtual Environment
venv/
env/
.env

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store

# Wing IDE user preferences (not project settings)
*.wpu
*.wpr~
.wingide/

# Jupyter
.ipynb_checkpoints/
*.ipynb
"""
        
        # Only write if different
        if not gitignore.exists() or gitignore.read_text() != gitignore_content:
            gitignore.write_text(gitignore_content)
            print("  Updated .gitignore")
        else:
            print("  .gitignore already configured")
    
    
    def _create_wing_desktop_shortcut(self):
        """Create desktop shortcut for Wing IDE on Windows."""
        # Prompt in interactive mode
        if self.interactive:
            response = input("  Create Wing IDE desktop shortcut? (y/n): ").strip().lower()
            if response != 'y':
                print("  Skipped desktop shortcut creation")
                print("  Use 'Open-Wing' command in PowerShell instead")
                return
        
        # Get actual Desktop path (handles OneDrive)
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", "[Environment]::GetFolderPath('Desktop')"],
            capture_output=True,
            text=True,
            check=True
        )
        desktop = Path(result.stdout.strip())
        shortcut_path = desktop / "PAIP - Wing IDE.lnk"
        
        # PowerShell script to create shortcut
        wpr_path = str((self.repo_path / "python-analytics-interview-prep.wpr").absolute())
        
        ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-Command `"& 'C:\\Program Files\\Wing Pro 11\\bin\\wing.exe' '{wpr_path}'`""
$Shortcut.WorkingDirectory = "{self.repo_path}"
$Shortcut.IconLocation = "C:\\Program Files\\Wing Pro 11\\bin\\wing.exe,0"
$Shortcut.Description = "Python Analytics Interview Prep - Wing IDE"
$Shortcut.Save()
"""
        
        try:
            result = subprocess.run(
                ["powershell", "-Command", ps_script],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  Created desktop shortcut: {shortcut_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"  Warning: Could not create desktop shortcut")
            print(f"    Use 'Open-Wing' command in PowerShell instead")
    
    def create_shortcuts(self):
        """Create helpful shortcuts/aliases."""
        print("\nCreating shortcuts...")
        
        # Create desktop shortcut on Windows
        if self.system == 'Windows':
            self._create_wing_desktop_shortcut()
        
        # Create run script
        run_script = self.repo_path / "run.py"
        run_content = """#!/usr/bin/env python3
\"\"\"Quick launcher for common tasks.\"\"\"

import sys
import os

print("Python Analytics Interview Prep - Quick Launch")
print("=" * 50)
print("1. Run exercises")
print("2. Test patterns")
print("3. Open documentation")
print("4. Start Docker environment")

choice = input("\\nSelect option (1-4): ").strip()

if choice == '1':
    os.system(f"{sys.executable} platform/content/src/exercises.py")
elif choice == '2':
    os.system(f"{sys.executable} platform/content/src/patterns_and_gotchas.py")
elif choice == '3':
    os.system("start platform/content/docs/README.md" if os.name == 'nt' else "open platform/content/docs/README.md")
elif choice == '4':
    os.system("docker compose up")
else:
    print("Invalid choice")
"""
        
        # Only write if different or doesn't exist
        if not run_script.exists() or run_script.read_text() != run_content:
            run_script.write_text(run_content)
            run_script.chmod(0o755)
            print(f"  Created/updated run.py launcher")
        else:
            print(f"  run.py launcher already exists")
    
    def check_java(self):
        """Check if Java is installed and accessible."""
        # Check JAVA_HOME
        java_home = os.environ.get('JAVA_HOME')
        if java_home:
            java_exe = Path(java_home) / 'bin' / 'java.exe' if self.system == 'Windows' else Path(java_home) / 'bin' / 'java'
            if java_exe.exists():
                print(f"Java found via JAVA_HOME: {java_home}")
                return True
        
        # Check PATH
        try:
            result = subprocess.run(['java', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Java found in PATH")
                return True
        except FileNotFoundError:
            pass
        
        return False
    
    def install_java(self):
        """Download and install OpenJDK silently (Windows only)."""
        if self.system != 'Windows':
            print("Automatic Java installation only supported on Windows.")
            print("Please install Java manually from: https://adoptium.net/")
            return False
        
        print("\nJava not found. Installing OpenJDK...")
        
        # Adoptium Temurin JRE 11 (LTS) - Windows x64 MSI
        jdk_url = "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21%2B9/OpenJDK11U-jre_x64_windows_hotspot_11.0.21_9.msi"
        
        try:
            # Download to temp directory
            with tempfile.NamedTemporaryFile(delete=False, suffix='.msi') as tmp_file:
                print(f"  Downloading OpenJDK 11...")
                urllib.request.urlretrieve(jdk_url, tmp_file.name)
                msi_path = tmp_file.name
            
            print(f"  Installing (this may take a minute)...")
            # Silent install with ADDLOCAL to set environment variables
            result = subprocess.run([
                'msiexec', '/i', msi_path,
                '/qn',  # Quiet mode, no user interaction
                'ADDLOCAL=FeatureMain,FeatureEnvironment,FeatureJarFileRunWith,FeatureJavaHome',
                '/norestart'
            ], capture_output=True, text=True)
            
            # Clean up installer
            try:
                os.unlink(msi_path)
            except:
                pass
            
            if result.returncode == 0:
                print("  Java installed successfully")
                return True
            else:
                print(f"  Installation failed with code {result.returncode}")
                print(f"  {result.stderr}")
                return False
                
        except Exception as e:
            print(f"  Error installing Java: {e}")
            print("  Please install manually from: https://adoptium.net/")
            return False
    
    def setup_java_environment(self):
        """Set JAVA_HOME if needed after installation."""
        if self.system != 'Windows':
            return
        
        # Check if JAVA_HOME already set
        if os.environ.get('JAVA_HOME'):
            return
        
        # Find Java installation
        program_files = Path(os.environ.get('ProgramFiles', 'C:\\Program Files'))
        java_dirs = [
            program_files / 'Eclipse Adoptium',
            program_files / 'Java',
            program_files / 'OpenJDK',
        ]
        
        java_home = None
        for base_dir in java_dirs:
            if base_dir.exists():
                # Find JRE or JDK subdirectory
                for subdir in base_dir.iterdir():
                    if subdir.is_dir() and ('jre' in subdir.name.lower() or 'jdk' in subdir.name.lower()):
                        java_exe = subdir / 'bin' / 'java.exe'
                        if java_exe.exists():
                            java_home = subdir
                            break
            if java_home:
                break
        
        if not java_home:
            print("  Warning: Could not auto-detect JAVA_HOME")
            return
        
        # Set system environment variable
        print(f"  Setting JAVA_HOME: {java_home}")
        try:
            subprocess.run([
                'powershell', '-Command',
                f'[Environment]::SetEnvironmentVariable("JAVA_HOME", "{java_home}", "User")'
            ], check=True)
            
            # Also add to current session
            os.environ['JAVA_HOME'] = str(java_home)
            
            # Add to PATH
            java_bin = java_home / 'bin'
            subprocess.run([
                'powershell', '-Command',
                f'$path = [Environment]::GetEnvironmentVariable("PATH", "User"); ' +
                f'if ($path -notlike "*{java_bin}*") {{ ' +
                f'[Environment]::SetEnvironmentVariable("PATH", "$path;{java_bin}", "User") }}'
            ], check=True)
            
            print("  JAVA_HOME configured")
        except Exception as e:
            print(f"  Warning: Could not set JAVA_HOME: {e}")
    
    def setup_java(self):
        """Check for Java and install if needed (required for PySpark)."""
        print("\nChecking Java (required for PySpark)...")
        
        if self.check_java():
            return True
        
        # Java not found, attempt installation
        if self.install_java():
            self.setup_java_environment()
            # Verify installation
            if self.check_java():
                return True
        
        print("\nWarning: Java not available. PySpark will not work.")
        print("Install Java manually from: https://adoptium.net/")
        return False
    
    def run_full_setup(self):
        """Run complete bootstrap process."""
        print("=" * 60)
        print("Python Interview Prep - Environment Bootstrapper v1.0.5-RC4")
        print("=" * 60)
        
        # Detect GitHub home folder
        if not self.detect_github_home():
            print("Could not determine GitHub folder. Please set manually.")
            return False
        
        # Detect patterns repo
        if self.patterns_repo or self.detect_patterns_repo():
            # Configure shell profile
            if self.system == 'Windows':
                self.setup_powershell_profile()
            else:
                self.setup_bash_profile()
        
        # Setup Python environment
        self.setup_virtual_environment()
        
        # Setup Java (required for PySpark)
        self.setup_java()
        
        # Git configuration
        self.setup_git_config()
        
        # Wing IDE setup
        self.setup_wing_ide()
        
        # Create shortcuts
        self.create_shortcuts()
        
        print("\n" + "=" * 60)
        print("Bootstrap complete!")
        print("=" * 60)
        print("\nEnvironment variables set:")
        print(f"  GITHUB_HOME = {self.github_home}")
        print(f"  PAIP_HOME = {self.repo_path}")
        print(f"  PATTERNS_REPO = {self.patterns_repo}")
        print(f"  PATTERNS_TOOLS = {self.patterns_repo}/tools")
        print("\nNext steps:")
        print("1. Restart your terminal (to load profile changes)")
        print("2. Navigate to: $PAIP_HOME")
        print("3. Activate virtual environment")
        print("4. Open Wing IDE and start coding in study/")
        
        return True

def main():
    """Main entry point."""
    # Check for interactive flag
    interactive = '--interactive' in sys.argv
    bootstrapper = EnvironmentBootstrapper(interactive=interactive)
    bootstrapper.run_full_setup()

if __name__ == "__main__":
    main()
