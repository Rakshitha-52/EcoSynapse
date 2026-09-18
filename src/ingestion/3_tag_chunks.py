"""
03_tag_chunks.py

Loads chunks created by 02_chunk_documents.py,
assigns Phase 2 metadata, validates each chunk using
ChunkMetadata, and saves:

    index/chunk_metadata.jsonl
"""

import json
import re
import sys
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

INDEX_DIR = PROJECT_ROOT / "index"

CHUNKS_PATH = INDEX_DIR / "chunks.jsonl"
OUTPUT_PATH = INDEX_DIR / "chunk_metadata.jsonl"

SCHEMA_DIR = PROJECT_ROOT / "src" / "schema"

sys.path.insert(0, str(SCHEMA_DIR))

from chunk_schema import ChunkMetadata


# ============================================================
# DOCUMENT INFORMATION
# ============================================================

DOCUMENT_INFO = {

    "FAO_Climate_Smart_Agriculture_Soil_Management.pdf": {
        "source": "FAO",
        "document": "Climate Smart Agriculture Soil Management",
        "year": 2026,
    },

    "FAO_Global_Soil_Organic_Carbon_Map_GSOCmap_2022.pdf": {
        "source": "FAO",
        "document": "Global Soil Organic Carbon Map GSOCmap",
        "year": 2022,
    },

    "FAO_Soil_Organic_Carbon_Conservation_Agriculture_2012.pdf": {
        "source": "FAO",
        "document": "Soil Organic Carbon and Conservation Agriculture",
        "year": 2012,
    },

    "FAO_Status_World_Soil_Resources_2026.pdf": {
        "source": "FAO",
        "document": "Status of the World's Soil Resources 2026",
        "year": 2026,
    },

    "FAO_Status_World_Soil_Resources_2025_Asia.pdf": {
        "source": "FAO",
        "document": "Status of the World's Soil Resources 2025 Asia",
        "year": 2025,
    },

    "FAO_Land_Use_Statistics_Indicators_1990_2019.pdf": {
        "source": "FAO",
        "document": "Land Use Statistics and Indicators",
        "year": 2021,
    },

    "FAO_Agricultural_Plastics_Pollution_Management.pdf": {
        "source": "FAO",
        "document": "Agricultural Plastics Pollution Management",
        "year": 2023,
    },

    "IPCC_AR6_WGII_Technical_Summary_2022.pdf": {
        "source": "IPCC",
        "document": "AR6 WGII Technical Summary",
        "year": 2022,
    },

    "IPBES_Global_Assessment_Biodiversity_Ecosystem_Services_2019.pdf": {
        "source": "IPBES",
        "document": "Global Assessment of Biodiversity and Ecosystem Services",
        "year": 2019,
    },

    "UNEP_Loss_and_Damage_Climate_Change_Ecosystems_2016.pdf": {
        "source": "UNEP",
        "document": "Loss and Damage, Climate Change and Ecosystems",
        "year": 2016,
    },

    "UNEP_Land_Degradation_Drought_Resilience_Technical_Note_2024.pdf": {
        "source": "UNEP",
        "document": "Land Degradation, Drought and Resilience",
        "year": 2024,
    },

    "UNCCD_Land_in_Numbers_Livelihoods.pdf": {
        "source": "UNCCD",
        "document": "Land in Numbers: Livelihoods",
        "year": 2022,
    },

    "Andrieu_2023_Western_Ghats_Plant_Occurrence_Datasets.pdf": {
        "source": "Andrieu et al.",
        "document": "Western Ghats Plant Occurrence Datasets",
        "year": 2023,
    },

    "Biodiversity_Western_Ghats_Regional_Reference.pdf": {
        "source": "Regional Reference",
        "document": "Biodiversity Western Ghats Regional Reference",
        "year": 2023,
    },

    "NRSC_Karnataka_LULC_Atlas.pdf": {
        "source": "NRSC",
        "document": "Karnataka Land Use Land Cover Atlas",
        "year": 2025,
    },

    "NRSC_Annual_LULC_Atlas_India_2024.pdf": {
        "source": "NRSC",
        "document": "Annual Land Use Land Cover Atlas India",
        "year": 2024,
    },

    "NRSC_Annual_LULC_Technical_Document_2025.pdf": {
        "source": "NRSC",
        "document": "Annual Land Use Land Cover Technical Document",
        "year": 2025,
    },

    "IMD_State_Rainfall_Distribution_2026.pdf.pdf": {
        "source": "IMD",
        "document": "State Rainfall Distribution",
        "year": 2026,
    },

    "IMD_District_Rainfall_Distribution_2026.pdf.pdf": {
        "source": "IMD",
        "document": "District Rainfall Distribution",
        "year": 2026,
    },
}


# ============================================================
# PILLAR → TOPIC
# ============================================================

PILLAR_TO_TOPIC = {
    "soil": "soil_health",
    "land_and_ecosystems": "land_use",
    "biodiversity": "biodiversity",
    "climate_and_risks": "climate",
    "pollution": "human_impact",
    "scientific_reports": None,
}


# ============================================================
# KEYWORD RULES
# ============================================================

METRIC_KEYWORDS = {

    "organic_carbon": [
        "soil organic carbon",
        "organic carbon",
        "soil carbon",
        "carbon stock",
    ],

    "soil_ph": [
        "soil ph",
        "soil pH",
        "acidity",
        "alkalinity",
    ],

    "soil_erosion": [
        "soil erosion",
        "erosion",
        "soil loss",
    ],

    "agricultural_pct": [
        "agricultural land",
        "cropland",
        "agriculture area",
    ],

    "forest_pct": [
        "forest cover",
        "forest area",
        "forest land",
        "forested",
        "deforestation",
    ],

    "species_count": [
        "species richness",
        "number of species",
        "species diversity",
        "species count",
    ],

    "endemic_count": [
        "endemic species",
        "endemism",
    ],

    "extinction_risk_count": [
        "threatened species",
        "endangered species",
        "extinction risk",
        "extinction",
    ],

    "regional_species_richness": [
        "species richness",
        "biodiversity richness",
    ],

    "rainfall": [
        "rainfall",
        "precipitation",
        "rainfall distribution",
    ],

    "temperature": [
        "temperature",
        "warming",
        "heat",
    ],

    "disaster_count": [
        "climate disaster",
        "climatological disaster",
        "hydrological disaster",
        "flood",
        "drought",
    ],

    "freshwater_pc": [
        "freshwater",
        "water availability",
        "water resources",
        "renewable freshwater",
    ],

    "pesticide_intensity": [
        "pesticide",
        "pesticides",
        "pesticide use",
        "pesticide intensity",
    ],

    "co2_landuse": [
        "land use emissions",
        "land-use emissions",
        "land use change emissions",
    ],

    "ghg_transport": [
        "transport emissions",
        "transportation emissions",
        "transport sector",
    ],

    "hazardous_waste": [
        "hazardous waste",
        "hazardous wastes",
    ],

    "so2_pc": [
        "sulfur dioxide",
        "sulphur dioxide",
        "so2",
    ],

    "nox_pc": [
        "nitrogen oxides",
        "nitrogen oxide",
        "nox",
    ],
}


PRACTICE_KEYWORDS = {

    "cover_crops": [
        "cover crop",
        "cover crops",
    ],

    "agroforestry": [
        "agroforestry",
    ],

    "intercropping": [
        "intercropping",
        "intercrop",
    ],

    "reduced_tillage": [
        "reduced tillage",
        "minimum tillage",
        "conservation tillage",
        "no till",
        "no-till",
    ],

    "buffer_strips": [
        "buffer strip",
        "buffer strips",
        "riparian buffer",
    ],

    "native_reforestation": [
        "reforestation",
        "native reforestation",
        "forest restoration",
        "habitat restoration",
    ],

    "integrated_nutrient_management": [
        "integrated nutrient management",
        "integrated pest management",
        "ipm",
    ],

    "crop_diversification": [
        "crop diversification",
        "diversified cropping",
    ],

    "organic_amendments": [
        "organic amendment",
        "organic amendments",
        "compost",
        "manure",
    ],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def contains_keyword(text, keyword):
    return keyword.lower() in text.lower()


def detect_metrics(text):

    found = []

    for metric, keywords in METRIC_KEYWORDS.items():

        if any(contains_keyword(text, keyword) for keyword in keywords):
            found.append(metric)

    return found


def detect_practices(text):

    found = []

    for practice, keywords in PRACTICE_KEYWORDS.items():

        if any(contains_keyword(text, keyword) for keyword in keywords):
            found.append(practice)

    return found


def detect_claim_type(text, practices):

    # Quantified claims contain numbers, percentages,
    # measurements, ranges, etc.
    has_number = bool(
        re.search(r"\b\d+(?:\.\d+)?\b", text)
    )

    if practices and has_number:
        return "practice_evidence"

    if practices:
        return "practice_evidence"

    if has_number:
        return "quantified"

    return "background"


def detect_topic(chunk):

    pillar = chunk.get("pillar_folder")

    topic = PILLAR_TO_TOPIC.get(pillar)

    if topic:
        return topic

    text = chunk["text"].lower()

    # Scientific reports are mixed, so inspect the text.
    if any(
        word in text
        for word in ["soil organic carbon", "soil health", "soil erosion"]
    ):
        return "soil_health"

    if any(
        word in text
        for word in ["forest cover", "land use", "land cover"]
    ):
        return "land_use"

    if any(
        word in text
        for word in ["species richness", "biodiversity", "ecosystem"]
    ):
        return "biodiversity"

    if any(
        word in text
        for word in ["climate change", "temperature", "rainfall", "drought"]
    ):
        return "climate"

    return "human_impact"


def get_document_info(source_pdf):

    if source_pdf in DOCUMENT_INFO:
        return DOCUMENT_INFO[source_pdf]

    # Safe fallback
    return {
        "source": "Unknown",
        "document": Path(source_pdf).stem,
        "year": 2026,
    }


# ============================================================
# TAG ONE CHUNK
# ============================================================

def tag_chunk(chunk, chunk_index):

    source_pdf = chunk["source_pdf"]
    page = chunk["page"]
    text = chunk["text"]

    info = get_document_info(source_pdf)

    topic = detect_topic(chunk)

    metrics = detect_metrics(text)

    practices = detect_practices(text)

    claim_type = detect_claim_type(
        text,
        practices
    )

    # Ensure at least one valid metric where possible.
    # If no metric is detected, use the broad topic-related
    # information only and leave metric empty.
    metadata = ChunkMetadata(
        chunk_id=chunk["chunk_id"],
        text=text,
        source=info["source"],
        document=info["document"],
        year=info["year"],
        page=page,
        topic=topic,
        metric=metrics,
        practice=practices,
        region_scope="global",
        claim_type=claim_type,
    )

    return metadata


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n")
    print("#" * 80)
    print("              ECOSYNAPSE CHUNK TAGGING")
    print("#" * 80)

    print(f"\nInput:")
    print(CHUNKS_PATH)

    print(f"\nOutput:")
    print(OUTPUT_PATH)

    if not CHUNKS_PATH.exists():

        raise FileNotFoundError(
            f"\nchunks.jsonl not found:\n{CHUNKS_PATH}\n\n"
            "Run 02_chunk_documents.py first."
        )

    chunks = []

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            if line:
                chunks.append(json.loads(line))

    print(f"\nChunks loaded: {len(chunks):,}")

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    topic_counts = {}
    claim_counts = {}
    metricless_count = 0

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as output:

        for i, chunk in enumerate(chunks, start=1):

            metadata = tag_chunk(
                chunk,
                i
            )

            metadata_dict = metadata.__dict__

            output.write(
                json.dumps(
                    metadata_dict,
                    ensure_ascii=False
                ) + "\n"
            )

            topic_counts[metadata.topic] = (
                topic_counts.get(metadata.topic, 0) + 1
            )

            claim_counts[metadata.claim_type] = (
                claim_counts.get(metadata.claim_type, 0) + 1
            )

            if not metadata.metric:
                metricless_count += 1

    print("\n")
    print("#" * 80)
    print("                    TAGGING SUMMARY")
    print("#" * 80)

    print(f"\nChunks tagged : {len(chunks):,}")

    print("\nTopics:")
    for topic, count in sorted(topic_counts.items()):
        print(f"  {topic:<25} {count:,}")

    print("\nClaim types:")
    for claim_type, count in sorted(claim_counts.items()):
        print(f"  {claim_type:<25} {count:,}")

    print(f"\nChunks without detected metric: {metricless_count:,}")

    print(f"\nSaved to:")
    print(OUTPUT_PATH)

    print("\nNext step:")
    print("    python src\\ingestion\\4_build_embeddings.py")
    print()


if __name__ == "__main__":
    main()