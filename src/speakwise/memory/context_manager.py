
from speakwise.memory.conversation_memory import ConversationMessage


class ContextManager:

    def __init__(self, max_messages: int = 10):

        if max_messages < 1:
            raise ValueError("max_messages must be at least 1")

        self.max_messages = max_messages

    def build_context(
        self,
        messages: list[ConversationMessage]
    ) -> str:

        # Select the most recent messages
        recent_messages = messages[-self.max_messages:]

        context = []

        for message in recent_messages:

            role = message.role.upper()

            context.append(
                f"{role}: {message.content}"
            )

        return "\n\n".join(context)
