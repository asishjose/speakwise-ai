
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.tools.grammar import GrammarCorrection


SYSTEM_PROMPT = """
You are the Grammar Correction Tool of SpeakWise AI.

Your responsibility is to identify and correct grammatical
errors in the user's text.

Instructions:

1. Correct grammatical errors, spelling mistakes and punctuation.
2. Preserve the original meaning and intent.
3. Do not unnecessarily rewrite or paraphrase sentences.
4. Maintain the original tone and writing style.
5. Do not add new information.
6. Identify the errors found in the original text.
7. Explain each correction clearly and briefly.
8. If the text is already grammatically correct:
   - Return the original text as corrected_text.
   - Set has_errors to false.
   - Return empty errors_found and explanations lists.

Return only the structured response matching the provided schema.
"""


def correct_grammar(user_input: str) -> GrammarCorrection:

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=GrammarCorrection,
                temperature=0.1
            )
        )

        if response.parsed is not None:
            return GrammarCorrection.model_validate(response.parsed)

        if response.text:
            return GrammarCorrection.model_validate_json(response.text)

        raise ValueError("Gemini returned an empty response")

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Grammar correction failed: {str(e)}"
        ) from e
