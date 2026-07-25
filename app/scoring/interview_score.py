import json

from app.llm.groq_client import generate_response


# ======================================================
# Build Evaluation Prompt
# ======================================================

def build_evaluation_prompt(
    question: str,
    answer: str,
    resume_context: str = ""
) -> str:
    """
    Creates a structured prompt for evaluating
    the candidate's interview answer.
    """

    return f"""
You are an experienced Senior Technical Interviewer.

Candidate Resume:
-----------------
{resume_context}

Interview Question:
-------------------
{question}

Candidate Answer:
-----------------
{answer}

Evaluate the answer carefully.

Return ONLY valid JSON.

JSON Format:

{{
    "technical_score": 0,
    "communication_score": 0,
    "strengths": [],
    "improvements": [],
    "feedback": ""
}}

Rules:

- technical_score should be between 0 and 10
- communication_score should be between 0 and 10
- strengths should contain 2-4 short bullet points
- improvements should contain 2-4 short bullet points
- feedback should be a concise paragraph.

Return JSON only.
"""


# ======================================================
# Evaluate Interview Answer
# ======================================================

def evaluate_answer(
    question: str,
    answer: str,
    resume_context: str = ""
):
    """
    Evaluates a candidate's answer using Groq LLM.
    Returns structured JSON.
    """

    prompt = build_evaluation_prompt(
        question=question,
        answer=answer,
        resume_context=resume_context
    )

    response = generate_response(
        prompt=prompt,
        temperature=0.2,
        max_tokens=700
    )

    try:

        # Remove markdown code fences if present
        cleaned = (
            response.replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned)

    except Exception:

        # Fallback if the LLM doesn't return valid JSON
        return {
            "technical_score": 0,
            "communication_score": 0,
            "strengths": [],
            "improvements": [],
            "feedback": response
        }