from pydantic import BaseModel
from typing import List


# ======================================================
# Individual Answer Evaluation
# ======================================================

class AnswerEvaluation(BaseModel):
    technical_score: int
    communication_score: int
    strengths: List[str]
    improvements: List[str]
    feedback: str


# ======================================================
# Question + Candidate Answer
# ======================================================

class InterviewAnswer(BaseModel):
    question: str
    answer: str
    evaluation: AnswerEvaluation


# ======================================================
# Final Interview Report
# ======================================================

class InterviewReport(BaseModel):
    total_questions: int

    answered_questions: int

    average_technical_score: float

    average_communication_score: float

    overall_score: float

    recommendation: str

    answers: List[InterviewAnswer]