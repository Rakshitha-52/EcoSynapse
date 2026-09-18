from src.conversation.memory import ConversationMemory
from src.conversation.state_analyzer import detect_risks, needs_clarification


class ConversationManager:

    def __init__(self):
        self.memory = ConversationMemory()
        self.last_environmental_query = None

    def process(self, user_message):

        self.memory.update(user_message)

        current_state = self.memory.get_state()

        risks = detect_risks(current_state)

        clarification_needed, clarification_question = needs_clarification(
            current_state
        )

        # Detect whether this is a follow-up question.
        follow_up_phrases = [
            "what should i do",
            "what should we do",
            "what can i do",
            "what can we do",
            "what do you recommend",
            "how should i improve",
            "how can i improve",
            "what next",
            "what next?"
        ]

        normalized_message = user_message.lower().strip()

        is_follow_up = any(
            phrase in normalized_message
            for phrase in follow_up_phrases
        )

        # Preserve the previous environmental query for RAG retrieval.
        if not is_follow_up:
            self.last_environmental_query = user_message

        retrieval_query = self.last_environmental_query

        if is_follow_up and retrieval_query:
            retrieval_query = (
                retrieval_query
                + " "
                + user_message
            )

        return {
            "state": current_state,
            "risks": risks,
            "clarification_needed": clarification_needed,
            "clarification_question": clarification_question,
            "retrieval_query": retrieval_query,
            "is_follow_up": is_follow_up,
        }

    def reset(self):
        """Start a completely new environmental scenario."""

        self.memory = ConversationMemory()
        self.last_environmental_query = None