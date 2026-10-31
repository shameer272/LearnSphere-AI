"""
SQLAlchemy ORM models for LearnSphere AI — B.Tech Computer Science and Engineering.
"""
import json
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.types import TypeDecorator, TEXT

from app.database.db import Base


class JSONEncodedList(TypeDecorator):
    """Stores a Python list as a JSON-encoded string in TEXT column."""
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return "[]"
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return []


class JSONEncodedDict(TypeDecorator):
    """Stores a Python dict as a JSON-encoded string in TEXT column."""
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is None:
            return "{}"
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return {}


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    learning_level: Mapped[str] = mapped_column(String(50), default="Intermediate")
    degree: Mapped[str] = mapped_column(String(100), default="B.Tech Computer Science & Engineering")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    streak_days: Mapped[int] = mapped_column(Integer, default=1)
    role: Mapped[str] = mapped_column(String(20), default="student", nullable=False)

    @validates("email")
    def validate_email(self, key, address):
        if not address:
            raise ValueError("Student email cannot be empty.")
        return address.strip().lower()

    # Relationships
    enrolled_subjects: Mapped[list["StudentSubject"]] = relationship(
        "StudentSubject", back_populates="student", cascade="all, delete-orphan"
    )
    assessments: Mapped[list["Assessment"]] = relationship("Assessment", back_populates="student", cascade="all, delete-orphan")
    answer_histories: Mapped[list["AnswerHistory"]] = relationship("AnswerHistory", back_populates="student", cascade="all, delete-orphan")
    concept_masteries: Mapped[list["ConceptMastery"]] = relationship("ConceptMastery", back_populates="student", cascade="all, delete-orphan")
    misconceptions: Mapped[list["Misconception"]] = relationship("Misconception", back_populates="student", cascade="all, delete-orphan")
    revision_schedules: Mapped[list["RevisionSchedule"]] = relationship("RevisionSchedule", back_populates="student", cascade="all, delete-orphan")


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    icon: Mapped[str] = mapped_column(String(50), default="FiCode")
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    topics: Mapped[list["Topic"]] = relationship("Topic", back_populates="subject", cascade="all, delete-orphan")
    concepts: Mapped[list["Concept"]] = relationship("Concept", back_populates="subject", cascade="all, delete-orphan")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="subject")
    enrolled_students: Mapped[list["StudentSubject"]] = relationship("StudentSubject", back_populates="subject")


class Topic(Base):
    __tablename__ = "topics"
    __table_args__ = (UniqueConstraint("subject_id", "name", name="uq_subject_topic"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    # Relationships
    subject: Mapped["Subject"] = relationship("Subject", back_populates="topics")
    concepts: Mapped[list["Concept"]] = relationship("Concept", back_populates="topic")


class Concept(Base):
    __tablename__ = "concepts"
    __table_args__ = (UniqueConstraint("subject_id", "name", name="uq_subject_concept"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    topic_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("topics.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    prerequisites: Mapped[list] = mapped_column(JSONEncodedList, default=list)

    # Relationships
    subject: Mapped["Subject"] = relationship("Subject", back_populates="concepts")
    topic: Mapped[Optional["Topic"]] = relationship("Topic", back_populates="concepts")
    questions: Mapped[list["Question"]] = relationship("Question", back_populates="concept")
    concept_masteries: Mapped[list["ConceptMastery"]] = relationship("ConceptMastery", back_populates="concept")
    answer_histories: Mapped[list["AnswerHistory"]] = relationship("AnswerHistory", back_populates="concept")
    misconceptions: Mapped[list["Misconception"]] = relationship("Misconception", back_populates="concept")
    revision_schedules: Mapped[list["RevisionSchedule"]] = relationship("RevisionSchedule", back_populates="concept")


class StudentSubject(Base):
    __tablename__ = "student_subjects"
    __table_args__ = (UniqueConstraint("student_id", "subject_id", name="uq_student_subject"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    enrolled_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    target_level: Mapped[str] = mapped_column(String(50), default="Intermediate")

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="enrolled_subjects")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="enrolled_students")


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (UniqueConstraint("concept_id", "question_text", name="uq_concept_question"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False, index=True)
    concept_id: Mapped[int] = mapped_column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    question_type: Mapped[str] = mapped_column(String(50), default="mcq")  # mcq, output_prediction, code_debugging, conceptual, sql_query, scenario
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    code_snippet: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    options: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    correct_answer: Mapped[str] = mapped_column(String(10), nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    difficulty: Mapped[str] = mapped_column(String(20), default="medium")  # easy, medium, hard
    misconception_targets: Mapped[list] = mapped_column(JSONEncodedList, default=list)
    is_ai_generated: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    subject: Mapped["Subject"] = relationship("Subject", back_populates="questions")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="questions")
    answer_histories: Mapped[list["AnswerHistory"]] = relationship("AnswerHistory", back_populates="question")


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=True, index=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total_questions: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    score_percentage: Mapped[float] = mapped_column(Float, default=0.0)

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="assessments")
    subject: Mapped[Optional["Subject"]] = relationship("Subject")


class AnswerHistory(Base):
    __tablename__ = "answer_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=True, index=True)
    question_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("questions.id"), nullable=True)
    concept_id: Mapped[int] = mapped_column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    selected_answer: Mapped[str] = mapped_column(String(10), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    written_reasoning: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_feedback: Mapped[dict] = mapped_column(JSONEncodedDict, default=dict)
    time_taken_seconds: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    answered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="answer_histories")
    subject: Mapped[Optional["Subject"]] = relationship("Subject")
    question: Mapped[Optional["Question"]] = relationship("Question", back_populates="answer_histories")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="answer_histories")
    misconceptions: Mapped[list["Misconception"]] = relationship("Misconception", back_populates="answer_history")


class ConceptMastery(Base):
    __tablename__ = "concept_mastery"
    __table_args__ = (UniqueConstraint("student_id", "concept_id", name="uq_student_concept"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=True, index=True)
    concept_id: Mapped[int] = mapped_column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    mastery_score: Mapped[float] = mapped_column(Float, default=0.0)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    correct_count: Mapped[int] = mapped_column(Integer, default=0)
    incorrect_count: Mapped[int] = mapped_column(Integer, default=0)
    last_assessed: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    current_difficulty: Mapped[str] = mapped_column(String(20), default="easy")

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="concept_masteries")
    subject: Mapped[Optional["Subject"]] = relationship("Subject")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="concept_masteries")


class Misconception(Base):
    __tablename__ = "misconceptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=True, index=True)
    concept_id: Mapped[int] = mapped_column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    answer_history_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("answer_history.id"), nullable=True)
    misconception_type: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="misconceptions")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="misconceptions")
    answer_history: Mapped[Optional["AnswerHistory"]] = relationship("AnswerHistory", back_populates="misconceptions")


class RevisionSchedule(Base):
    __tablename__ = "revision_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    subject_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=True, index=True)
    concept_id: Mapped[int] = mapped_column(Integer, ForeignKey("concepts.id"), nullable=False, index=True)
    scheduled_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    priority: Mapped[str] = mapped_column(String(20), default="medium")
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    student: Mapped["Student"] = relationship("Student", back_populates="revision_schedules")
    concept: Mapped["Concept"] = relationship("Concept", back_populates="revision_schedules")
