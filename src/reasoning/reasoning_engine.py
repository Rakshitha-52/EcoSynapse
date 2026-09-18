"""
EcoSynapse reasoning engine.

Combines detected environmental risks using:
1. Individual causal chains
2. Multi-risk interaction rules
"""

from .causal_chains import CAUSAL_CHAINS
from .risk_combination import get_combination


class ReasoningEngine:

    def analyze(self, risks):
        """
        Generate a structured reasoning plan from detected risks.

        Parameters
        ----------
        risks : list[str]
            Detected environmental risks.

        Returns
        -------
        dict
            Structured reasoning result.
        """

        risks = list(dict.fromkeys(risks))

        if not risks:
            return {
                "risks": [],
                "causal_chains": [],
                "interaction": None,
                "recommended_practices": [],
                "affected_metrics": [],
                "reasoning": []
            }

        causal_chains = []

        for risk in risks:

            chain = CAUSAL_CHAINS.get(risk)

            if chain:
                causal_chains.append({
                    "risk": risk,
                    "trigger": chain["trigger"],
                    "mechanism": chain["mechanism"],
                    "affected_metrics": chain["affected_metrics"],
                    "practices": chain["practices"]
                })

        combination = get_combination(risks)

        practices = set()
        metrics = set()
        reasoning = []

        # Add individual risk information
        for chain in causal_chains:

            practices.update(chain["practices"])
            metrics.update(chain["affected_metrics"])
            reasoning.extend(chain["mechanism"])

        # Add multi-risk interaction
        interaction = None

        if combination:

            interaction = combination["interaction"]

            reasoning.extend(combination["reasoning"])

            practices.update(
                combination["recommended_practices"]
            )

            metrics.update(
                combination["affected_metrics"]
            )

        return {
            "risks": risks,
            "causal_chains": causal_chains,
            "interaction": interaction,
            "recommended_practices": sorted(practices),
            "affected_metrics": sorted(metrics),
            "reasoning": reasoning
        }


if __name__ == "__main__":

    engine = ReasoningEngine()

    result = engine.analyze([
        "low_forest_cover",
        "high_extinction_risk"
    ])

    print("\n=== EcoSynapse Reasoning Test ===\n")

    print("Risks:")
    for risk in result["risks"]:
        print("-", risk)

    print("\nInteraction:")
    print(result["interaction"])

    print("\nRecommended practices:")
    for practice in result["recommended_practices"]:
        print("-", practice)

    print("\nAffected metrics:")
    for metric in result["affected_metrics"]:
        print("-", metric)

    print("\nReasoning:")
    for step in result["reasoning"]:
        print("-", step)