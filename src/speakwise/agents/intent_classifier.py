
from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.intent import IntentClassification


SYSTEM_PROMPT = """
You are the intent classification engine of SpeakWise AI.

Your responsibility is to identify the primary communication
goal behind the user's message.

Choose exactly one intent from the available categories.

Categories:

1. email_writing:
   Creating, drafting or composing emails.

2. interview_practice:
   Interview preparation, mock interviews, practicing interview
   questions and improving interview answers.

3. grammar_correction:
   Identifying and correcting grammatical mistakes in existing text.

4. tone_improvement:
   Analyzing or changing communication tone, such as making
   existing content more polite, professional, confident or friendly.

5. conversation_improvement:
   Improving everyday conversational responses, replies,
   interpersonal communication and dialogue.

6. communication_evaluation:
   Evaluating communication quality, including clarity,
   grammar, tone, structure, confidence and effectiveness.
   Includes scoring or rating communication performance.

7. public_speaking:
   Speech preparation, presentation delivery and speaking skills.

8. conflict_resolution:
   Handling disagreements, misunderstandings and workplace conflicts.

9. customer_communication:
   Communicating with customers, handling complaints and
   preparing customer service responses.

10. other:
    Requests unrelated to the above categories.

Classification rules:

- Identify the user's primary goal, not merely keywords.
- Consider the complete context of the request.
- Select the most relevant category.
- Choose exactly one primary intent.
- If multiple communication goals are present, identify the
  dominant goal. The planner will determine whether multiple
  tools are required.
- Distinguish between improving communication and evaluating it.
- Do not classify every request to write a response as
  conversation_improvement. Use the appropriate specific category.
- Do not perform the requested task.
- Do not invent missing context.
- Provide a brief explanation for your classification.
"""


def classify_intent(user_input: str) -> IntentClassification:

    if not user_input.strip():
        raise ValueError("User input cannot be empty")

    response = client.models.generate_content(
        model=MODEL,
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=IntentClassification,
            temperature=0.1
        )
    )

    if response.parsed is not None:
        return IntentClassification.model_validate(response.parsed)

    if response.text:
        return IntentClassification.model_validate_json(response.text)

    raise ValueError("Gemini returned an empty response")
