import fitz


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a PDF file using PyMuPDF.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()