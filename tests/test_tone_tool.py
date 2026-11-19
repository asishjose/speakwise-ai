
from speakwise.tools.tone_tool import improve_tone


def main():
    text = "Send me the report immediately. I need it now."

    result = improve_tone(
        user_input=text,
        target_tone="Polite and professional"
    )

    print("\nOriginal:", result.original_text)
    print("\nDetected tone:", result.detected_tone)
    print("\nImproved text:", result.improved_text)
    print("\nExplanation:", result.explanation)
    print("\nChanges:", result.changes_made)


if __name__ == "__main__":
    main()
