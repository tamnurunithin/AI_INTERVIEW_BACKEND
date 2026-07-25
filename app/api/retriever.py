from fastapi import APIRouter

from app.rag.retriever import retrieve_chunks

router = APIRouter(
    prefix="/retriever",
    tags=["Retriever"]
)


@router.post("/search")
async def search_resume(query: str):
    """
    Search the uploaded resume using semantic similarity.
    """

    results = retrieve_chunks(query)

    return {
        "query": query,
        "matches": results
    }