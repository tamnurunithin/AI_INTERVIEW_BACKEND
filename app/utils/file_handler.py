from pathlib import Path
import shutil
from fastapi import UploadFile

# Upload folder
UPLOAD_DIR = Path("uploads")

# Create uploads folder if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)


def save_uploaded_file(file: UploadFile) -> str:
    """
    Save uploaded PDF file to uploads directory.
    Returns saved file path.
    """

    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return str(file_path)