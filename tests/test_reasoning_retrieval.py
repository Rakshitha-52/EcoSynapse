from src.reasoning.reasoning_engine import ReasoningEngine
from src.ingestion.retriever import retrieve


def main():

    risks = [
        "low_forest_cover",
        "high_extinction_risk"
    ]

    # 1. Multi-metric reasoning
    engine = ReasoningEngine()
    reasoning = engine.analyze(risks)

    print("\n=== REASONING ===")

    print("Risks:")
    for risk in reasoning["risks"]:
        print("-", risk)

    print("\nInteraction:")
    print(reasoning["interaction"])

    print("\nPractices:")
    for practice in reasoning["recommended_practices"]:
        print("-", practice)

    print("\nMetrics:")
    for metric in reasoning["affected_metrics"]:
        print("-", metric)

    # 2. Build a scientific evidence query
    query = (
        " ".join(risks)
        + " "
        + " ".join(reasoning["recommended_practices"])
        + " biodiversity habitat restoration ecological connectivity"
    )

    print("\n=== EVIDENCE QUERY ===")
    print(query)

    # 3. Retrieve scientific evidence
    results = retrieve(
        query=query,
        top_k=5
    )

    print("\n=== SCIENTIFIC EVIDENCE ===")

    if not results:
        print("No evidence retrieved.")
        return

    for i, (chunk, score) in enumerate(results, 1):

        print(f"\n--- Evidence {i} ---")

        print("Score:", round(float(score), 4))
        print("Document:", chunk.get("document"))
        print("Page:", chunk.get("page"))
        print("Topic:", chunk.get("topic"))
        print("Claim type:", chunk.get("claim_type"))

        print("Text:")
        print(chunk.get("text", "")[:500])


if __name__ == "__main__":
    main()