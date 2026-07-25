from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


# ==========================================
# Interview Question
# ==========================================

class InterviewQuestion(BaseModel):
    """
    Represents a single interview question.
    """

    question_number: int
    question: str
    answer: str = ""
    score: float = 0.0


# ==========================================
# Interview Session
# ==========================================

class InterviewSession(BaseModel):
    """
    Stores one complete interview session.
    """

    session_id: str

    resume_filename: str

    interview_type: str = "Technical"

    difficulty: str = "medium"

    total_questions: int = 10

    current_question: int = 0

    questions: List[InterviewQuestion] = Field(default_factory=list)

    overall_score: float = 0.0

    started_at: datetime = Field(default_factory=datetime.utcnow)

    completed: bool = False


# ==========================================
# Start Interview Request
# ==========================================

class StartInterviewRequest(BaseModel):
    resume_filename: str
    interview_type: str = "Technical"
    difficulty: str = "medium"
    total_questions: int = 10


# ==========================================
# Start Interview Response
# ==========================================

class StartInterviewResponse(BaseModel):
    success: bool
    session_id: str
    message: str


# ==========================================
# Submit Answer Request
# ==========================================

class SubmitAnswerRequest(BaseModel):
    session_id: str
    question_number: int
    answer: str


# ==========================================
# Submit Answer Response
# ==========================================

class SubmitAnswerResponse(BaseModel):
    success: bool
    next_question: str | None = None
    interview_completed: bool = False


# ==========================================
# End Interview Response
# ==========================================

class EndInterviewResponse(BaseModel):
    success: bool
    session_id: str
    overall_score: float
    message: str