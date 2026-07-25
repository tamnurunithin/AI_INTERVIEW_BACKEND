from app.utils.pdf_loader import extract_text_from_pdf
from app.utils.text_splitter import split_text


def parse_resume(pdf_path: str) -> list[str]:
    """
    Parse the uploaded resume.

    Steps:
    1. Extract text from the PDF.
    2. Split the text into overlapping chunks.
    3. Return the list of chunks.
    """

    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Split into chunks
    chunks = split_text(text)

    return chunks