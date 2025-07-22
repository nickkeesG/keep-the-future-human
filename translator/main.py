#!/usr/bin/env python3
"""
Translation Pipeline CLI

Usage:
    python main.py <language>

Example:
    python main.py Spanish
    python main.py Dutch
    python main.py French
"""

import sys
from src.translator import Translator

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <language>")
        print("\nExample:")
        print("  python main.py Spanish")
        print("  python main.py Dutch")
        print("  python main.py French")
        sys.exit(1)
    
    target_language = sys.argv[1]
    
    # Confirm with user
    print(f"🌍 You are about to translate all 14 chapters to {target_language}")
    print("⚠️  This will make multiple API calls and incur costs.")
    confirm = input("Continue? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("Translation cancelled.")
        sys.exit(0)
    
    # Run translation
    try:
        translator = Translator()
        successful, failed = translator.translate_all_chapters_for_language(target_language)
        
        if len(failed) == 0:
            print(f"🎉 All chapters successfully translated to {target_language}!")
        else:
            print(f"⚠️  Translation completed with {len(failed)} failures.")
            
    except KeyboardInterrupt:
        print("\n❌ Translation interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Translation failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()