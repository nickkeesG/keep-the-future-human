#!/usr/bin/env python3

from src.translator import Translator

def test_chapter_translation():
    try:
        translator = Translator()
        
        # Step 1: Get analysis (reuse existing or create new)
        target_language = "Dutch"
        analysis_file = f"translations/{target_language.lower()}/analysis/document_analysis.md"
        
        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = f.read()
            print(f"✅ Using existing analysis from {analysis_file}")
        except FileNotFoundError:
            print("No existing analysis found. Creating new analysis...")
            analysis = translator.analyze_document_for_language(target_language)
        
        # Step 2: Translate a single chapter (test with first chapter)
        test_filename = "1.md"  # Translate Chapter 1
        
        translated_content = translator.translate_individual_chapter(
            test_filename, target_language, analysis
        )
        
        print("✅ Chapter translation completed successfully!")
        print(f"Translated content length: {len(translated_content)} characters")
        
        # Save a copy for inspection
        with open(f"chapter_translation_test_{test_filename}.txt", "w", encoding="utf-8") as f:
            f.write(translated_content)
        
        print(f"Translation sample saved to: chapter_translation_test_{test_filename}.txt")
        
    except Exception as e:
        print("❌ Chapter translation failed!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_chapter_translation()
