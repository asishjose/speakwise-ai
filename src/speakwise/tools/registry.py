
from speakwise.tools.grammar_tool import correct_grammar
from speakwise.tools.tone_tool import improve_tone
from speakwise.tools.email_tool import generate_email
from speakwise.tools.interview_tool import conduct_interview
from speakwise.tools.conversation_tool import improve_conversation
from speakwise.tools.scoring_tool import evaluate_communication


TOOL_REGISTRY = {
    "grammar_tool": correct_grammar,
    "tone_tool": improve_tone,
    "email_tool": generate_email,
    "interview_tool": conduct_interview,
    "conversation_tool": improve_conversation,
    "scoring_tool": evaluate_communication,
}


def get_tool(tool_name: str):

    tool = TOOL_REGISTRY.get(tool_name)

    if tool is None:
        raise ValueError(f"Unknown tool: {tool_name}")

    return tool
