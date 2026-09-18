from src.reasoning.reasoning_engine import ReasoningEngine
from src.ingestion.retriever import retrieve

from .prompt import SYSTEM_PROMPT, build_user_prompt


class EcoSynapseRAG:

    def __init__(self):
        self.reasoning_engine = ReasoningEngine()

    def generate_evidence(self, risks, query, top_k=5):

        # Generate multi-risk reasoning
        reasoning = self.reasoning_engine.analyze(risks)

        # Build a retrieval query using:
        # - original user query
        # - recommended practices
        # - affected environmental metrics
        evidence_query = (
            query
            + " "
            + " ".join(reasoning["recommended_practices"])
            + " "
            + " ".join(reasoning["affected_metrics"])
        )

        # Retrieve extra candidates so weak evidence can be filtered
        candidate_k = max(top_k + 3, 8)

        evidence = retrieve(
            query=evidence_query,
            top_k=candidate_k
        )

        # Filter weak or non-substantive evidence
        filtered_evidence = []

        for chunk, score in evidence:

            text = chunk.get("text", "").strip()

            # Ignore extremely short chunks
            if len(text) < 150:
                continue

            lower_text = text.lower()

            # Ignore obvious structural / non-evidence content
            weak_patterns = [
                "table of contents",
                "contents",
                "document title",
                "chapter contents",
            ]

            if any(pattern in lower_text for pattern in weak_patterns):
                continue

            filtered_evidence.append((chunk, score))

        # Keep only the strongest valid evidence
        evidence = filtered_evidence[:top_k]

        return reasoning, evidence

    def build_prompt(self, query, risks, top_k=5):

        reasoning, evidence = self.generate_evidence(
            risks=risks,
            query=query,
            top_k=top_k
        )

        user_prompt = build_user_prompt(
            query=query,
            reasoning=reasoning,
            evidence=evidence
        )

        return {
            "system_prompt": SYSTEM_PROMPT,
            "user_prompt": user_prompt,
            "reasoning": reasoning,
            "evidence": evidence
        }

    def answer(self, query, risks, llm_callable):

        package = self.build_prompt(
            query=query,
            risks=risks
        )

        # Do not generate an answer without scientific evidence
        if not package["evidence"]:

            return {
                "answer": (
                    "I don't have sufficient scientific evidence in "
                    "the knowledge base to support a recommendation."
                ),
                "reasoning": package["reasoning"],
                "evidence": []
            }

        # Generate grounded response using the LLM
        answer = llm_callable(
            system_prompt=package["system_prompt"],
            user_prompt=package["user_prompt"]
        )

        return {
            "answer": answer,
            "reasoning": package["reasoning"],
            "evidence": package["evidence"]
        }