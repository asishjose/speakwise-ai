
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.tools.tone import ToneImprovement


SYSTEM_PROMPT = """
You are the Tone Improvement Tool of SpeakWise AI.

Your responsibility is to analyze and improve the tone of communication.

Instructions:
1. Identify the original tone of the text.
2. Rewrite the text using the requested target tone.
3. Preserve the original meaning and intent.
4. Do not introduce new information.
5. Maintain clarity and natural language.
6. Explain the changes made.
7. If the original text already matches the target tone,
   make minimal or no changes.

Return a structured response matching the provided schema.
"""


def improve_tone(
    user_input: str,
    target_tone: str
) -> ToneImprovement:

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty")

    if not target_tone or not target_tone.strip():
        raise ValueError("Target tone cannot be empty")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
            ORIGINAL TEXT:
            {user_input}

            TARGET TONE:
            {target_tone}
            """,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ToneImprovement,
                temperature=0.2
            )
        )

        if response.parsed is not None:
            return ToneImprovement.model_validate(response.parsed)

        if response.text:
            return ToneImprovement.model_validate_json(response.text)

        raise ValueError("Gemini returned an empty response")

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Tone improvement failed: {str(e)}"
        ) from e
