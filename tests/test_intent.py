from speakwise.agents.intent_classifier import classify_intent


user_input = "Make this email sound more professional and polite."

result = classify_intent(user_input)

print("User Input:", user_input)
print("Intent:", result.intent)
print("Confidence:", result.confidence)
print("Reasoning:", result.reasoning)

print("\nComplete JSON:")
print(result.model_dump_json(indent=2))


test_cases = [
    "Write an email requesting leave from my manager.",

    "Conduct a mock interview for a machine learning engineer role.",

    "Correct the grammar in this paragraph.",

    "Make this message sound more polite and professional.",

    "Help me prepare a speech for a college event.",

    "My colleague and I disagree about a project. Help me handle it.",

    "A customer is angry about a delayed order. Help me respond.",

    "What is the capital of France?"
]


for text in test_cases:

    result = classify_intent(text)

    print("-" * 60)
    print("Input:", text)
    print("Predicted intent:", result.intent)
    print("Confidence:", result.confidence)