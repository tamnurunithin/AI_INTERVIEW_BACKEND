import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ==========================================================
# Groq Client
# ==========================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==========================================================
# Speech to Text using Groq Whisper
# ==========================================================

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribes an audio file using Groq Whisper.

    Parameters
    ----------
    audio_path : str
        Path to the uploaded audio file.

    Returns
    -------
    str
        Transcribed text.
    """

    try:

        with open(audio_path, "rb") as audio_file:

            transcription = client.audio.transcriptions.create(

                file=audio_file,

                model="whisper-large-v3",

                response_format="verbose_json",

                language="en",

                temperature=0

            )

        return transcription.text

    except Exception as e:

        raise Exception(
            f"Whisper transcription failed: {str(e)}"
        )