from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

model = SentenceTransformer("all-MiniLM-L6-v2")  # fast, solid quality, same as most RAG starter stacks

def load_chunks(path):
    chunks = []
    with open(path) as f:
        for line in f:
            chunks.append(json.loads(line))
    return chunks

chunks = load_chunks("../../index/chunk_metadata.jsonl")
texts = [c["text"] for c in chunks]

embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)
embeddings = np.array(embeddings, dtype="float32")

# Flat index is fine at this corpus size (a few hundred to low thousands of chunks) —
# don't reach for IVF/HNSW, it adds complexity with zero benefit here.
index = faiss.IndexFlatIP(embeddings.shape[1])  # inner product = cosine sim, since embeddings are normalized
index.add(embeddings)

faiss.write_index(index, "../../index/faiss.index")

# Save the chunk_id order separately — FAISS returns row indices, you need
# to map those back to chunk_id / metadata.
with open("../../index/faiss_row_to_chunk_id.json", "w") as f:
    json.dump([c["chunk_id"] for c in chunks], f)