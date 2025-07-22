#!/usr/bin/env python3

from src.utils import concatenate_all_files

def count_document_characters():
    try:
        full_document = concatenate_all_files()
        char_count = len(full_document)
        
        print(f"Full concatenated document statistics:")
        print(f"Total characters: {char_count:,}")
        print(f"Approximate words: {char_count // 5:,}")
        print(f"Approximate tokens (rough estimate): {char_count // 4:,}")
        
        # Save count to file for reference
        with open("document_stats.txt", "w") as f:
            f.write(f"Full Document Statistics\n")
            f.write(f"========================\n")
            f.write(f"Total characters: {char_count:,}\n")
            f.write(f"Approximate words: {char_count // 5:,}\n")
            f.write(f"Approximate tokens: {char_count // 4:,}\n")
        
        print("\nStats saved to: document_stats.txt")
        
    except Exception as e:
        print(f"❌ Error counting characters: {str(e)}")

if __name__ == "__main__":
    count_document_characters()