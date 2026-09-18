from src.reasoning.reasoning_engine import ReasoningEngine
from src.ingestion.retriever import retrieve

from .prompt import SYSTEM_PROMPT, build_user_prompt


class EcoSynapseRAG:

    def __init__(self):
        self.reasoning_engine = ReasoningEngine()

    # --------------------------------------------------
    # Evidence quality checks
    # --------------------------------------------------

    def _is_strong_evidence(self, chunk):

        text = chunk.get("text", "").strip()

        if len(text) < 150:
            return False

        lower_text = text.lower()

        weak_patterns = [
            "table of contents",
            "contents",
            "chapter contents",
            "list of contents",
            "acronyms",
            "abbreviations",
            "references",
            "bibliography",
            "document structure",
        ]

        if any(pattern in lower_text for pattern in weak_patterns):
            return False

        return True

    def _evidence_score(self, chunk, similarity):

        claim_type = chunk.get("claim_type", "")

        bonus = 0.0

        if claim_type == "practice_evidence":
            bonus += 0.08

        elif claim_type == "quantified":
            bonus += 0.05

        elif claim_type == "background":
            bonus += 0.0

        return float(similarity) + bonus

    # --------------------------------------------------
    # Retrieve scientific evidence
    # --------------------------------------------------

    def generate_evidence(self, risks, query, top_k=5):

        reasoning = self.reasoning_engine.analyze(risks)

        practices = reasoning.get(
            "recommended_practices",
            []
        )

        metrics = reasoning.get(
            "affected_metrics",
            []
        )

        # Build a retrieval query using the actual
        # environmental context + reasoning vocabulary.
        evidence_query = (
            query
            + " "
            + " ".join(practices)
            + " "
            + " ".join(metrics)
        )

        # Retrieve more candidates than we finally display.
        candidate_k = max(top_k + 8, 15)

        evidence = retrieve(
            query=evidence_query,
            top_k=candidate_k
        )

        strong_evidence = []

        for chunk, similarity in evidence:

            if not self._is_strong_evidence(chunk):
                continue

            score = self._evidence_score(
                chunk,
                similarity
            )

            strong_evidence.append(
                (chunk, similarity, score)
            )

        # Rank by semantic similarity + evidence quality.
        strong_evidence.sort(
            key=lambda item: item[2],
            reverse=True
        )

        final_evidence = [
            (chunk, similarity)
            for chunk, similarity, _ in strong_evidence[:top_k]
        ]

        return reasoning, final_evidence

    # --------------------------------------------------
    # Build RAG prompt
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Deterministic fallback
    # --------------------------------------------------

    def _build_fallback_answer(
        self,
        reasoning,
        evidence
    ):

        practices = reasoning.get(
            "recommended_practices",
            []
        )

        metrics = reasoning.get(
            "affected_metrics",
            []
        )

        reasoning_text = reasoning.get(
            "reasoning",
            ""
        )

        answer_parts = []

        # --------------------------------------------------
        # Recommendation
        # --------------------------------------------------

        if practices:

            practice_text = ", ".join(
                practice.replace("_", " ")
                for practice in practices
            )

            answer_parts.append(
                "### Recommendation\n"
                f"Consider the following practices: "
                f"{practice_text}."
            )

        # --------------------------------------------------
        # Why
        # --------------------------------------------------

        if reasoning_text:

            answer_parts.append(
                "### Why\n"
                f"{reasoning_text}"
            )

        # --------------------------------------------------
        # Impacted metrics
        # --------------------------------------------------

        if metrics:

            metric_text = ", ".join(
                metric.replace("_", " ")
                for metric in metrics
            )

            answer_parts.append(
                "### Impacted metrics\n"
                f"{metric_text}"
            )

        # --------------------------------------------------
        # Scientific evidence
        # --------------------------------------------------

        if evidence:

            evidence_lines = []

            for chunk, similarity in evidence:

                source = chunk.get(
                    "source",
                    "Unknown source"
                )

                document = chunk.get(
                    "document",
                    "Unknown document"
                )

                page = chunk.get(
                    "page",
                    "Unknown page"
                )

                text = chunk.get(
                    "text",
                    ""
                ).strip()

                # Keep the fallback readable.
                if len(text) > 650:

                    text = (
                        text[:650]
                        .rsplit(" ", 1)[0]
                        + "..."
                    )

                evidence_lines.append(
                    f"- **{source}, page {page}** "
                    f"({document}): {text}"
                )

            answer_parts.append(
                "### Scientific evidence\n"
                + "\n".join(evidence_lines)
            )

            answer_parts.append(
                "### Evidence limitation\n"
                "The language model is temporarily unavailable, "
                "so this response is generated directly from the "
                "EcoSynapse reasoning engine and retrieved scientific "
                "evidence. No additional claims have been generated "
                "beyond the available evidence."
            )

        else:

            answer_parts.append(
                "### Evidence limitation\n"
                "The EcoSynapse knowledge base did not return "
                "sufficient substantive scientific evidence to "
                "support a grounded recommendation."
            )

        return "\n\n".join(answer_parts)

    # --------------------------------------------------
    # Generate final answer
    # --------------------------------------------------

    def answer(
        self,
        query,
        risks,
        llm_callable
    ):

        package = self.build_prompt(
            query=query,
            risks=risks
        )

        if not package["evidence"]:

            return {
                "answer": (
                    "I don't have sufficient scientific evidence "
                    "in the knowledge base to support a recommendation."
                ),
                "reasoning": package["reasoning"],
                "evidence": []
            }

        try:

            answer = llm_callable(
                system_prompt=package["system_prompt"],
                user_prompt=package["user_prompt"]
            )

            # --------------------------------------------------
            # Gemini unavailable / quota exhausted
            # --------------------------------------------------

            if (
                not answer
                or "RESOURCE_EXHAUSTED" in answer
                or "API error:" in answer
                or "language model could not generate"
                in answer.lower()
                or "temporarily unavailable"
                in answer.lower()
            ):

                answer = self._build_fallback_answer(
                    reasoning=package["reasoning"],
                    evidence=package["evidence"]
                )

        except Exception:

            answer = self._build_fallback_answer(
                reasoning=package["reasoning"],
                evidence=package["evidence"]
            )

        return {
            "answer": answer,
            "reasoning": package["reasoning"],
            "evidence": package["evidence"]
        }