"""
Prompt templates used by the AI Interview Coach.
This file is responsible for creating high-quality prompts
that are sent to the Groq LLM.
"""


# ==========================================
# Resume-Based Interview Prompt
# ==========================================

def build_interview_prompt(
    resume_context: str,
    difficulty: str = "medium",
    num_questions: int = 10
) -> str:
    """
    Creates a prompt for generating interview questions
    using the uploaded resume context.
    """

    prompt = f"""
You are a Senior Technical Interviewer with over 15 years of experience.

Your task is to generate {num_questions} interview questions.

Candidate Resume Information:
----------------------------------------------------
{resume_context}
----------------------------------------------------

Instructions:

1. Generate interview questions ONLY using the resume.
2. Focus on:
   - Skills
   - Projects
   - Technologies
   - Work Experience
   - Certifications
3. Start with easy questions.
4. Gradually increase difficulty.
5. Include conceptual questions.
6. Include project-based questions.
7. Include scenario-based questions.
8. Do NOT ask duplicate questions.
9. Keep every question concise.
10. Return ONLY the numbered questions.

Difficulty Level:
{difficulty}

Example Format:

1. Tell me about yourself.
2. Explain your Resume Matcher project.
3. Why did you choose FAISS?
4. Explain your Kafka implementation.
5. What challenges did you face while building this project?
"""

    return prompt


# ==========================================
# Answer Evaluation Prompt
# ==========================================

def build_evaluation_prompt(
    question: str,
    answer: str
) -> str:
    """
    Creates a prompt to evaluate
    a candidate's answer.
    """

    prompt = f"""
You are an experienced technical interviewer.

Interview Question:

{question}

Candidate Answer:

{answer}

Evaluate the answer on:

1. Technical Accuracy
2. Communication
3. Confidence
4. Completeness
5. Practical Knowledge

Give:

Overall Score (0-10)

Strengths

Weaknesses

Suggestions for Improvement
"""

    return prompt


# ==========================================
# HR Interview Prompt
# ==========================================

def build_hr_prompt(
    resume_context: str
) -> str:
    """
    Creates HR interview questions.
    """

    prompt = f"""
You are an HR interviewer.

Candidate Resume:

{resume_context}

Generate 10 HR interview questions based on the resume.

Focus on:

- Career Goals
- Leadership
- Teamwork
- Communication
- Problem Solving
- Motivation

Return only numbered questions.
"""

    return prompt


# ==========================================
# Follow-up Question Prompt
# ==========================================

def build_followup_prompt(
    previous_question: str,
    previous_answer: str
) -> str:
    """
    Generates a follow-up question
    based on the candidate's answer.
    """

    prompt = f"""
You are conducting a technical interview.

Previous Question:

{previous_question}

Candidate Answer:

{previous_answer}

Generate ONE intelligent follow-up question.

Return ONLY the question.
"""

    return prompt