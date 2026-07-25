from pathlib import Path
import json

import faiss
import numpy as np


# ===============================
# Vector Database Folder
# ===============================

VECTOR_DB_DIR = Path("vector_db")
VECTOR_DB_DIR.mkdir(exist_ok=True)

INDEX_FILE = VECTOR_DB_DIR / "resume.index"
CHUNKS_FILE = VECTOR_DB_DIR / "chunks.json"


# ===============================
# Create Vector Store
# ===============================

def create_vector_store(
    embeddings: list[list[float]],
    chunks: list[str]
):
    """
    Create a FAISS vector store and save
    both the vectors and the original chunks.
    """

    # Convert embeddings to numpy float32
    vectors = np.array(embeddings, dtype=np.float32)

    # Embedding dimension
    dimension = vectors.shape[1]

    # Create FAISS Index
    index = faiss.IndexFlatL2(dimension)

    # Add vectors
    index.add(vectors)

    # Save FAISS index
    faiss.write_index(index, str(INDEX_FILE))

    # Save chunks
    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=4)

    return index


# ===============================
# Load Vector Store
# ===============================

def load_vector_store():
    """
    Load the saved FAISS index.
    """

    if not INDEX_FILE.exists():
        return None

    return faiss.read_index(str(INDEX_FILE))


# ===============================
# Load Chunks
# ===============================

def load_chunks():
    """
    Load the saved resume chunks.
    """

    if not CHUNKS_FILE.exists():
        return []

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ===============================
# Total Stored Vectors
# ===============================

def total_vectors():
    """
    Return the number of vectors
    stored in the FAISS database.
    """

    index = load_vector_store()

    if index is None:
        return 0

    return index.ntotal