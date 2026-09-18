import sys
sys.path.append("../schema")
from chunk_schema import ChunkMetadata

# Rough per-document tagging defaults — refine per-chunk as you go through
DOCUMENT_DEFAULTS = {
    "fao_swsr_2026.pdf": {
        "source": "FAO", "document": "Status of the World's Soil Resources 2026",
        "year": 2026, "topic": "soil_health",
    },
    "ipcc_ar6_wgii_technical_summary.pdf": {
        "source": "IPCC", "document": "AR6 WGII Technical Summary",
        "year": 2022, "topic": "climate",
    },
    "ipbes_global_assessment_spm.pdf": {
        "source": "IPBES", "document": "Global Assessment Summary for Policymakers",
        "year": 2019, "topic": "biodiversity",
    },
    "fao_land_use_statistics.pdf": {
        "source": "FAO", "document": "Land Use Statistics and Indicators (FAOSTAT Brief 28)",
        "year": 2021, "topic": "land_use",
    },
    "fao_plastics_pollution.pdf": {
        "source": "FAO", "document": "FAO Work on Plastics Management and Pollution",
        "year": 2023, "topic": "human_impact",
    },
}

def tag_chunk(filename: str, page: int, chunk_index: int, text: str,
              metric: list, practice: list = None,
              region_scope: str = "global", claim_type: str = "background") -> ChunkMetadata:
    defaults = DOCUMENT_DEFAULTS[filename]
    return ChunkMetadata(
        chunk_id=f"{filename.replace('.pdf','')}-p{page}-c{chunk_index}",
        text=text,
        source=defaults["source"],
        document=defaults["document"],
        year=defaults["year"],
        page=page,
        topic=defaults["topic"],
        metric=metric,
        practice=practice or [],
        region_scope=region_scope,
        claim_type=claim_type,
    )