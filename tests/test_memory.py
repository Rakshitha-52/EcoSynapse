from src.conversation.memory import ConversationMemory


def main():

    memory = ConversationMemory()

    print("\n=== TURN 1 ===")

    memory.update(
        "My farm has low organic carbon."
    )

    print(memory.get_state())

    print("\n=== TURN 2 ===")

    memory.update(
        "It is located in Karnataka."
    )

    print(memory.get_state())

    print("\n=== TURN 3 ===")

    memory.update(
        "There is also high pesticide use and low forest cover."
    )

    print(memory.get_state())

    print("\n=== CONVERSATION HISTORY ===")

    for message in memory.get_history():
        print("-", message)


if __name__ == "__main__":
    main()