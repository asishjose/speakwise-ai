
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.tools.conversation import ConversationImprovement


SYSTEM_PROMPT = """
You are the Conversation Improvement Tool of SpeakWise AI.

Your responsibility is to improve responses in everyday
and professional conversations.

Instructions:
1. Understand the conversation context.
2. Understand the user's intended message.
3. Improve clarity, naturalness and relevance.
4. Maintain the user's original meaning.
5. Make the response sound natural and human.
6. Avoid unnecessarily formal or robotic language.
7. Adapt the response to the relationship and situation.
8. Provide useful suggestions for better communication.

Return a structured response matching the provided schema.
"""


def improve_conversation(
    conversation_context: str,
    original_response: str,
    communication_goal: str = "Respond naturally and clearly"
) -> ConversationImprovement:

    if not conversation_context or not conversation_context.strip():
        raise ValueError("Conversation context cannot be empty")

    if not original_response or not original_response.strip():
        raise ValueError("Original response cannot be empty")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"""
            CONVERSATION CONTEXT:
            {conversation_context}

            USER'S ORIGINAL RESPONSE:
            {original_response}

            COMMUNICATION GOAL:
            {communication_goal}
            """,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=ConversationImprovement,
                temperature=0.4
            )
        )

        if response.parsed is not None:
            return ConversationImprovement.model_validate(response.parsed)

        if response.text:
            return ConversationImprovement.model_validate_json(response.text)

        raise ValueError("Gemini returned an empty response")

    except ValueError:
        raise

    except Exception as e:
        raise RuntimeError(
            f"Conversation improvement failed: {str(e)}"
        ) from e
