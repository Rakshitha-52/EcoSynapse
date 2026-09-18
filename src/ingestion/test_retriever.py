"""
test_retriever.py — runs the risk_query_map.json entries as literal test
queries against the built FAISS index, so retrieval quality is checked
before Phase 4 exists to generate these queries automatically.

Run directly:
    python3 test_retriever.py
"""

import json
from pathlib import Path

from retriever import retrieve

RISK_QUERY_MAP_PATH = Path(__file__).resolve().parent.parent / "schema" / "risk_query_map.json"


def load_test_cases_from_risk_map(path: Path) -> list[tuple]:
    """
    Turn every entry in risk_query_map.json into a (label, query, topics,
    metrics, practices) test case, so the test suite stays in sync with
    the actual risk map instead of hardcoding a separate copy of it.
    """
    with open(path, "r", encoding="utf-8") as f:
        risk_map = json.load(f)

    cases = []
    for risk_label, spec in risk_map.items():
        if risk_label.startswith("_"):
            continue  # skip _comment or other non-risk keys
        cases.append((
            risk_label,
            spec["query"],
            spec.get("topic_filter"),
            spec.get("metric_filter"),
            spec.get("practice_filter"),
        ))
    return cases


def run_test_cases(cases: list[tuple]) -> dict:
    """Runs every case, prints results, and returns a pass/fail summary."""
    summary = {}

    for risk_label, query, topics, metrics, practices in cases:
        print("=" * 80)
        print(f"RISK: {risk_label}")
        print(f"QUERY: {query}")
        print("-" * 80)

        results = retrieve(query, topic_filter=topics, metric_filter=metrics,
                            practice_filter=practices, top_k=5)

        if not results:
            print("  ⚠️  NO RESULTS — evidence gap for this risk flag.")
            summary[risk_label] = "EMPTY"
            continue

        has_practice_evidence = any(c["claim_type"] == "practice_evidence" for c, _ in results)

        for chunk, score in results:
            flag = "✅" if chunk["claim_type"] == "practice_evidence" else "  "
            print(f"  {flag} [{score:.3f}] {chunk['chunk_id']} ({chunk['claim_type']})")
            print(f"       {chunk['text'][:120]}...")

        summary[risk_label] = "OK (has practice_evidence)" if has_practice_evidence else "WEAK (no practice_evidence found)"
        print()

    return summary


def print_summary(summary: dict):
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    for risk_label, status in summary.items():
        marker = "✅" if status.startswith("OK") else ("⚠️ " if status.startswith("WEAK") else "❌")
        print(f"  {marker} {risk_label:<30} {status}")

    empty_or_weak = [k for k, v in summary.items() if not v.startswith("OK")]
    if empty_or_weak:
        print(f"\n{len(empty_or_weak)} risk flag(s) need attention before Phase 4: {empty_or_weak}")
        print("These are real evidence gaps — document them in your README as known limitations")
        print("rather than discovering them live during a demo.")
    else:
        print("\nAll risk flags have supporting practice_evidence. Ready for Phase 4.")


if __name__ == "__main__":
    test_cases = load_test_cases_from_risk_map(RISK_QUERY_MAP_PATH)
    print(f"Running {len(test_cases)} test case(s) from risk_query_map.json...\n")
    summary = run_test_cases(test_cases)
    print_summary(summary)