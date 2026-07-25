from google import genai

from app.config import settings

# Create Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# Gemini Embedding Model
EMBEDDING_MODEL = "gemini-embedding-001"


def generate_embedding(text: str) -> list[float]:
    """
    Generate an embedding for a single text chunk.
    """

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


def generate_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for all chunks.
    """

    return [generate_embedding(chunk) for chunk in chunks]