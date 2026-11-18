from google.genai import types

from speakwise.llm_client import client, MODEL
from speakwise.schemas.intent import IntentClassification
from speakwise.schemas.plan import CommunicationPlan


PLANNER_PROMPT = """
You are the Communication Planner of SpeakWise AI.

Your responsibility is to convert the user's communication
request into an actionable execution plan.

You do not execute tasks or generate the final communication.

AVAILABLE TOOLS:

1. email_writer
   Creates professional emails.

2. interview_coach
   Helps users prepare and practice interview answers.

3. grammar_checker
   Identifies and corrects grammatical mistakes.

4. tone_improver
   Improves tone, politeness, confidence and professionalism.

5. speech_coach
   Helps prepare and improve speeches and presentations.

6. conflict_resolution_coach
   Provides strategies for handling disagreements and conflicts.

7. customer_communication_writer
   Creates responses for customer queries and complaints.

PLANNING INSTRUCTIONS:

1. Identify the user's primary goal.

2. Break the request into distinct responsibilities.

3. Assign each responsibility to its appropriate
   specialized tool.

4. Do not automatically assign every request to one tool.

5. Use multiple tools when the request contains
   multiple independent or dependent responsibilities.

6. TOOL SELECTION RULES:

   - email_writer:
     Creating, drafting or composing emails.

   - grammar_checker:
     Correcting grammatical mistakes in existing text.

   - tone_improver:
     Transforming the tone of existing content.

   - interview_coach:
     Interview preparation and practice.

   - speech_coach:
     Speech and presentation preparation.

   - conflict_resolution_coach:
     Handling disagreements and conflicts.

   - customer_communication_writer:
     Creating customer-facing responses.

7. If a request requires creating content and then
   modifying that content using another specialized tool,
   select both tools.

8. Do not select tools merely because a desired quality
   is mentioned.

9. Identify dependencies between selected actions.

10. Identify missing essential information.

11. If optional information is missing, do not
    unnecessarily block execution. Use placeholders
    or reasonable defaults where appropriate.

12. Never execute tools. Only generate the execution plan.

EXECUTION STRATEGY:

- single: Only one action is required.
- sequential: Multiple actions depend on one another.
- parallel: Multiple independent actions can be performed
  without depending on one another.

IMPORTANT:

Use the supplied intent classification as a helpful signal,
but prioritize the actual user request if they conflict.

Do not invent user information.
Return a concise, actionable execution plan.
"""


def create_plan(
    user_input: str,
    intent: IntentClassification
) -> CommunicationPlan:

    response = client.models.generate_content(
        model=MODEL,
        contents=f"""
        USER REQUEST:
        {user_input}

        INTENT CLASSIFICATION:
        {intent.model_dump_json()}
        """,
        config=types.GenerateContentConfig(
            system_instruction=PLANNER_PROMPT,
            response_mime_type="application/json",
            response_schema=CommunicationPlan,
            temperature=0.2
        )
    )

    if response.parsed is not None:
        return CommunicationPlan.model_validate(response.parsed)

    if response.text:
        return CommunicationPlan.model_validate_json(response.text)

    raise ValueError("Planner returned an empty response")