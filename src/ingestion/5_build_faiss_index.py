"""
05_build_faiss_index.py

Loads embeddings.npy (built by 04_build_embeddings.py) and
chunk_metadata.jsonl, builds a flat FAISS index (exact search — correct
choice at this corpus size, no need for IVF/HNSW), and saves:

  - faiss.index                  the FAISS index itself
  - faiss_row_to_chunk_id.json    maps FAISS row number -> chunk_id,
                                  since FAISS only returns row indices

Usage:
    python3 05_build_faiss_index.py
"""

import json
from pathlib import Path

import numpy as np
import faiss

INDEX_DIR = Path(__file__).resolve().parent.parent.parent / "index"
CHUNK_METADATA_PATH = INDEX_DIR / "chunk_metadata.jsonl"
EMBEDDINGS_PATH = INDEX_DIR / "embeddings.npy"
FAISS_INDEX_OUTPUT_PATH = INDEX_DIR / "faiss.index"
ROW_TO_CHUNK_ID_OUTPUT_PATH = INDEX_DIR / "faiss_row_to_chunk_id.json"


def load_chunks(path: Path) -> list[dict]:
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def main():
    print(f"Loading chunks from {CHUNK_METADATA_PATH}...")
    chunks = load_chunks(CHUNK_METADATA_PATH)

    print(f"Loading embeddings from {EMBEDDINGS_PATH}...")
    embeddings = np.load(EMBEDDINGS_PATH)

    if embeddings.shape[0] != len(chunks):
        raise ValueError(
            f"Mismatch: {embeddings.shape[0]} embeddings but {len(chunks)} chunks. "
            "Did chunk_metadata.jsonl change since you ran 04_build_embeddings.py? "
            "Re-run step 4 if so."
        )

    dim = embeddings.shape[1]
    print(f"Building flat FAISS index (IndexFlatIP, dim={dim})...")

    # IndexFlatIP = inner product = cosine similarity, since embeddings
    # were normalized in step 4. Flat = exact search, correct at this
    # corpus size (hundreds to low thousands of chunks) — don't reach
    # for IVF/HNSW, it adds complexity for zero benefit here.
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_OUTPUT_PATH))

    row_to_chunk_id = [c["chunk_id"] for c in chunks]
    with open(ROW_TO_CHUNK_ID_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(row_to_chunk_id, f, indent=2)

    print(f"\nIndex built: {index.ntotal} vectors")
    print(f"  -> {FAISS_INDEX_OUTPUT_PATH}")
    print(f"  -> {ROW_TO_CHUNK_ID_OUTPUT_PATH}")
    print("\nNext step: run retriever.py or test_retriever.py")


if __name__ == "__main__":
    main()