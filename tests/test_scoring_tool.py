
from speakwise.tools.scoring_tool import evaluate_communication


def main():
    text = """
    Dear Manager,

    I would like to request two days of leave next week
    due to a family function. Please let me know if this
    can be approved.

    Thank you.
    """

    result = evaluate_communication(
        user_input=text,
        context="Professional email requesting leave"
    )

    print("\nGrammar score:", result.grammar_score)
    print("Clarity score:", result.clarity_score)
    print("Tone score:", result.tone_score)
    print("Relevance score:", result.relevance_score)

    print("\nOverall score:", result.overall_score)

    print("\nStrengths:", result.strengths)
    print("\nWeaknesses:", result.weaknesses)
    print("\nRecommendations:", result.recommendations)

    print("\nSummary:", result.evaluation_summary)


if __name__ == "__main__":
    main()
