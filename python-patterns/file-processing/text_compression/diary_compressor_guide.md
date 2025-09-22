# Diary Compression System - User Guide

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Installation & Setup](#installation--setup)
4. [Usage Options](#usage-options)
5. [Parameters Reference](#parameters-reference)
6. [How It Works](#how-it-works)
7. [Understanding Your Results](#understanding-your-results)
8. [Tips & Best Practices](#tips--best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Cross-Platform Compatibility](#cross-platform-compatibility)

## Cross-Platform Compatibility

### Supported Platforms
✅ **Windows** (7, 10, 11)  
✅ **Linux** (Ubuntu, Debian, Fedora, etc.)  
✅ **macOS** (10.10+)  

### Key Differences by Platform

| Feature | Windows | Linux/macOS |
|---------|---------|-------------|
| Python command | `python` or `py` | `python3` or `python` |
| Path separator | `\` or `/` (both work) | `/` |
| Case sensitivity | No | Yes |
| Line endings | CRLF | LF |
| Special chars display | Windows Terminal recommended | Native support |

### Platform-Specific Commands Quick Reference

| Task | Windows | Linux/macOS |
|------|---------|-------------|
| Run analysis | `python diary_compressor.py analyze` | `python3 diary_compressor.py analyze` |
| Check Python | `python --version` | `python3 --version` |
| List files | `dir diary` | `ls -la diary/` |
| View file | `type parameters.json` | `cat parameters.json` |
| Set UTF-8 | `chcp 65001` | (not needed) |
| Make executable | (not needed) | `chmod +x diary_compressor.py` |

### Ensuring Compatibility

The system uses these cross-platform practices:
- **Path handling**: `os.path.join()` for all path operations
- **Encoding**: UTF-8 specified for all file operations
- **Line endings**: Handles both CRLF (Windows) and LF (Unix) automatically
- **No external dependencies**: Pure Python standard library
- **No shell commands**: All operations use Python's built-in functions

---

## Overview

The Diary Compression System is a specialized tool designed to compress curated diary chapters (chat conversations) by 75-85%. It learns from your existing chapters to create custom compression rules optimized for your specific writing style and conversation patterns.

### Key Benefits
- **Extreme compression**: Achieve 75-85% size reduction
- **Preserves meaning**: Full decompression possible with keys
- **Learns from your data**: Analyzes your chapters to optimize compression
- **Batch processing**: Compress multiple chapters at once
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Flexible configuration**: Customize via parameters file

### Workflow
```
Your 10 Curated Chapters → Analysis → Custom Rules → Compress New Chapters
```

---

## Quick Start

### 1. Create Your Diary Folder
```
diary/
├── chapter_01_curated.txt
├── chapter_02_curated.txt
├── chapter_03_curated.txt
└── ... (your 10 curated chapters)
```

### 2. Analyze and Compress

**Linux/macOS:**
```bash
python3 diary_compressor.py both
# or if python3 is default:
python diary_compressor.py both
```

**Windows:**
```cmd
python diary_compressor.py both
# or
py diary_compressor.py both
```

That's it! Check the `diary_compressed` folder for results.

---

## Installation & Setup

### Requirements
- Python 3.6 or higher
- No external dependencies (uses standard library only)
- Works on Windows, Linux, and macOS

### Initial Setup

1. **Save the compression script** as `diary_compressor.py`

2. **Create a parameters file** (optional but recommended):

   **Linux/macOS:**
   ```bash
   python3 diary_compressor.py --create-params
   ```
   
   **Windows:**
   ```cmd
   python diary_compressor.py --create-params
   # or
   py diary_compressor.py --create-params
   ```

3. **Edit `parameters.json`** to match your setup:
   ```json
   {
     "diary_folder": "my_diary",
     "output_folder": "my_diary_compressed",
     "config_file": "my_compression_rules.json"
   }
   ```
   
   **Note:** Both forward slashes (`/`) and backslashes (`\\`) work in Windows paths.

### Platform-Specific Setup

#### Windows
- **Recommended**: Use Windows Terminal or PowerShell for better UTF-8 character display
- If using Command Prompt, you may need to set UTF-8 encoding:
  ```cmd
  chcp 65001
  ```

#### Linux/macOS
- Make the script executable (optional):
  ```bash
  chmod +x diary_compressor.py
  ```
- Add shebang line to top of script (optional):
  ```python
  #!/usr/bin/env python3
  ```

---

## Usage Options

### Command Line Interface

The system supports three main commands. Examples are shown for both platforms:

#### 1. ANALYZE - Learn from Your Chapters

**Linux/macOS:**
```bash
python3 diary_compressor.py analyze
```

**Windows:**
```cmd
python diary_compressor.py analyze
```

Analyzes all chapters in your diary folder to generate optimal compression rules.

**Options (both platforms):**
```bash
# Specify custom diary folder
python diary_compressor.py analyze -d path/to/diary

# Use custom parameters file
python diary_compressor.py analyze -p my_params.json

# Specify output config file
python diary_compressor.py analyze -c my_rules.json
```

#### 2. COMPRESS - Compress Chapters

**Linux/macOS:**
```bash
python3 diary_compressor.py compress
```

**Windows:**
```cmd
python diary_compressor.py compress
```

Compresses chapters using previously generated rules.

**Options (both platforms):**
```bash
# Compress specific files only
python diary_compressor.py compress -f chapter_11.txt chapter_12.txt

# Use different output folder
python diary_compressor.py compress -o special_output

# Use specific configuration
python diary_compressor.py compress -c custom_rules.json
```

#### 3. BOTH - Analyze Then Compress

**Linux/macOS:**
```bash
python3 diary_compressor.py both
```

**Windows:**
```cmd
python diary_compressor.py both
```

Performs analysis followed immediately by compression.

**Options (both platforms):**
```bash
# Full custom setup
python diary_compressor.py both -d diary -o compressed -c rules.json

# With parameters file
python diary_compressor.py both -p production_params.json
```

### Command Line Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--diary-folder` | `-d` | Input folder with chapters | `-d my_diary` |
| `--output-folder` | `-o` | Output for compressed files | `-o compressed` |
| `--config-file` | `-c` | Configuration file path | `-c rules.json` |
| `--params-file` | `-p` | Parameters file | `-p params.json` |
| `--specific-files` | `-f` | Compress specific files | `-f ch1.txt ch2.txt` |

### Using Parameters File

Instead of command line arguments, you can use a `parameters.json` file:

```json
{
  "diary_folder": "diary",
  "output_folder": "diary_compressed",
  "config_file": "diary_compression_config.json",
  "chapter_patterns": [
    "chapter*.txt",
    "curated*.txt",
    "diary_entry*.txt"
  ],
  "file_extensions": [".txt", ".md"],
  "compression_params": {
    "min_word_length_for_vowel_removal": 5,
    "aggressive_vowel_removal": true,
    "track_topics": true,
    "track_entities": true,
    "compress_whitespace": true
  }
}
```

**Path Format Notes:**
- **Linux/macOS**: Use forward slashes: `"diary_folder": "path/to/diary"`
- **Windows**: Both work:
  - Forward slashes: `"diary_folder": "path/to/diary"`
  - Escaped backslashes: `"diary_folder": "path\\to\\diary"`

---

## Parameters Reference

### Core Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `diary_folder` | `"diary"` | Folder containing your curated chapters |
| `output_folder` | `"diary_compressed"` | Where compressed files are saved |
| `config_file` | `"diary_compression_config.json"` | Generated rules file |

### Pattern Matching

| Parameter | Default | Description |
|-----------|---------|-------------|
| `chapter_patterns` | `["chapter*.txt"]` | Patterns to identify chapter files |
| `file_extensions` | `[".txt", ".md"]` | File types to process |

**Note on Case Sensitivity:**
- **Linux/macOS**: Case-sensitive (`Chapter*.txt` ≠ `chapter*.txt`)
- **Windows**: Case-insensitive (both patterns match the same files)

### Analysis Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_phrase_length` | `2` | Minimum words in a phrase to track |
| `min_phrase_freq` | `3` | Minimum occurrences to compress a phrase |
| `max_symbols` | `50` | Max single-symbol replacements |
| `max_two_letter_codes` | `100` | Max two-letter abbreviations |
| `max_phrase_codes` | `200` | Max phrase compressions |

### Compression Settings

| Parameter | Default | Description |
|-----------|---------|-------------|
| `min_word_length_for_vowel_removal` | `5` | Remove vowels from words this long |
| `aggressive_vowel_removal` | `true` | Remove all vowels except first |
| `track_topics` | `true` | Create references for repeated topics |
| `track_entities` | `true` | Track names and proper nouns |
| `compress_whitespace` | `true` | Remove unnecessary spaces |

---

## How It Works

### The Two-Phase Process

#### Phase 1: Analysis (Learning)
The system reads your 10 curated chapters and learns:

1. **Word Frequency Analysis**
   - Identifies your most common words
   - Assigns single symbols (§, @, #) to ultra-common words
   - Creates two-letter codes (QX, QZ) for very common words

2. **Phrase Pattern Detection**
   - Finds repeated multi-word phrases
   - Common questions: "can you help" → "?11"
   - Common statements: "that makes sense" → "!4"
   - Transitions: "by the way" → "~1"

3. **Structural Analysis**
   - Sentence patterns you frequently use
   - Common word endings (suffixes)
   - Character-level patterns (bigrams)

4. **Compression Rule Generation**
   - Creates a custom configuration file
   - Optimizes rules for YOUR specific writing style
   - Estimates compression potential

#### Phase 2: Compression (Applying)
Using the learned rules, the system compresses new chapters:

1. **Phrase Replacement**
   - Replaces common phrases with short codes
   - "can you help me understand" → "?11 me undrstnd"

2. **Word Compression**
   - Ultra-common words → symbols
   - Common words → two-letter codes
   - Long words → vowel removal
   - Very long words → custom abbreviations

3. **Entity & Topic Tracking**
   - First mention: "machine learning"
   - Later mentions: "E1" (entity reference)
   - Builds references throughout the document

4. **Repeated Block Detection**
   - Identifies repeated explanations or paragraphs
   - Replaces duplicates with block references: "[B:a3f2c1]"

5. **Whitespace Optimization**
   - Removes spaces before punctuation
   - Compresses multiple spaces
   - Optimizes line breaks

### Compression Techniques Explained

#### Symbol Mappings
Most frequent words become single characters:
- "the" → "§"
- "and" → "&"
- "you" → "U"

#### Two-Letter Codes
Common words get two-letter codes using rare letter combinations:
- "would" → "QW"
- "about" → "QA"
- "there" → "QT"

#### Phrase Compression
Multi-word patterns get coded by category:
- Questions: "?" prefix ("can you" → "?1")
- Statements: "!" prefix ("I think" → "!1")
- Transitions: "~" prefix ("however" → "~11")

#### Vowel Removal
Words ≥5 characters lose vowels (except first):
- "understanding" → "undrstndng"
- "compression" → "cmprsn"
- "conversation" → "cnvrstn"

#### Entity References
Repeated proper nouns get numbered references:
- First: "Claude"
- Later: "E1"

#### Block References
Repeated sentences/paragraphs become hashes:
- First: Full text
- Later: "[B:hash]"

---

## Understanding Your Results

### Output Files

After compression, you'll find:

```
diary_compressed/
├── chapter_01_curated.cmp.txt          # Compressed chapter
├── chapter_01_curated.cmp.txt.key.json # Decompression key
├── chapter_02_curated.cmp.txt
├── chapter_02_curated.cmp.txt.key.json
└── _compression_results.json           # Overall statistics
```

### Compressed File Format
```
[DIARY:a3f2c1b8]
◊?11 me undrstnd mchn lrnng?
◈!1 its @ typ of AI tht enbls cmptrs 2 lrn frm data.
◊!4.?14 nrl ntwrks?
```

### Decompression Key Structure
```json
{
  "version": "2.0",
  "filename": "chapter_01_curated.txt",
  "mappings": {
    "symbols": {"§": "the", "&": "and"},
    "phrases": {"?11": "can you help"},
    "entities": {"E1": "machine learning"},
    "blocks": {"a3f2c1": "This is a repeated block of text..."}
  },
  "stats": {
    "original_length": 50000,
    "compressed_length": 10000,
    "compression_ratio": "80.0%"
  }
}
```

### Statistics File
Shows overall compression performance:
```json
{
  "files_compressed": 10,
  "total_original_size": 500000,
  "total_compressed_size": 100000,
  "overall_compression_ratio": "80.0%"
}
```

---

## Tips & Best Practices

### For Best Compression

1. **Use at least 10 chapters for analysis**
   - More data = better pattern detection
   - Include diverse conversation types

2. **Keep consistent formatting**
   - Use the same speaker labels (Human:/Assistant:)
   - Maintain consistent paragraph structure

3. **Run analysis periodically**
   - Re-analyze every 20-30 new chapters
   - Your style may evolve over time

### Optimizing Parameters

#### For Maximum Compression (85%+)
```json
{
  "compression_params": {
    "min_word_length_for_vowel_removal": 4,
    "aggressive_vowel_removal": true,
    "max_symbols": 100,
    "max_phrase_codes": 500
  }
}
```

#### For Better Readability (70-75%)
```json
{
  "compression_params": {
    "min_word_length_for_vowel_removal": 6,
    "aggressive_vowel_removal": false,
    "max_symbols": 30,
    "track_entities": false
  }
}
```

### Managing Multiple Configurations

You can maintain different configs for different content types:

```bash
# Technical discussions
python diary_compressor.py analyze -d tech_diary -c tech_config.json

# Personal diary
python diary_compressor.py analyze -d personal_diary -c personal_config.json

# Compress using specific config
python diary_compressor.py compress -c tech_config.json
```

---

## Troubleshooting

### Common Issues and Solutions

#### "No chapter files found"
- Check your `chapter_patterns` in parameters.json
- **Linux/macOS**: Remember patterns are case-sensitive
- **Windows**: Check file extensions match (.txt vs .TXT both work)
- Ensure files have correct extensions (.txt or .md)
- Verify the diary_folder path is correct

#### Low compression ratio (<70%)
- Analyze more chapters (minimum 10 recommended)
- Check if chapters have enough repetition
- Adjust compression parameters for more aggressive settings

#### Error reading files
- Ensure files are UTF-8 encoded
- Check file permissions
- Remove any binary files from diary folder

#### Configuration not found
- Run `analyze` before `compress`
- Check config_file path in parameters
- Ensure previous analysis completed successfully

#### Special Characters Not Displaying (Windows)
- Use Windows Terminal or PowerShell instead of Command Prompt
- Set console to UTF-8: run `chcp 65001` before running the script
- Special characters (§, ◊, ω) display better in modern terminals

#### Python Command Not Found
- **Windows**: Try `py` instead of `python`
- **Linux/macOS**: Try `python3` instead of `python`
- Verify Python installation: `python --version` or `python3 --version`

### Platform-Specific Issues

#### Windows Issues
- **"Module not found"**: Ensure you're in the correct directory
- **Path errors**: Use forward slashes or escaped backslashes in parameters.json
- **Encoding errors**: Run in PowerShell or Windows Terminal with UTF-8

#### Linux/macOS Issues
- **Permission denied**: Make script executable: `chmod +x diary_compressor.py`
- **Python version**: Ensure using Python 3: `python3 --version`
- **Case sensitivity**: Check file patterns match exact case

### Performance Considerations

- **Analysis time**: ~1-2 seconds per chapter
- **Compression time**: ~0.5 seconds per chapter
- **Memory usage**: Minimal (< 100MB for typical usage)
- **Maximum chapter size**: No hard limit, tested up to 1MB

### Getting Help

1. **Check Python version**: 
   - Windows: `python --version` or `py --version`
   - Linux/macOS: `python3 --version`
2. **Check parameters**: `cat parameters.json` (Linux/macOS) or `type parameters.json` (Windows)
3. **Verify structure**: 
   - Linux/macOS: `ls -la diary/`
   - Windows: `dir diary`
4. **Test with sample**: Try with 1-2 chapters first
5. **Check output**: Review _compression_results.json for details

---

## Advanced Usage

### Batch Processing Multiple Diaries

**Linux/macOS (bash script):**
```bash
#!/bin/bash
# Process multiple diaries
for diary in diary1 diary2 diary3; do
    python3 diary_compressor.py both -d $diary -o ${diary}_compressed
done
```

**Windows (batch script):**
```batch
@echo off
REM Process multiple diaries
for %%d in (diary1 diary2 diary3) do (
    python diary_compressor.py both -d %%d -o %%d_compressed
)
```

**Cross-platform (Python script):**
```python
# batch_compress.py
import subprocess
import sys

diaries = ["diary1", "diary2", "diary3"]
python_cmd = "python3" if sys.platform != "win32" else "python"

for diary in diaries:
    subprocess.run([
        python_cmd, "diary_compressor.py", "both",
        "-d", diary,
        "-o", f"{diary}_compressed"
    ])
```

### Automated Compression Pipeline

**Cross-platform Python script:**
```python
# compress_new_chapters.py
import subprocess
import os
import sys

# Determine Python command based on platform
python_cmd = "python3" if sys.platform != "win32" else "python"

new_chapters = ["chapter_11.txt", "chapter_12.txt"]
for chapter in new_chapters:
    if os.path.exists(chapter):
        subprocess.run([
            python_cmd, "diary_compressor.py", "compress",
            "-f", chapter
        ])
```

**Linux/macOS cron job (daily at 2 AM):**
```bash
# Add to crontab with: crontab -e
0 2 * * * cd /path/to/diary && python3 diary_compressor.py compress
```

**Windows Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily/weekly)
4. Set action: Start a program
5. Program: `python`
6. Arguments: `diary_compressor.py compress`
7. Start in: `C:\path\to\diary`

### Integration with Claude

When providing compressed text to Claude:
1. Include the compressed text
2. Provide the decompression key (or relevant portions)
3. Mention it's compressed using this system
4. Claude can reference the original file if needed

---

## Summary

The Diary Compression System provides powerful, customized compression for your curated diary chapters. By learning from your existing content, it achieves 75-85% compression while maintaining the ability to fully reconstruct the original text using decompression keys. The system is designed to be simple to use while offering extensive customization options for advanced users.