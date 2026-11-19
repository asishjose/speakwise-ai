
from speakwise.tools.conversation_tool import improve_conversation


def main():
    result = improve_conversation(
        conversation_context=(
            "My colleague asked whether I could complete "
            "the assigned task by tomorrow."
        ),
        original_response="No, I can't do it. I am busy.",
        communication_goal="Be polite but communicate the delay clearly"
    )

    print("\nOriginal:", result.original_response)
    print("\nImproved:", result.improved_response)
    print("\nExplanation:", result.explanation)
    print("\nSuggestions:", result.suggestions)


if __name__ == "__main__":
    main()
