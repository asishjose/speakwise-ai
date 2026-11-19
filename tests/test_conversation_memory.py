
from speakwise.memory.conversation_memory import ConversationMemory


def main():

    memory = ConversationMemory()

    # Create a session
    session_id = memory.create_session()

    print("Session ID:", session_id)

    # Add conversation messages
    memory.add_message(
        session_id,
        "user",
        "Write an email requesting leave."
    )

    memory.add_message(
        session_id,
        "assistant",
        "Subject: Leave Request\nDear Manager..."
    )

    memory.add_message(
        session_id,
        "user",
        "Make it more formal."
    )

    # Retrieve conversation history
    history = memory.get_history(session_id)

    print("\nConversation History:")

    for message in history:
        print(f"{message.role}: {message.content}")

    print("\nTotal messages:", len(history))


if __name__ == "__main__":
    main()
