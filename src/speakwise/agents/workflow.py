from speakwise.agents.intent_classifier import classify_intent
from speakwise.agents.communication_planner import create_plan

def process_request(user_input:str):

    # Step 1: Identify the user intent
    intent = classify_intent(user_input)

    # Step 2: Generate execution plan
    plan  = create_plan(user_input, intent)

    return {
        "intent": intent,
        "plan": plan
    }