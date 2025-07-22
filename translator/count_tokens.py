#!/usr/bin/env python3
"""
Count exact tokens in a file using Anthropic's token counting API.

Usage:
    python count_tokens.py <file_path>

Example:
    python count_tokens.py "original markdown/1.md"
"""

import sys
import anthropic
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def count_tokens_in_file(file_path: str) -> None:
    """Count tokens in a single file and display results"""
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count tokens using Anthropic API
    try:
        client = anthropic.Anthropic()
        result = client.messages.count_tokens(
            model="claude-sonnet-4-20250514",
            messages=[
                {"role": "user", "content": content}
            ]
        )
        
        tokens = result.input_tokens
        characters = len(content)
        chars_per_token = characters / tokens if tokens > 0 else 0
        
        print(f"📄 File: {file_path}")
        print(f"📊 Characters: {characters:,}")
        print(f"🔢 Tokens: {tokens:,}")
        print(f"📈 Chars/Token: {chars_per_token:.2f}")
        
    except Exception as e:
        print(f"❌ Token counting failed: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python count_tokens.py <file_path>")
        print('Example: python count_tokens.py "original markdown/1.md"')
        sys.exit(1)
    
    count_tokens_in_file(sys.argv[1])

if __name__ == "__main__":
    main()