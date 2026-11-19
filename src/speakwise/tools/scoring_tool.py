
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.tools.scoring import CommunicationScore


SYSTEM_PROMPT = """
You are the Communication Scoring Tool of SpeakWise AI.

Your responsibility is to evaluate the quality and effectiveness
of user communication.

Evaluate the text using these dimensions:

1. Grammar:
   Correctness of grammar, spelling and punctuation.

2. Clarity:
   How clearly the message communicates its meaning.

3. Tone:
   Appropriateness of tone for the given situation.

4. Relevance:
   How effectively the message addresses its purpose.

Scoring rules:

- Give each dimension a score from 0 to 10.
- Calculate the overall score as the arithmetic mean
  of the four dimension scores.
- Round scores to one decimal place.
- Identify genuine strengths and weaknesses.
- Provide actionable recommendations.
- Consider the communication context when evaluating.
- Do not reward unnecessarily complicated language.
- Evaluate the actual communication rather than inventing
  information about the speaker.

Return a structured response matching the provided schema.
"""


def evaluate_communication(
    user_input: str,
    context: str = "General communication"
) -> CommunicationScore:

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
            COMMUNICATION TEXT:
            {user_input}

            COMMUNICATION CONTEXT:
            {context}
            """,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=CommunicationScore,
                temperature=0.1
            )
        )

        if response.parsed is not None:
            return CommunicationScore.model_validate(response.parsed)

        if response.text:
            return CommunicationScore.model_validate_json(response.text)

        raise ValueError("Gemini returned an empty response")

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Communication evaluation failed: {str(e)}"
        ) from e
