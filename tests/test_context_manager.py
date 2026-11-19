
from speakwise.memory.conversation_memory import ConversationMemory
from speakwise.memory.context_manager import ContextManager


def main():

    memory = ConversationMemory(max_messages=20)

    session_id = memory.create_session()

    # Add six messages
    memory.add_message(session_id, "user", "Message 1")
    memory.add_message(session_id, "assistant", "Response 1")

    memory.add_message(session_id, "user", "Message 2")
    memory.add_message(session_id, "assistant", "Response 2")

    memory.add_message(session_id, "user", "Message 3")
    memory.add_message(session_id, "assistant", "Response 3")

    # Retrieve complete history
    history = memory.get_history(session_id)

    # Select only the latest four messages
    context_manager = ContextManager(max_messages=4)

    context = context_manager.build_context(history)

    print("\nComplete messages:", len(history))
    print("Context:\n")
    print(context)

    assert "Message 1" not in context
    assert "Response 1" not in context
    assert "Message 2" in context
    assert "Response 3" in context

    print("\nContext window test passed!")


if __name__ == "__main__":
    main()
