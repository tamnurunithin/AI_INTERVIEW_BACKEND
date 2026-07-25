from typing import List


def split_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100
) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Input text to split.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Number of overlapping characters.

    Returns:
        List of text chunks.
    """

    # Remove unnecessary spaces and blank lines
    text = " ".join(text.split())

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:

        end = min(start + chunk_size, text_length)

        chunk = text[start:end]

        chunks.append(chunk)

        if end == text_length:
            break

        start = end - chunk_overlap

    return chunks