from groq import Groq

from app.config import settings


# ==========================================
# Groq Client
# ==========================================

client = Groq(
    api_key=settings.GROQ_API_KEY
)


# Default Model
MODEL_NAME = "llama-3.3-70b-versatile"


# ==========================================
# Generic LLM Function
# ==========================================

def generate_response(
    prompt: str,
    temperature: float = 0.7,
    max_tokens: int = 1024,
):
    """
    Sends a prompt to Groq Llama model
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