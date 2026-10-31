"""
Pydantic v2 schemas for LearnSphere AI — B.Tech Computer Science & Engineering.
"""
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, EmailStr, field_validator


# ── Auth & Student ─────────────────────────────────────────────────────────────

class StudentCreate(BaseModel):
    name: str
    email: str
    password: str
    learning_level: str = "Intermediate"
    degree: str = "B.Tech Computer Science & Engineering"
    selected_subject_ids: list[int] = []

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = v.strip().lower()
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email address format.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return v


class StudentLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        return v.strip().lower()


class StudentProfileUpdate(BaseModel):
    name: Optional[str] = None
    learning_level: Optional[str] = None
    selected_subject_ids: Optional[list[int]] = None


class EnrolledSubjectOut(BaseModel):
    id: int
    name: str
    code: str
    category: str
    icon: str
    target_level: str
    enrolled_at: datetime

    model_config = {"from_attributes": True}


class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    learning_level: str
    degree: str
    role: str = "student"
    created_at: datetime
    last_active: Optional[datetime] = None
    streak_days: int = 1
    enrolled_subjects: list[EnrolledSubjectOut] = []

    model_config = {"from_attributes": True}


class AuthToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    student: StudentOut


# ── Subject & Concept ──────────────────────────────────────────────────────────

class SubjectOut(BaseModel):
    id: int
    category: str
    name: str
    code: str
    description: Optional[str] = None
    icon: str
    order_index: int
    concept_count: int = 0
    is_enrolled: bool = False

    model_config = {"from_attributes": True}


class ConceptOut(BaseModel):
    id: int
    subject_id: int
    topic_id: Optional[int] = None
    name: str
    description: Optional[str] = None
    order_index: int
    prerequisites: list[int] = []
    subject_name: Optional[str] = None

    model_config = {"from_attributes": True}


class TopicOut(BaseModel):
    id: int
    subject_id: int
    name: str
    description: Optional[str] = None
    order_index: int
    concepts: list[ConceptOut] = []

    model_config = {"from_attributes": True}


class SubjectDetailOut(SubjectOut):
    topics: list[TopicOut] = []
    concepts: list[ConceptOut] = []


# ── Questions ──────────────────────────────────────────────────────────────────

class QuestionOut(BaseModel):
    id: Optional[int] = None
    subject_id: int
    concept_id: int
    subject_name: Optional[str] = None
    concept_name: str
    question_type: str = "mcq"  # mcq, output_prediction, code_debugging, conceptual, sql_query, scenario
    question_text: str
    code_snippet: Optional[str] = None
    options: dict[str, str]
    difficulty: str
    is_ai_generated: bool = False
    current_mastery: Optional[float] = None


class QuestionDB(BaseModel):
    id: int
    subject_id: int
    concept_id: int
    question_type: str
    question_text: str
    code_snippet: Optional[str] = None
    options: dict[str, str]
    correct_answer: str
    explanation: Optional[str] = None
    difficulty: str
    is_ai_generated: bool = False

    model_config = {"from_attributes": True}


# ── Assessment ─────────────────────────────────────────────────────────────────

class AnswerSubmit(BaseModel):
    question_id: int
    selected_answer: str

    @field_validator("selected_answer")
    @classmethod
    def validate_answer(cls, v: str) -> str:
        v = v.upper().strip()
        if v not in ("A", "B", "C", "D"):
            raise ValueError("selected_answer must be A, B, C, or D")
        return v


class AssessmentSubmit(BaseModel):
    student_id: int
    subject_id: Optional[int] = None
    answers: list[AnswerSubmit]


class AssessmentResult(BaseModel):
    assessment_id: int
    total_questions: int
    correct_answers: int
    score_percentage: float
    completed_at: datetime
    mastery_initialized: dict[str, float]
    recommendations: list[str]


# ── Learning Workspace ─────────────────────────────────────────────────────────

class LearningAnswerSubmit(BaseModel):
    student_id: int
    question_id: Optional[int] = None
    concept_id: int
    selected_answer: str
    written_reasoning: Optional[str] = None
    time_taken_seconds: Optional[int] = None

    @field_validator("selected_answer")
    @classmethod
    def validate_answer(cls, v: str) -> str:
        v = v.upper().strip()
        if v not in ("A", "B", "C", "D"):
            raise ValueError("selected_answer must be A, B, C, or D")
        return v


class LearningFeedback(BaseModel):
    is_correct: bool
    correct_answer: str
    detected_misconception: Optional[str] = None
    misconception_category: Optional[str] = None
    reasoning_analysis: str
    concept_understanding: str
    explanation: str
    recommended_learning_action: str
    suggested_difficulty: str
    previous_mastery: float
    new_mastery: float
    mastery_level: str
    revision_scheduled: Optional[dict] = None
    is_ai_generated: bool = False


# ── Dashboard ──────────────────────────────────────────────────────────────────

class DashboardOut(BaseModel):
    student: StudentOut
    overall_mastery: float
    enrolled_subjects_count: int
    concepts_mastered: int
    concepts_needing_attention: list[dict]
    recent_assessments: list[dict]
    streak_days: int
    weekly_progress: list[dict]
    upcoming_revisions: list[dict]
    recommended_next_activity: Optional[dict]
    subject_masteries: list[dict]
    mastery_by_concept: list[dict]
