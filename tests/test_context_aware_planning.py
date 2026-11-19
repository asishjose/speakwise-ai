
from speakwise.agents.intent_classifier import classify_intent
from speakwise.agents.communication_planner import create_plan


def main():

    conversation_context = """
    USER:
    Write an email requesting two days of leave.

    ASSISTANT:
    Subject: Leave Request

    Dear Manager,

    I would like to request two days of leave next week.
    Please let me know if this can be approved.

    Thank you.
    """

    user_input = "Make it more formal."

    # Step 1: Context-aware intent classification
    intent = classify_intent(
        user_input=user_input,
        conversation_context=conversation_context
    )

    print("\n========== INTENT ==========")
    print(intent.model_dump_json(indent=2))

    # Step 2: Context-aware planning
    plan = create_plan(
        user_input=user_input,
        intent=intent,
        conversation_context=conversation_context
    )

    print("\n========== PLAN ==========")
    print(plan.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
