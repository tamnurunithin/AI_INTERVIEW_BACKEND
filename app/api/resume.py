from fastapi import APIRouter, UploadFile, File, HTTPException

from app.utils.file_handler import save_uploaded_file
from app.nlp.resume_parser import parse_resume
from app.rag.embeddings import generate_embeddings
from app.rag.vector_store import create_vector_store

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)


@router.post("/upload")
async def upload_resume(resume: UploadFile = File(...)):
    """
    Upload resume, parse it, generate embeddings,
    create FAISS vector database and return summary.
    """

    # -----------------------------
    # Validate PDF
    # -----------------------------
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # -----------------------------
    # Save PDF
    # -----------------------------
    file_path = save_uploaded_file(resume)

    # -----------------------------
    # Parse Resume
    # -----------------------------
    chunks = parse_resume(file_path)

    if len(chunks) == 0:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the resume."
        )

    # -----------------------------
    # Generate Gemini Embeddings
    # -----------------------------
    embeddings = generate_embeddings(chunks)

    # -----------------------------
    # Create FAISS Vector Database
    # -----------------------------
    index = create_vector_store(
        embeddings=embeddings,
        chunks=chunks
    )

    # -----------------------------
    # Success Response
    # -----------------------------
    return {
        "message": "Resume processed successfully.",
        "filename": resume.filename,
        "file_path": file_path,
        "chunks_created": len(chunks),
        "embeddings_created": len(embeddings),
        "embedding_dimension": len(embeddings[0]),
        "vectors_saved": index.ntotal
    }