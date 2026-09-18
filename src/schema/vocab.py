"""
vocab.py — the single source of truth for controlled vocabularies.

Both the RAG ingestion pipeline (chunk tagging) and the reasoning engine
(risk flags, variable names) must import from here rather than hardcoding
strings. If you need a new tag, add it here first — never inline a new
topic/metric/practice string somewhere else in the codebase.
"""

# --- 1. Topic / pillar tags (fixed at 5, matching the challenge brief) ---
TOPICS = [
    "soil_health",
    "land_use",
    "biodiversity",
    "climate",
    "human_impact",
]

# --- 2. Metric vocabulary ---
# Each metric is tagged with whether we have structured (CSV) data for it,
# or it's RAG-only (evidence exists in documents, but no tabular column).
METRICS = {
    # soil_health
    "organic_carbon":         {"pillar": "soil_health", "structured": False},
    "soil_ph":                {"pillar": "soil_health", "structured": False},
    "soil_erosion":           {"pillar": "soil_health", "structured": False},

    # land_use
    "agricultural_pct":       {"pillar": "land_use", "structured": True},
    "forest_pct":             {"pillar": "land_use", "structured": True},

    # biodiversity
    "species_count":            {"pillar": "biodiversity", "structured": True},
    "endemic_count":             {"pillar": "biodiversity", "structured": True},
    "extinction_risk_count":      {"pillar": "biodiversity", "structured": True},
    "regional_species_richness":  {"pillar": "biodiversity", "structured": True},

    # climate
    "rainfall":                {"pillar": "climate", "structured": False},
    "temperature":             {"pillar": "climate", "structured": False},
    "disaster_count":          {"pillar": "climate", "structured": True},
    "freshwater_pc":           {"pillar": "climate", "structured": True},

    # human_impact
    "pesticide_intensity":    {"pillar": "human_impact", "structured": True},
    "co2_landuse":            {"pillar": "human_impact", "structured": True},
    "co2_fossil":             {"pillar": "human_impact", "structured": True},
    "ghg_transport":          {"pillar": "human_impact", "structured": True},
    "hazardous_waste":        {"pillar": "human_impact", "structured": True},
    "so2_pc":                 {"pillar": "human_impact", "structured": True},
    "nox_pc":                 {"pillar": "human_impact", "structured": True},
}

# --- 3. Practice / intervention vocabulary ---
# What the system is allowed to recommend. Add a practice here only once
# you have at least one RAG chunk with quantified evidence for it.
PRACTICES = [
    "cover_crops",
    "agroforestry",
    "intercropping",
    "reduced_tillage",
    "buffer_strips",
    "native_reforestation",
    "integrated_nutrient_management",
    "crop_diversification",
    "organic_amendments",
]

# --- 4. Claim types for RAG chunks ---
# background     = general context, no specific number
# quantified      = has a specific stat, not necessarily tied to a practice
# practice_evidence = ties a named intervention to a measurable outcome
CLAIM_TYPES = ["background", "quantified", "practice_evidence"]

# --- 5. Region scope for RAG chunks ---
REGION_SCOPES = ["global", "regional", "country"]


def validate_topic(topic: str) -> bool:
    return topic in TOPICS


def validate_metric(metric: str) -> bool:
    return metric in METRICS


def validate_practice(practice: str) -> bool:
    return practice in PRACTICES


def validate_claim_type(claim_type: str) -> bool:
    return claim_type in CLAIM_TYPES


def metrics_for_pillar(pillar: str) -> list:
    """Return all metric names belonging to a given topic/pillar."""
    return [m for m, meta in METRICS.items() if meta["pillar"] == pillar]


def structured_metrics() -> list:
    """Return metric names that have a column in the structured CSV data."""
    return [m for m, meta in METRICS.items() if meta["structured"]]


def rag_only_metrics() -> list:
    """Return metric names that only exist as RAG evidence (no CSV column)."""
    return [m for m, meta in METRICS.items() if not meta["structured"]]


if __name__ == "__main__":
    # quick self-check when run directly
    print(f"{len(TOPICS)} topics, {len(METRICS)} metrics, {len(PRACTICES)} practices")
    print("RAG-only metrics (no structured data yet):", rag_only_metrics())