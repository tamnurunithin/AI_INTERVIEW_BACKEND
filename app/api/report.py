from fastapi import APIRouter, HTTPException

from app.api.interview import INTERVIEW_SESSIONS
from app.scoring.final_report import generate_final_report

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


# ======================================================
# Get Final Interview Report
# ======================================================

@router.get("/{session_id}")
async def get_final_report(session_id: str):
    """
    Returns the complete interview report for a session.
    """

    if session_id not in INTERVIEW_SESSIONS:
        raise HTTPException(
            status_code=404,
            detail="Interview session not found."
        )

    session = INTERVIEW_SESSIONS[session_id]

    if not session["completed"]:
        raise HTTPException(
            status_code=400,
            detail="Interview is still in progress."
        )

    report = generate_final_report(session["answers"])

    return {
        "success": True,
        "session_id": session_id,
        "report": report
    }


# ======================================================
# List All Interview Reports
# ======================================================

@router.get("/")
async def list_reports():
    """
    Returns all completed interview sessions.
    """

    completed_reports = []

    for session_id, session in INTERVIEW_SESSIONS.items():

        if session["completed"]:

            completed_reports.append({
                "session_id": session_id,
                "questions": len(session["questions"]),
                "answers": len(session["answers"])
            })

    return {
        "success": True,
        "total_reports": len(completed_reports),
        "reports": completed_reports
    }