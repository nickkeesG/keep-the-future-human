from pathlib import Path
import yaml
from .api_client import AnthropicClient
from .utils import concatenate_all_files, save_markdown
from .cot_prompts import PROMPT_A, PROMPT_B, PROMPT_C, PROMPT_D, PROMPT_E


class Translator:
    def __init__(self, config_path: str = "config/settings.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.client = AnthropicClient(config_path)
        self.output_dir = Path(self.config['directories']['output'])
    
    def analyze_document_for_language(self, target_language: str) -> str:
        """
        Step 1: Analyze the full document for a target language
        Returns: Summary, glossary, and style guide
        """
        print(f"Analyzing document for {target_language} translation...")
        
        # Concatenate all files
        full_document = concatenate_all_files()
        
        # Build the complete prompt
        prompt_a = PROMPT_A.format(target_language=target_language)
        prompt_b = PROMPT_B.format(target_language=target_language)
        
        full_prompt = prompt_a + full_document + prompt_b
        
        # Make API call
        analysis = self.client.send_message(full_prompt)
        
        # Save analysis to file
        analysis_dir = self.output_dir / target_language.lower() / "analysis"
        analysis_dir.mkdir(parents=True, exist_ok=True)
        
        analysis_file = analysis_dir / "document_analysis.md"
        save_markdown(analysis_file, analysis)
        
        print(f"Analysis saved to: {analysis_file}")
        return analysis
    
    def translate_individual_chapter(self, filename: str, target_language: str, analysis: str, force_retranslate: bool = False) -> str:
        """
        Step 2: Translate a single chapter using the analysis from step 1
        """
        # Check if translation already exists
        language_dir = self.output_dir / target_language.lower()
        translated_file = language_dir / filename
        
        if translated_file.exists() and not force_retranslate:
            print(f"✓ {filename} already translated to {target_language} (skipping)")
            with open(translated_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        print(f"Translating {filename} to {target_language}...")
        
        # Load the individual chapter
        source_dir = Path(self.config['directories']['source'])
        chapter_path = source_dir / filename
        
        if not chapter_path.exists():
            raise FileNotFoundError(f"Chapter file not found: {chapter_path}")
        
        chapter_content = ""
        with open(chapter_path, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        # Build the complete prompt: PromptC + Analysis + PromptD + Chapter + PromptE
        prompt_c = PROMPT_C.format(target_language=target_language)
        prompt_d = PROMPT_D
        prompt_e = PROMPT_E.format(target_language=target_language)
        
        full_prompt = prompt_c + analysis + prompt_d + chapter_content + prompt_e
        
        # Make API call
        translated_content = self.client.send_message(full_prompt)
        
        # Save translated chapter
        language_dir.mkdir(parents=True, exist_ok=True)
        save_markdown(translated_file, translated_content)
        
        print(f"Translation saved to: {translated_file}")
        return translated_content
    
    def translate_all_chapters_for_language(self, target_language: str):
        """
        Complete translation pipeline for one language:
        1. Generate/load analysis for the language
        2. Translate all 14 chapters using that analysis
        """
        print(f"=== Starting complete translation to {target_language} ===")
        
        # Step 1: Get or create analysis
        analysis_file = self.output_dir / target_language.lower() / "analysis" / "document_analysis.md"
        
        force_retranslate = False
        if analysis_file.exists():
            print(f"✅ Using existing analysis from {analysis_file}")
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = f.read()
        else:
            print("📊 Creating new document analysis...")
            analysis = self.analyze_document_for_language(target_language)
            print("🔄 New analysis created - will retranslate all chapters for consistency")
            force_retranslate = True
        
        # Step 2: Translate all chapters
        print(f"📖 Processing all {len(self.config['source_files'])} chapters...")
        
        successful_translations = 0
        failed_translations = []
        skipped_translations = 0
        
        for i, filename in enumerate(self.config['source_files'], 1):
            try:
                print(f"[{i}/{len(self.config['source_files'])}] Processing {filename}...")
                
                # Check if file exists before translation attempt
                language_dir = self.output_dir / target_language.lower()
                translated_file = language_dir / filename
                
                if translated_file.exists() and not force_retranslate:
                    skipped_translations += 1
                    print(f"✓ {filename} already exists (skipping)")
                else:
                    self.translate_individual_chapter(filename, target_language, analysis, force_retranslate)
                    successful_translations += 1
                    
                    # Small delay to be respectful to API (only after actual translation)
                    if force_retranslate or not translated_file.exists():
                        import time
                        time.sleep(1)
                
            except Exception as e:
                print(f"❌ Failed to process {filename}: {str(e)}")
                failed_translations.append((filename, str(e)))
        
        # Summary
        print(f"\n=== Translation Summary for {target_language} ===")
        print(f"✅ Successful translations: {successful_translations}")
        print(f"⏭️  Skipped (already exist): {skipped_translations}")
        print(f"❌ Failed: {len(failed_translations)}")
        
        if failed_translations:
            print("\nFailed translations:")
            for filename, error in failed_translations:
                print(f"  - {filename}: {error}")
        
        print(f"\nAll translations saved to: translations/{target_language.lower()}/")
        
        return successful_translations, failed_translations