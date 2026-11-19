
from speakwise.tools.email_tool import generate_email


def main():
    result = generate_email(
        recipient="Manager",
        purpose="Request two days of leave",
        context="I have a family function to attend next week.",
        tone="Polite and professional"
    )

    print("\nSubject:", result.subject)
    print("\nEmail body:\n", result.body)
    print("\nKey points:", result.key_points)


if __name__ == "__main__":
    main()
