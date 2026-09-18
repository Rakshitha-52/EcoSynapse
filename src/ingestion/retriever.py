"""
retriever.py — loads the FAISS index + chunk metadata built in
04_build_embeddings.py / 05_build_faiss_index.py, and exposes retrieve()
for metadata-filtered semantic search.

Run this module's __main__ block directly for a one-query smoke test,
or import retrieve() from test_retriever.py to run the full test suite.
"""

import json
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# --- Paths (adjust if your folder layout differs) ---
INDEX_DIR = Path(__file__).resolve().parent.parent.parent / "index"
FAISS_INDEX_PATH = INDEX_DIR / "faiss.index"
CHUNK_METADATA_PATH = INDEX_DIR / "chunk_metadata.jsonl"
ROW_TO_CHUNK_ID_PATH = INDEX_DIR / "faiss_row_to_chunk_id.json"

MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks(path: Path) -> list[dict]:
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


# --- Load everything once, at import time ---
print("Loading FAISS index...")
_index = faiss.read_index(str(FAISS_INDEX_PATH))

print("Loading chunk metadata...")
_chunks = load_chunks(CHUNK_METADATA_PATH)

print("Loading row-to-chunk_id mapping...")
with open(ROW_TO_CHUNK_ID_PATH, "r", encoding="utf-8") as f:
    _row_to_chunk_id = json.load(f)

# chunk_id -> chunk dict, and chunk_id -> row index, for fast lookup
_chunk_by_id = {c["chunk_id"]: c for c in _chunks}
_chunk_id_to_row = {cid: row for row, cid in enumerate(_row_to_chunk_id)}

print("Loading embedding model (this can take a few seconds the first time)...")
_model = SentenceTransformer(MODEL_NAME)

# Reconstruct all embeddings from the FAISS index once, so filtered
# candidate scoring doesn't need to re-embed the whole corpus per query.
_all_embeddings = _index.reconstruct_n(0, _index.ntotal)

print(f"Ready: {len(_chunks)} chunks loaded, index has {_index.ntotal} vectors.\n")


def retrieve(query: str, topic_filter: list = None, metric_filter: list = None,
             practice_filter: list = None, top_k: int = 5) -> list[tuple[dict, float]]:
    """
    Metadata-filtered semantic search.
    Returns a list of (chunk_dict, similarity_score) tuples, ranked with
    practice_evidence chunks first, then by similarity score.
    """
    candidates = _chunks
    if topic_filter:
        candidates = [c for c in candidates if c["topic"] in topic_filter]
    if metric_filter:
        candidates = [c for c in candidates if any(m in c["metric"] for m in metric_filter)]
    if practice_filter:
        candidates = [c for c in candidates if any(p in c["practice"] for p in practice_filter)]

    if not candidates:
        return []  # no matching evidence — caller must handle this, never fabricate a citation

    query_vec = _model.encode([query], normalize_embeddings=True)[0]

    candidate_rows = [_chunk_id_to_row[c["chunk_id"]] for c in candidates]
    candidate_vecs = np.array([_all_embeddings[r] for r in candidate_rows], dtype="float32")

    scores = candidate_vecs @ query_vec

    ranked = sorted(
        zip(candidates, scores),
        key=lambda pair: (pair[0]["claim_type"] != "practice_evidence", -pair[1])
    )
    return ranked[:top_k]


if __name__ == "__main__":
    # one-query smoke test
    results = retrieve(
        "cover crops and organic amendments effect on soil organic carbon",
        topic_filter=["soil_health"],
        metric_filter=["organic_carbon"],
        practice_filter=["cover_crops", "organic_amendments"],
    )
    print(f"Got {len(results)} result(s):")
    for chunk, score in results:
        print(f"  [{score:.3f}] {chunk['chunk_id']} ({chunk['claim_type']}): {chunk['text'][:100]}...")