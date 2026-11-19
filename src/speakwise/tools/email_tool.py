
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.tools.email import EmailGeneration


SYSTEM_PROMPT = """
You are the Email Writing Tool of SpeakWise AI.

Your responsibility is to generate clear, professional and
well-structured emails based on the user's requirements.

Instructions:
1. Generate an appropriate subject line.
2. Structure the email with a suitable greeting and closing.
3. Maintain the requested tone.
4. Include all relevant information provided by the user.
5. Do not invent facts or commitments.
6. Keep the email concise and clear.
7. Use placeholders for missing details when necessary.
8. Adapt the writing style to the recipient and purpose.

Return a structured response matching the provided schema.
"""


def generate_email(
    recipient: str,
    purpose: str,
    context: str = "",
    tone: str = "Professional"
) -> EmailGeneration:

    if not recipient or not recipient.strip():
        raise ValueError("Recipient cannot be empty")

    if not purpose or not purpose.strip():
        raise ValueError("Email purpose cannot be empty")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
            RECIPIENT:
            {recipient}

            PURPOSE:
            {purpose}

            ADDITIONAL CONTEXT:
            {context}

            DESIRED TONE:
            {tone}
            """,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=EmailGeneration,
                temperature=0.4
            )
        )

        if response.parsed is not None:
            return EmailGeneration.model_validate(response.parsed)

        if response.text:
            return EmailGeneration.model_validate_json(response.text)

        raise ValueError("Gemini returned an empty response")

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Email generation failed: {str(e)}"
        ) from e
