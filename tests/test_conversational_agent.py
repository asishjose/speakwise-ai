
from speakwise.agents.workflow import process_request


def main():

    session_id = None

    # First interaction
    print("\n========== INTERACTION 1 ==========")

    result1 = process_request(
        user_input="Write an email to my manager requesting two days of leave.",
        session_id=session_id
    )

    session_id = result1["session_id"]

    print("Session ID:", session_id)
    print("Intent:", result1["intent"].intent)
    print("Plan:", result1["plan"].model_dump_json(indent=2))
    print("Response:", result1["response"])

    # Second interaction: Follow-up
    print("\n========== INTERACTION 2 ==========")

    result2 = process_request(
        user_input="Make it more formal.",
        session_id=session_id
    )

    print("Session ID:", result2["session_id"])
    print("Intent:", result2["intent"].intent)
    print("Plan:", result2["plan"].model_dump_json(indent=2))
    print("Response:", result2["response"])

    # Verify session continuity
    assert result1["session_id"] == result2["session_id"]

    print("\nSession continuity verified!")



# if __name__ == "__main__":
#     main()



from speakwise.memory.conversation_memory import ConversationMemory


def test_session_isolation():

    memory = ConversationMemory()

    # Create two independent sessions
    session_a = memory.create_session()
    session_b = memory.create_session()

    # User A's conversation
    memory.add_message(
        session_a,
        "user",
        "Write an email requesting leave."
    )

    memory.add_message(
        session_a,
        "assistant",
        "Here is your leave request email."
    )

    # User B's conversation
    memory.add_message(
        session_b,
        "user",
        "Help me prepare for a Python interview."
    )

    memory.add_message(
        session_b,
        "assistant",
        "Let's start with Python fundamentals."
    )

    # Retrieve both histories
    history_a = memory.get_history(session_a)
    history_b = memory.get_history(session_b)

    # Verify session IDs are different
    assert session_a != session_b

    # Verify message counts
    assert len(history_a) == 2
    assert len(history_b) == 2

    # Verify User A's messages
    assert history_a[0].content == "Write an email requesting leave."
    assert history_a[1].content == "Here is your leave request email."

    # Verify User B's messages
    assert history_b[0].content == "Help me prepare for a Python interview."
    assert history_b[1].content == "Let's start with Python fundamentals."

    # Verify no cross-session contamination
    assert all(
        "interview" not in message.content.lower()
        for message in history_a
    )

    assert all(
        "email" not in message.content.lower()
        for message in history_b
    )

    print("Session isolation verified successfully!")


if __name__ == "__main__":
    test_session_isolation()
