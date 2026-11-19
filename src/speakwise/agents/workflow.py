
from speakwise.agents.intent_classifier import classify_intent
from speakwise.agents.communication_planner import create_plan
from speakwise.agents.tool_executor import execute_plan


def process_request(user_input: str):

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty")

    # Step 1: Identify intent
    intent = classify_intent(user_input)

    # Step 2: Generate execution plan
    plan = create_plan(user_input, intent)

    # Step 3: Execute selected tools
    execution = execute_plan(plan)

    # Step 4: Return complete result
    return {
        "intent": intent,
        "plan": plan,
        "execution": execution
    }
