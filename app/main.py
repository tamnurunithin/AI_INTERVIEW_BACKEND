from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

from app.api.health import router as health_router
from app.api.resume import router as resume_router
from app.api.retriever import router as retriever_router
from app.api.interview import router as interview_router
from app.api.report import router as report_router
from app.api.speech import router as speech_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for AI Interview Coach"
)


# ==========================================
# CORS Configuration
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        settings.FRONTEND_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to AI Interview Coach API",
        "version": settings.APP_VERSION,
    }


# ==========================================
# Register API Routes
# ==========================================

app.include_router(health_router)

app.include_router(resume_router)

app.include_router(retriever_router)

app.include_router(interview_router)

app.include_router(report_router)

# ==========================================
# Speech-to-Text (Groq Whisper)
# ==========================================

app.include_router(speech_router)