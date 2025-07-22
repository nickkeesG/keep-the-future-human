#!/usr/bin/env python3
"""
Test concatenation script with original English markdown files.
"""

import re
import yaml
from pathlib import Path

def increment_headers(content: str) -> str:
    """
    Increment all markdown header levels by one, except the very first # header.
    # -> stays #, ## -> ###, etc.
    The first # header is preserved as the main title.
    """
    first_h1_found = False
    
    def replace_header(match):
        nonlocal first_h1_found
        hashes = match.group(1)
        rest = match.group(2)
        
        # If this is a single # and we haven't found the first one yet
        if hashes == '#' and not first_h1_found:
            first_h1_found = True
            return hashes + rest  # Don't increment the first #
        else:
            return '#' + hashes + rest  # Increment all others
    
    pattern = r'^(#{1,6})(.*)$'
    return re.sub(pattern, replace_header, content, flags=re.MULTILINE)

def renumber_footnotes(content: str, start_number: int = 1) -> tuple[str, int]:
    """
    Renumber all footnotes in content starting from start_number.
    Returns (modified_content, next_available_number)
    """
    # Find all footnote references [^number]
    footnote_refs = re.findall(r'\[\^(\d+)\]', content)
    unique_footnotes = list(dict.fromkeys(footnote_refs))  # Remove duplicates, preserve order
    
    # Create mapping from old numbers to new numbers
    footnote_mapping = {}
    current_number = start_number
    
    for old_num in unique_footnotes:
        footnote_mapping[old_num] = str(current_number)
        current_number += 1
    
    # Replace footnote references [^old] -> [^new]
    def replace_ref(match):
        old_num = match.group(1)
        new_num = footnote_mapping.get(old_num, old_num)
        return f'[^{new_num}]'
    
    content = re.sub(r'\[\^(\d+)\]', replace_ref, content)
    
    return content, current_number

def test_concatenate_english():
    """
    Test concatenation with original English files.
    """
    # Load config to get file order
    with open("config/settings.yaml", 'r') as f:
        config = yaml.safe_load(f)
    
    source_dir = Path("original markdown")
    
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")
    
    print(f"📁 Processing files from: {source_dir}")
    
    result = ""
    current_footnote_number = 1
    processed_files = 0
    first_h1_found = False  # Track if we've seen the first # header globally
    
    for filename in config['source_files']:
        file_path = source_dir / filename
        
        if not file_path.exists():
            print(f"⚠️  Warning: {filename} not found (skipping)")
            continue
        
        print(f"📄 Processing: {filename}")
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            print(f"⚠️  Warning: {filename} is empty (skipping)")
            continue
        
        # Step 1: Increment headers (but preserve the very first # across all files)
        def replace_header(match):
            nonlocal first_h1_found
            hashes = match.group(1)
            rest = match.group(2)
            
            # If this is a single # and we haven't found the first one yet
            if hashes == '#' and not first_h1_found:
                first_h1_found = True
                return hashes + rest  # Don't increment the first #
            else:
                return '#' + hashes + rest  # Increment all others
        
        pattern = r'^(#{1,6})(.*)$'
        content = re.sub(pattern, replace_header, content, flags=re.MULTILINE)
        
        # Step 2: Renumber footnotes
        content, current_footnote_number = renumber_footnotes(content, current_footnote_number)
        
        # Step 3: Add to result with spacing
        if processed_files > 0:
            result += "\n\n"  # Add spacing between chapters
        
        result += content
        processed_files += 1
    
    print(f"✅ Successfully processed {processed_files} files")
    print(f"📊 Total footnotes renumbered: {current_footnote_number - 1}")
    
    # Write output to translations/full essays folder
    output_dir = Path("translations") / "full essays"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_filename = "Keep_the_Future_Human_English.md"
    output_path = output_dir / output_filename
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"\n🎉 Test concatenation complete!")
    print(f"📄 Output file: {output_path}")
    print(f"📊 File size: {len(result):,} characters")

if __name__ == "__main__":
    test_concatenate_english()