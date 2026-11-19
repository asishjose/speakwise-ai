
from speakwise.agents.workflow import process_request
from speakwise.history.coaching_repository import get_session_history


# First interaction: Create a new session
first = process_request(
    "Correct the grammar: She don't like coffee."
)

session_id = first["session_id"]

print("Session ID:", session_id)


# Second interaction: Continue the same session
second = process_request(
    "Make it sound more professional.",
    session_id=session_id
)


# Retrieve complete session history
history = get_session_history(session_id)

print("\nTotal interactions:", len(history))

for item in history:
    print("\nQuery:", item["user_query"])
    print("Intent:", item["detected_intent"])
    print("Tools:", item["selected_tools"])
    print("Response:", item["generated_response"])
