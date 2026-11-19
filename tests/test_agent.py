
from speakwise.agents.workflow import process_request


def main():

    user_input = (
        "Correct the grammar in this sentence: "
        "She don't like coffee."
    )

    result = process_request(user_input)

    print("\n========== INTENT ==========")
    print(result["intent"].model_dump_json(indent=2))

    print("\n========== PLAN ==========")
    print(result["plan"].model_dump_json(indent=2))

    print("\n========== EXECUTION ==========")

    execution = result["execution"]

    print("Status:", execution["status"])
    print("Message:", execution["message"])

    for item in execution["results"]:

        print("\nTool:", item["tool_name"])

        output = item["output"]

        if hasattr(output, "model_dump_json"):
            print(output.model_dump_json(indent=2))
        else:
            print(output)


if __name__ == "__main__":
    main()
