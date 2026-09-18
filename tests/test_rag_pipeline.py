from src.rag.rag_pipeline import EcoSynapseRAG


def main():

    query = (
        "The region has low forest cover and a high number of species "
        "at extinction risk. What should be done?"
    )

    risks = [
        "low_forest_cover",
        "high_extinction_risk"
    ]

    rag = EcoSynapseRAG()

    result = rag.build_prompt(
        query=query,
        risks=risks,
        top_k=5
    )

    print("\n=== REASONING ===")

    print(result["reasoning"]["interaction"])

    print("\nRecommended practices:")

    for practice in result["reasoning"]["recommended_practices"]:
        print("-", practice)

    print("\n=== RETRIEVED EVIDENCE ===")

    for i, (chunk, score) in enumerate(result["evidence"], 1):

        print(f"\nEvidence {i}")
        print("Score:", round(float(score), 4))
        print("Document:", chunk.get("document"))
        print("Page:", chunk.get("page"))
        print("Claim:", chunk.get("claim_type"))

    print("\n=== USER PROMPT ===")

    print(result["user_prompt"][:4000])


if __name__ == "__main__":
    main()