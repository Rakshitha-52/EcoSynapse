"""
04_build_embeddings.py

Loads chunk_metadata.jsonl (built by 03_tag_chunks.py) and computes a
dense embedding for every chunk's text using all-MiniLM-L6-v2.

Run this on a machine with internet access to huggingface.co — the
model weights (~90MB) download automatically on first run and are
cached locally after that.

Output: embeddings.npy (float32 array, shape = [num_chunks, 384])
        saved in the same order as the lines in chunk_metadata.jsonl.

Usage:
    python3 04_build_embeddings.py
"""

import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

# --- Paths (adjust to your EcoSynapse layout if different) ---
INDEX_DIR = Path(__file__).resolve().parent.parent.parent / "index"
CHUNK_METADATA_PATH = INDEX_DIR / "chunk_metadata.jsonl"
EMBEDDINGS_OUTPUT_PATH = INDEX_DIR / "embeddings.npy"

MODEL_NAME = "all-MiniLM-L6-v2"


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
    print(f"  {len(chunks)} chunks loaded")

    if not chunks:
        raise ValueError(
            "No chunks found — run 01_extract_text.py, 02_chunk_documents.py, "
            "and 03_tag_chunks.py first."
        )

    print(f"Loading embedding model '{MODEL_NAME}' (downloads on first run)...")
    model = SentenceTransformer(MODEL_NAME)

    texts = [c["text"] for c in chunks]

    print(f"Encoding {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,  # so inner product == cosine similarity later
    )
    embeddings = np.array(embeddings, dtype="float32")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    np.save(EMBEDDINGS_OUTPUT_PATH, embeddings)

    print(f"\nSaved embeddings: shape={embeddings.shape} -> {EMBEDDINGS_OUTPUT_PATH}")
    print("Next step: run 05_build_faiss_index.py")


if __name__ == "__main__":
    main()