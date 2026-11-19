
from speakwise.tools.interview_tool import conduct_interview


def main():
    # Test 1: Generate an interview question
    question_result = conduct_interview(
        role="Machine Learning Engineer",
        mode="ask_question",
        experience_level="Entry level"
    )

    print("\nGenerated question:")
    print(question_result.interview_question)

    # Test 2: Evaluate a candidate answer
    answer_result = conduct_interview(
        role="Machine Learning Engineer",
        mode="evaluate_answer",
        question="What is overfitting in machine learning?",
        candidate_answer=(
            "Overfitting happens when a model learns "
            "training data too well and performs poorly "
            "on unseen data."
        ),
        experience_level="Entry level"
    )

    print("\nFeedback:", answer_result.answer_feedback)
    print("\nImproved answer:", answer_result.improved_answer)
    print("\nStrengths:", answer_result.strengths)
    print("\nAreas to improve:", answer_result.areas_to_improve)
    print("\nFollow-up:", answer_result.follow_up_question)


if __name__ == "__main__":
    main()
