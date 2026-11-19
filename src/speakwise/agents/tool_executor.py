
from concurrent.futures import ThreadPoolExecutor
from inspect import signature

from speakwise.tools.registry import get_tool


# Text fields produced by each tool
OUTPUT_FIELDS = {
    "grammar_tool": "corrected_text",
    "tone_tool": "improved_text",
    "email_tool": "body",
    "interview_tool": "improved_answer",
    "conversation_tool": "improved_response",
    "scoring_tool": "evaluation_summary",
}

# Input fields that can receive a previous tool's output
INPUT_FIELDS = {
    "grammar_tool": "user_input",
    "tone_tool": "user_input",
    "email_tool": "context",
    "interview_tool": "candidate_answer",
    "conversation_tool": "original_response",
    "scoring_tool": "user_input",
}


def _execute_action(action, previous_result=None):

    tool = get_tool(action.tool_name)

    arguments = dict(action.arguments)

    # Pass the previous result to the next dependent tool
    if action.use_previous_output:

        if previous_result is None:
            raise ValueError(
                "Previous tool output is required but unavailable"
            )

        output_field = OUTPUT_FIELDS.get(
            action.tool_name
        )

        input_field = INPUT_FIELDS.get(
            action.tool_name
        )

        if not output_field or not input_field:
            raise ValueError(
                f"Sequential input mapping not configured for "
                f"{action.tool_name}"
            )

        previous_text = getattr(
            previous_result,
            output_field,
            None
        )

        if not previous_text:
            raise ValueError(
                "Previous tool did not produce usable text"
            )

        arguments[input_field] = previous_text

    # Validate required function arguments before execution
    tool_signature = signature(tool)

    required_arguments = {
        name
        for name, parameter in tool_signature.parameters.items()
        if parameter.default == parameter.empty
    }

    missing_arguments = required_arguments - arguments.keys()

    if missing_arguments:
        raise ValueError(
            f"Missing arguments for {action.tool_name}: "
            f"{', '.join(sorted(missing_arguments))}"
        )

    # Ignore any arguments that the function does not accept
    valid_arguments = {
        key: value
        for key, value in arguments.items()
        if key in tool_signature.parameters
    }

    return tool(**valid_arguments)


def execute_plan(plan):

    if plan.needs_clarification:
        return {
            "status": "clarification_required",
            "message": plan.clarification_question,
            "results": []
        }

    if not plan.actions:
        return {
            "status": "no_action",
            "message": "No communication tool was selected.",
            "results": []
        }

    results = []

    # Single tool execution
    if plan.execution_strategy == "single":

        result = _execute_action(plan.actions[0])

        results.append({
            "tool_name": plan.actions[0].tool_name,
            "output": result
        })

    # Independent tools can execute simultaneously
    elif plan.execution_strategy == "parallel":

        with ThreadPoolExecutor(
            max_workers=len(plan.actions)
        ) as executor:

            futures = [
                executor.submit(_execute_action, action)
                for action in plan.actions
            ]

            for action, future in zip(plan.actions, futures):

                result = future.result()

                results.append({
                    "tool_name": action.tool_name,
                    "output": result
                })

    # Dependent tools execute one after another
    elif plan.execution_strategy == "sequential":

        previous_result = None

        for action in plan.actions:

            result = _execute_action(
                action,
                previous_result=previous_result
            )

            results.append({
                "tool_name": action.tool_name,
                "output": result
            })

            previous_result = result

    else:
        raise ValueError(
            f"Unsupported execution strategy: "
            f"{plan.execution_strategy}"
        )

    return {
        "status": "success",
        "message": "Communication task completed successfully.",
        "results": results
    }
