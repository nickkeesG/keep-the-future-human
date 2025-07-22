#!/usr/bin/env python3
"""
Script to convert HTML footnote links to standard markdown footnote format.

Usage:
    python fix_footnotes.py <input_file> [output_file]

If no output file is specified, will create a new file with "_fixed" suffix.
"""

import re
import sys
from pathlib import Path

def fix_footnotes(content: str) -> str:
    """
    Convert HTML footnote links to markdown footnote format.
    
    Converts: <sup><a href="...">1</a></sup>
    To: [^1]
    """
    # Pattern to match HTML footnote links
    pattern = r'<sup><a href="[^"]*">(\d+)</a></sup>'
    
    # Replace with markdown footnote format
    def replace_footnote(match):
        footnote_number = match.group(1)
        return f'[^{footnote_number}]'
    
    # Apply the replacement
    fixed_content = re.sub(pattern, replace_footnote, content)
    
    return fixed_content

def main():
    if len(sys.argv) < 2:
        print("Usage: python fix_footnotes.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        sys.exit(1)
    
    # Determine output file
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        # Create output filename with "_fixed" suffix
        stem = input_file.stem
        suffix = input_file.suffix
        output_file = input_file.parent / f"{stem}_fixed{suffix}"
    
    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fix footnotes
        fixed_content = fix_footnotes(content)
        
        # Count replacements made
        original_count = len(re.findall(r'<sup><a href="[^"]*">(\d+)</a></sup>', content))
        
        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print(f"✅ Fixed {original_count} footnote references")
        print(f"📄 Input:  {input_file}")
        print(f"📄 Output: {output_file}")
        
    except Exception as e:
        print(f"❌ Error processing file: {str(e)}")
        sys.exit(1)

def fix_footnotes_in_directory(directory: str, pattern: str = "*.md"):
    """
    Fix footnotes in all markdown files in a directory.
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    files = list(dir_path.glob(pattern))
    
    if not files:
        print(f"📭 No {pattern} files found in {directory}")
        return
    
    print(f"🔄 Processing {len(files)} files in {directory}...")
    
    total_fixes = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fixed_content = fix_footnotes(content)
            
            # Count fixes in this file
            fixes = len(re.findall(r'<sup><a href="[^"]*">(\d+)</a></sup>', content))
            
            if fixes > 0:
                # Write back to same file (in-place editing)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(fixed_content)
                
                print(f"✅ {file_path.name}: Fixed {fixes} footnotes")
                total_fixes += fixes
            else:
                print(f"➖ {file_path.name}: No footnotes to fix")
                
        except Exception as e:
            print(f"❌ Error processing {file_path.name}: {str(e)}")
    
    print(f"\n🎉 Total: Fixed {total_fixes} footnotes across {len(files)} files")

if __name__ == "__main__":
    # If called with --directory flag, process all files in directory
    if len(sys.argv) >= 2 and sys.argv[1] == "--directory":
        if len(sys.argv) < 3:
            print("Usage: python fix_footnotes.py --directory <directory_path>")
            sys.exit(1)
        fix_footnotes_in_directory(sys.argv[2])
    else:
        main()