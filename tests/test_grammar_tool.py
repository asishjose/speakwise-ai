
from speakwise.tools.grammar_tool import correct_grammar


def main():
    text = "He don't knows how to communicating properly."

    result = correct_grammar(text)

    print("\nOriginal:")
    print(result.original_text)

    print("\nCorrected:")
    print(result.corrected_text)

    print("\nErrors:")
    for error in result.errors_found:
        print("-", error)

    print("\nExplanations:")
    for explanation in result.explanations:
        print("-", explanation)

    print("\nHas errors:", result.has_errors)


if __name__ == "__main__":
    main()
