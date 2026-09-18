from src.rag.rag_pipeline import EcoSynapseRAG
from src.rag.llm import GeminiLLM


def main():

    query = (
        "The region has low forest cover and a high number of "
        "species at extinction risk. What should be done?"
    )

    risks = [
        "low_forest_cover",
        "high_extinction_risk"
    ]

    print("\nInitializing EcoSynapse RAG...")

    rag = EcoSynapseRAG()
    llm = GeminiLLM()

    print("Generating grounded response...\n")

    result = rag.answer(
        query=query,
        risks=risks,
        llm_callable=llm.generate
    )

    print("=" * 60)
    print("ECOSYNAPSE RESPONSE")
    print("=" * 60)

    print(result["answer"])

    print("\n" + "=" * 60)
    print("RETRIEVED SOURCES")
    print("=" * 60)

    for i, (chunk, score) in enumerate(result["evidence"], 1):

        print(
            f"{i}. {chunk.get('document')} "
            f"(page {chunk.get('page')}) "
            f"[score={float(score):.4f}]"
        )


if __name__ == "__main__":
    main()