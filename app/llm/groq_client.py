from groq import Groq

from app.config import settings


# ==========================================
# Groq Client
# ==========================================

if not settings.GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to your .env file or deployment environment variables."
    )


client = Groq(
    api_key=settings.GROQ_API_KEY
)


# ==========================================
# Default Model
# ==========================================

MODEL_NAME = settings.GROQ_MODEL


# ==========================================
# Generic LLM Function
# ==========================================

def generate_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
):
    """
    Sends a prompt to the Groq LLM
    and returns the generated response.
    """

    completion = client.chat.completions.create(

        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert AI Interview Coach. "
                    "You help candidates prepare for interviews "
                    "by asking intelligent, professional, and "
                    "resume-aware interview questions."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        temperature=temperature,

        max_tokens=max_tokens,
    )

    return completion.choices[0].message.content.strip()
