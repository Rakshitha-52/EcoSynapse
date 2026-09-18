"""
chunk_schema.py — the RAG chunk metadata schema from Phase 2.

Every chunk produced during ingestion (Phase 3) must be built through
ChunkMetadata so that bad tags (typos, off-vocabulary topics/metrics/
practices) are caught at ingestion time instead of silently breaking
retrieval later.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json

from vocab import (
    validate_topic,
    validate_metric,
    validate_practice,
    validate_claim_type,
    REGION_SCOPES,
)


@dataclass
class ChunkMetadata:
    chunk_id: str
    text: str
    source: str                # e.g. "FAO", "IPCC", "IPBES"
    document: str               # e.g. "Status of the World's Soil Resources 2026"
    year: int
    page: int
    topic: str                  # must be one of vocab.TOPICS
    metric: List[str] = field(default_factory=list)     # must be in vocab.METRICS
    practice: List[str] = field(default_factory=list)   # must be in vocab.PRACTICES
    region_scope: str = "global"    # one of vocab.REGION_SCOPES
    claim_type: str = "background"  # one of vocab.CLAIM_TYPES

    def __post_init__(self):
        errors = []

        if not validate_topic(self.topic):
            errors.append(f"Invalid topic '{self.topic}' — must be one of vocab.TOPICS")

        for m in self.metric:
            if not validate_metric(m):
                errors.append(f"Invalid metric '{m}' — must be one of vocab.METRICS")

        for p in self.practice:
            if not validate_practice(p):
                errors.append(f"Invalid practice '{p}' — must be one of vocab.PRACTICES")

        if self.region_scope not in REGION_SCOPES:
            errors.append(f"Invalid region_scope '{self.region_scope}' — must be one of {REGION_SCOPES}")

        if not validate_claim_type(self.claim_type):
            errors.append(f"Invalid claim_type '{self.claim_type}' — must be one of vocab.CLAIM_TYPES")

        if errors:
            raise ValueError(
                f"ChunkMetadata validation failed for chunk_id='{self.chunk_id}':\n  - "
                + "\n  - ".join(errors)
            )

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)


def load_chunks_from_jsonl(path: str) -> List[ChunkMetadata]:
    """Load and validate a batch of chunks from a JSONL file (one JSON object per line)."""
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                chunks.append(ChunkMetadata(**data))
            except (json.JSONDecodeError, TypeError, ValueError) as e:
                raise ValueError(f"Error on line {line_num} of {path}: {e}")
    return chunks


if __name__ == "__main__":
    # Example: a valid chunk from the FAO SWSR 2026 report
    example = ChunkMetadata(
        chunk_id="fao-swsr2026-p3-c2",
        text=(
            "Many SSM practices - including reduced tillage, integrated nutrient "
            "management, crop diversification, cover crops, organic amendments and "
            "agroforestry - can effectively mitigate soil threats while sustaining "
            "or improving agricultural productivity."
        ),
        source="FAO",
        document="Status of the World's Soil Resources 2026",
        year=2026,
        page=3,
        topic="soil_health",
        metric=["organic_carbon", "soil_erosion"],
        practice=["reduced_tillage", "crop_diversification", "cover_crops",
                  "organic_amendments", "agroforestry"],
        region_scope="global",
        claim_type="practice_evidence",
    )
    print("Valid chunk built successfully:")
    print(example.to_json())

    # Example of what happens with an invalid tag (uncomment to see it raise):
    # bad = ChunkMetadata(
    #     chunk_id="bad-example", text="...", source="X", document="Y",
    #     year=2026, page=1, topic="soil_healthy",  # typo -> will raise
    # )