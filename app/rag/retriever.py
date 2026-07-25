import json
from pathlib import Path

import faiss
import numpy as np

from app.rag.embeddings import generate_embedding

# Vector database files
VECTOR_DB_DIR = Path("vector_db")
INDEX_FILE = VECTOR_DB_DIR / "resume.index"
CHUNKS_FILE = VECTOR_DB_DIR / "chunks.json"


def retrieve_chunks(query: str, top_k: int = 3):
    """
    Retrieve the most relevant resume chunks
    for a given user query using FAISS.
    """

    # Check if files exist
    if not INDEX_FILE.exists():
        raise FileNotFoundError("FAISS index not found.")

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("chunks.json not found.")

    # Load FAISS index
    index = faiss.read_index(str(INDEX_FILE))

    # Load stored chunks
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    # Generate embedding for the user query
    query_embedding = generate_embedding(query)

    # Convert to numpy float32
    query_vector = np.array(
        [query_embedding],
        dtype="float32"
    )

    # Search FAISS
    distances, indices = index.search(query_vector, top_k)

    results = []

    for rank, idx in enumerate(indices[0]):
        if idx == -1:
            continue

        results.append({
            "rank": rank + 1,
            "chunk_index": int(idx),
            "distance": float(distances[0][rank]),
            "text": chunks[idx]
        })

    return results