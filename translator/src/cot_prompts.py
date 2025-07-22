# Document Analysis Prompts

PROMPT_A = """You are a professional translator preparing to translate an essay into {target_language}.

Your task is to analyze the full document below and create two definitive resources for consistent, high-quality translation:

1. **Summary** – Concise overview of the document's core themes, arguments, and structure.

2. **Glossary** – A controlled list of key terms, technical vocabulary, and complex expressions. For each entry, provide:
   - Source term
   - Final, approved translation in {target_language} (or English term if commonly used)
   - Brief explanation of usage/context
   - Notes on why this term was chosen (e.g., existing usage, clarity, consistency)

   **Do not translate English terms that are already commonly used in {target_language} (e.g., domain-specific jargon, globalized terminology). Retain them as-is unless there is an established equivalent.**

Read the full document carefully before generating your output. Do not generalize — base all decisions on the specific content and style of this document.
Use concrete rules, avoid vague recommendations.

---

DOCUMENT BEGINS:

"""

PROMPT_B = """

---

DOCUMENT ENDS.

Now provide your analysis in the following format:

## Summary
[Summarize the document's main themes, structure, and arguments.]

## Glossary
[List key terms using the format:
- **Source Term**: [English term]
- **Target Translation**: [Translated term in {target_language} or original English if widely used]
- **Context**: [How/where it appears in the document]
- **Notes**: [Why this translation (or non-translation) was chosen]

Only include terms that are relevant and recur. If the English term is standard in {target_language} usage, do not translate it. All guidance must be concrete and unambiguous. Avoid overly literal translations, and prioritize translations being fluent and easy to understand.]

"""

# Individual Chapter Translation Prompts

PROMPT_C = """You are translating a chapter from an essay into {target_language}. 

You have already analyzed the full document and created translation resources. Use these resources to ensure consistency and quality in your translation.

Below you will find:
1. Your analysis (Summary and Glossary)
2. The specific chapter to translate

Follow the Glossary exactly. Maintain consistency with the established terminology and approach.

---

ANALYSIS:

"""

PROMPT_D = """
## Style Guide

1. Prioritize Idiomatic Language
- Always favor natural-sounding over literal translations.
- Translate intent and function, not word-for-word form.
- Avoid structures that are grammatically correct but awkward in the target language.

✅ DO:  
EN: "He made up his mind."  
→ ES: "Tomó una decisión." (Not: "Hizo su mente.")

❌ DON'T:  
Force the source sentence structure into the target language.

2. Maintain Register and Tone
- Match the formality and tone of the source text:
  - Technical → technical
  - Informal → informal
  - Persuasive → persuasive
- Do not over-formalize or simplify.

3. Structure Sentences for Flow
- Use natural sentence order in the target language.
- Break up long, complex sentences if they become confusing or heavy.
- Avoid overly rigid mirror structures from the source language.

4. Respect Cultural and Linguistic Norms
- Adjust references, idioms, and metaphors to fit the target audience’s context.
- Replace culturally specific idioms with equivalents, or rephrase neutrally.
---

TARGET CHAPTER TO TRANSLATE:

"""

PROMPT_E = """

---

Translate the above chapter into {target_language} following your analysis guidelines exactly. 

Requirements:
- Preserve the exact markdown formatting (headings, lists, emphasis, links, etc.)
- Maintain footnote references and citations exactly as they appear
- Do not add any commentary, explanations, or additional text
- Output only the translated markdown content

FINAL NOTE: Focus on making sure the translation is fluent, and adapt the English text well to avoid overly literal and clunky translations. It is important for the content to flow well, as if written by a native speaker.

Begin translation:"""

