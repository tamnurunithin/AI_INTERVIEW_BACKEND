from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.rag.retriever import retrieve_chunks
from app.rag.prompt import build_interview_prompt
from app.llm.groq_client import generate_response
from app.scoring.interview_score import evaluate_answer
from app.scoring.final_report import generate_final_report


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


INTERVIEW_SESSIONS = {}


class InterviewRequest(BaseModel):
    topic: str = "Technical Interview"
    difficulty: str = "medium"
    num_questions: int = 10


class StartInterviewRequest(BaseModel):
    name: str
    email: str
    topic: str = "Technical Interview"
    difficulty: str = "medium"
    num_questions: int = 10


class SubmitAnswerRequest(BaseModel):
    session_id: str
    answer: str

    # Camera Analytics
    total_frames: int = 0
    detected_frames: int = 0
    face_lost: int = 0


# ======================================================
# Generate Resume-Based Questions
# ======================================================

@router.post("/generate")
async def generate_interview_questions(request: InterviewRequest):

    try:

        retrieved_chunks = retrieve_chunks(
            request.topic,
            top_k=5
        )

        if not retrieved_chunks:
            raise HTTPException(
                status_code=404,
                detail="No resume context found."
            )

        resume_context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        prompt = build_interview_prompt(
            resume_context=resume_context,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )

        response = generate_response(prompt)

        return {
            "success": True,
            "topic": request.topic,
            "difficulty": request.difficulty,
            "questions": response
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# Start Interview
# ======================================================

@router.post("/start")
async def start_interview(request: StartInterviewRequest):

    try:

        retrieved_chunks = retrieve_chunks(
            request.topic,
            top_k=5
        )

        if not retrieved_chunks:
            raise HTTPException(
                status_code=404,
                detail="Resume not found."
            )

        resume_context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        prompt = build_interview_prompt(
            resume_context=resume_context,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )

        response = generate_response(prompt)

        questions = []

        for line in response.split("\n"):

            line = line.strip()

            if not line:
                continue

            if line[0].isdigit():

                question = line.split(".", 1)[-1].strip()

                questions.append(question)

        session_id = str(uuid4())

        INTERVIEW_SESSIONS[session_id] = {

            "name": request.name,

            "email": request.email,

            "questions": questions,

            "answers": [],

            "current_question": 0,

            "resume_context": resume_context,

            "completed": False,

            "report": None,

            # Camera Analytics
            "camera": {
                "total_frames": 0,
                "detected_frames": 0,
                "face_lost": 0
            }

        }

        return {

            "success": True,

            "session_id": session_id,

            "candidate": {

                "name": request.name,

                "email": request.email

            },

            "total_questions": len(questions),

            "current_question_number": 1,

            "current_question": questions[0] if questions else None

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ======================================================
# Submit Answer
# ======================================================

@router.post("/answer")
async def submit_answer(request: SubmitAnswerRequest):

    if request.session_id not in INTERVIEW_SESSIONS:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    session = INTERVIEW_SESSIONS[request.session_id]

    if session["completed"]:

        return {

            "success": False,

            "message": "Interview already completed."

        }

    current_index = session["current_question"]

    current_question = session["questions"][current_index]

    evaluation = evaluate_answer(

        question=current_question,

        answer=request.answer,

        resume_context=session["resume_context"]

    )

    session["answers"].append({

        "question": current_question,

        "answer": request.answer,

        "evaluation": evaluation

    })

    # Save latest camera analytics

    session["camera"] = {

        "total_frames": request.total_frames,

        "detected_frames": request.detected_frames,

        "face_lost": request.face_lost

    }

    session["current_question"] += 1

    # ==================================================
    # Interview Completed
    # ==================================================

    if session["current_question"] >= len(session["questions"]):

        session["completed"] = True

        report = generate_final_report(
            session["answers"],
            session["camera"]
        )

        report["candidate"] = {

            "name": session["name"],

            "email": session["email"]

        }

        session["report"] = report

        return {

            "success": True,

            "completed": True,

            "report": report,

            "message": "Interview completed successfully."

        }

    # ==================================================
    # Next Question
    # ==================================================

    next_question = session["questions"][session["current_question"]]

    return {

        "success": True,

        "completed": False,

        "evaluation": evaluation,

        "question_number": session["current_question"] + 1,

        "next_question": next_question

    }


# ======================================================
# Get Interview Session
# ======================================================

@router.get("/session/{session_id}")
async def get_session(session_id: str):

    if session_id not in INTERVIEW_SESSIONS:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    return {

        "success": True,

        "session": INTERVIEW_SESSIONS[session_id]

    }


# ======================================================
# Get Final Interview Report
# ======================================================

@router.get("/report/{session_id}")
async def get_final_report(session_id: str):

    if session_id not in INTERVIEW_SESSIONS:

        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    session = INTERVIEW_SESSIONS[session_id]

    if not session["completed"]:

        raise HTTPException(
            status_code=400,
            detail="Interview is not completed yet."
        )

    report = session["report"]

    report["candidate"] = {

        "name": session["name"],

        "email": session["email"]

    }

    return {

        "success": True,

        "report": report

    }