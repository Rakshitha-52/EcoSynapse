from src.conversation.memory import ConversationMemory
from src.conversation.state_analyzer import detect_risks, needs_clarification


class ConversationManager:
    def __init__(self):
        self.memory = ConversationMemory()

    def process(self, user_message):
        # Update conversation memory
        self.memory.update(user_message)

        # Get the updated state
        current_state = self.memory.get_state()

        # Detect risks from current state
        risks = detect_risks(current_state)

        clarification_needed, clarification_question = needs_clarification(
            current_state
        )

        return {
            "state": current_state,
            "risks": risks,
            "clarification_needed": clarification_needed,
            "clarification_question": clarification_question,
        }

    def reset(self):
        """Start a completely new environmental scenario."""
        self.memory = ConversationMemory()