import os
import shutil
import tempfile

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.llm.whisper_client import transcribe_audio


router = APIRouter(
    prefix="/speech",
    tags=["Speech"]
)


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """
    Speech-to-Text using Groq Whisper
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file uploaded."
        )

    allowed_extensions = (
        ".wav",
        ".mp3",
        ".m4a",
        ".webm",
        ".ogg",
        ".flac"
    )

    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    temp_path = None

    try:

        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            shutil.copyfileobj(
                file.file,
                temp_file
            )

            temp_path = temp_file.name

        transcript = transcribe_audio(temp_path)

        return {
            "success": True,
            "transcript": transcript
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)