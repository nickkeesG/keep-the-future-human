#!/usr/bin/env python3

from src.translator import Translator

def test_analysis():
    try:
        translator = Translator()
        
        # Test with Dutch as target language
        analysis = translator.analyze_document_for_language("Dutch")
        
        # Export full analysis to text file
        with open("analysis_test_output.txt", "w", encoding="utf-8") as f:
            f.write(analysis)
        
        print("✅ Analysis completed successfully!")
        print(f"Analysis length: {len(analysis)} characters")
        print("Full analysis exported to: analysis_test_output.txt")
        
    except Exception as e:
        print("❌ Analysis failed!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_analysis()