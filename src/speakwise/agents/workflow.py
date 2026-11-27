
from speakwise.agents.intent_classifier import classify_intent
from speakwise.agents.communication_planner import create_plan
from speakwise.agents.tool_executor import execute_plan

from speakwise.memory.conversation_memory import ConversationMemory
from speakwise.memory.context_manager import ContextManager

from speakwise.history.coaching_repository import save_interaction


# Shared memory instance for active sessions
memory = ConversationMemory()
context_manager = ContextManager(max_messages=10)


def process_request(
    user_input: str,
    session_id: str | None = None
):

    if not user_input or not user_input.strip():
        raise ValueError("User input cannot be empty")

    # Step 1: Create or retrieve session
    if session_id is None:
        session_id = memory.create_session()

    session = memory.get_session(session_id)

    if session is None:
        raise ValueError("Invalid session ID")

    # Step 2: Retrieve conversation history
    history = memory.get_history(session_id)

    conversation_context = context_manager.build_context(history)

    # Step 3: Store current user message
    memory.add_message(
        session_id,
        "user",
        user_input
    )

    # Step 4: Identify intent using conversation context
    intent = classify_intent(
        user_input=user_input,
        conversation_context=conversation_context
    )

    # Step 5: Generate context-aware plan
    plan = create_plan(
        user_input=user_input,
        intent=intent,
        conversation_context=conversation_context
    )


#########################################################################
    import logging

    logger = logging.getLogger(__name__)

    logger.info(
        "Session %s | Strategy: %s",
        session_id,
        plan.execution_strategy
    )

    for index, action in enumerate(plan.actions, start=1):
        logger.info(
            "Plan action %s: tool=%s, "
            "use_previous_output=%s, argument_keys=%s",
            index,
            action.tool_name,
            action.use_previous_output,
            list(action.arguments.model_dump().keys()),
        )
#############################################################################


    # Step 6: Execute selected tools
    execution = execute_plan(plan)

    # Step 7: Prepare assistant response
    if execution["status"] == "clarification_required":

        assistant_response = execution["message"]

    # elif execution["status"] == "success":

    #     assistant_response = "\n\n".join(
    #         str(item["output"].model_dump())
    #         for item in execution["results"]
    #     )
    ## For output formatting:

    elif execution["status"] == "success":

        response_parts = []

        for item in execution["results"]:

            tool_name = item["tool_name"]
            output = item["output"]

            # Convert Pydantic output to a dictionary
            if hasattr(output, "model_dump"):
                output = output.model_dump()

            # Grammar Tool
            if tool_name == "grammar_tool":

                corrected_text = output.get("corrected_text")

                if corrected_text:
                    response_parts.append(
                        "### Grammar correction\n"
                        f"> {corrected_text}"
                    )

            # Tone Tool
            elif tool_name == "tone_tool":

                improved_text = output.get("improved_text")
                explanation = output.get("explanation")

                if improved_text:
                    section = (
                        "### Improved message\n"
                        f"> {improved_text}"
                    )

                    if explanation:
                        section += f"\n\n{explanation}"

                    response_parts.append(section)

            # Scoring Tool
            elif tool_name == "scoring_tool":

                summary = output.get("evaluation_summary")

                if summary:
                    response_parts.append(
                        "### Evaluation summary\n"
                        f"{summary}"
                    )

        assistant_response = "\n\n".join(response_parts)


    else:
        assistant_response = execution["message"]

    # Step 8: Extract selected tools
    selected_tools = [
        action.tool_name
        for action in plan.actions
    ]

    # Step 9: Extract communication score, if available
    communication_score = None

    for result in execution.get("results", []):

        if result.get("tool_name") == "scoring_tool":

            output = result["output"]

            communication_score = (
                output.model_dump()
                if hasattr(output, "model_dump")
                else output
            )

            break

    # Step 10: Save coaching interaction to SQLite
    save_interaction(
        session_id=session_id,
        user_query=user_input,
        detected_intent=intent.intent,
        selected_tools=selected_tools,
        generated_response=assistant_response,
        communication_score=communication_score
    )

    # Step 11: Store assistant response in conversational memory
    memory.add_message(
        session_id,
        "assistant",
        assistant_response
    )

    # Step 12: Return workflow result
    return {
        "session_id": session_id,
        "intent": intent,
        "plan": plan,
        "execution": execution,
        "response": assistant_response
    }
