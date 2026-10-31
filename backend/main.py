"""
LearnSphere AI — FastAPI application entry point.
B.Tech Computer Science and Engineering Adaptive Learning Platform.
"""
import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()  # Load .env file if present

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, subjects, students, assessment, learning, revisions, teacher, concepts
from app.database.init_db import init_database
from app.utils.rate_limiter import RateLimiterMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and seed curriculum on startup."""
    init_database()
    yield


app = FastAPI(
    title="LearnSphere AI API",
    version="2.0.0",
    description="Adaptive B.Tech Computer Science & Engineering learning platform powered by Gemini AI.",
    lifespan=lifespan,
)

# ── Dynamic CORS Configuration ────────────────────────────────────────────────
default_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]
env_origins = os.getenv("CORS_ORIGINS", "")
if env_origins:
    for o in env_origins.split(","):
        cleaned = o.strip()
        if cleaned and cleaned not in default_origins:
            default_origins.append(cleaned)

app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Production Rate Limiter Middleware ────────────────────────────────────────
app.add_middleware(RateLimiterMiddleware)


@app.get("/api/health", tags=["health"])
def health():
    """Health-check endpoint."""
    return {
        "status": "ok",
        "message": "LearnSphere AI B.Tech CSE Backend Running",
        "curriculum": "B.Tech Computer Science and Engineering",
    }


# ── Include routers ──────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/api")
app.include_router(subjects.router, prefix="/api")
app.include_router(concepts.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(assessment.router, prefix="/api")
app.include_router(learning.router, prefix="/api")
app.include_router(revisions.router, prefix="/api")
app.include_router(teacher.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
