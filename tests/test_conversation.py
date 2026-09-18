from src.conversation.conversation_manager import ConversationManager


def main():

    conversation = ConversationManager()

    messages = [
        "My farm has low organic carbon.",
        "It is located in Karnataka.",
        "There is also high pesticide use.",
        "The area has low forest cover."
    ]

    for i, message in enumerate(messages, 1):

        print(f"\n=== TURN {i} ===")
        print("User:", message)

        result = conversation.process(message)

        print("\nRemembered state:")
        print(result["state"])

        print("\nDetected risks:")
        print(result["risks"])

        if result["clarification_needed"]:
            print("\nClarification:")
            print(result["clarification_question"])


if __name__ == "__main__":
    main()