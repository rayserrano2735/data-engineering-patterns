#!/usr/bin/env python3
"""
Reads a file and rewrites it through Python's standard file I/O.
This should create a file with clean Python-standard formatting.
"""

def rewrite_file(input_file="Aitana_40_2_trytoclean.txt", 
                 output_file="Aitana_40_2_python_rewrite.txt"):
    """
    Read a file and rewrite it using Python's standard text handling.
    This ensures consistent encoding and line endings.
    """
    
    try:
        # Read the entire file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Read {len(content)} characters from {input_file}")
        print(f"File has {len(content.splitlines())} lines")
        
        # Write it back out using Python's standard text mode
        with open(output_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        
        print(f"\nSuccessfully wrote to {output_file}")
        print("File has been rewritten with Python's standard text formatting")
        
        # Verify the files match
        with open(output_file, 'r', encoding='utf-8') as f:
            new_content = f.read()
        
        if content == new_content:
            print("✓ Verification passed - files are identical")
        else:
            print("⚠ Warning: Files don't match exactly")
            
        print(f"\nUpload {output_file} to KB and test if Claude can read it fully")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        print("Make sure the script is in the same folder as the input file")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # You can modify the filenames here if needed
    rewrite_file()