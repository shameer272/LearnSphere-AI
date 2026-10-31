"""
Authentication router for LearnSphere AI — B.Tech Computer Science & Engineering.
Provides registration, login, profile retrieval, and enrollment management.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import Student, Subject, StudentSubject, ConceptMastery
from app.schemas.schemas import (
    StudentCreate,
    StudentLogin,
    StudentOut,
    AuthToken,
    StudentProfileUpdate,
    EnrolledSubjectOut,
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_student,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _build_student_out(student: Student, db: Session) -> StudentOut:
    """Helper to assemble a StudentOut model with enrolled subjects."""
    enrolled = []
    for es in student.enrolled_subjects:
        subj = es.subject
        if subj:
            enrolled.append(
                EnrolledSubjectOut(
                    id=subj.id,
                    name=subj.name,
                    code=subj.code,
                    category=subj.category,
                    icon=subj.icon,
                    target_level=es.target_level,
                    enrolled_at=es.enrolled_at,
                )
            )

    return StudentOut(
        id=student.id,
        name=student.name,
        email=student.email,
        learning_level=student.learning_level,
        degree=student.degree,
        role=student.role,
        created_at=student.created_at,
        last_active=student.last_active,
        streak_days=student.streak_days,
        enrolled_subjects=enrolled,
    )


@router.post("/register", response_model=AuthToken, status_code=status.HTTP_201_CREATED)
def register(payload: StudentCreate, db: Session = Depends(get_db)):
    """Register a new B.Tech CSE student."""
    email_clean = payload.email.strip().lower()
    existing = db.query(Student).filter(func.lower(func.trim(Student.email)) == email_clean).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email address already exists. Please log in.",
        )

    # Hash password securely
    pwd_hash = hash_password(payload.password)

    student = Student(
        name=payload.name.strip(),
        email=email_clean,
        password_hash=pwd_hash,
        learning_level=payload.learning_level,
        degree=payload.degree,
        role="student",  # Never allow role escalation from registration payload
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow(),
        streak_days=1,
    )
    db.add(student)
    db.flush()

    # Enroll in chosen subjects, or default to core Programming & CS Fundamentals
    raw_subject_ids = payload.selected_subject_ids or []
    subject_ids = list(dict.fromkeys(raw_subject_ids))  # deduplicate
    if not subject_ids:
        # Default to Python, React, FastAPI, DSA
        defaults = db.query(Subject).filter(Subject.code.in_(["CS-PY", "CS-REACT", "CS-FASTAPI", "CS-DSA"])).all()
        subject_ids = [s.id for s in defaults]

    for sid in subject_ids:
        subj = db.query(Subject).filter(Subject.id == sid).first()
        if subj:
            existing_enroll = db.query(StudentSubject).filter(
                StudentSubject.student_id == student.id,
                StudentSubject.subject_id == subj.id,
            ).first()
            if not existing_enroll:
                enrollment = StudentSubject(
                    student_id=student.id,
                    subject_id=subj.id,
                    target_level=payload.learning_level,
                    enrolled_at=datetime.utcnow(),
                )
                db.add(enrollment)

            # Initialize zero mastery for the subject's concepts
            for concept in subj.concepts:
                existing_m = db.query(ConceptMastery).filter(
                    ConceptMastery.student_id == student.id,
                    ConceptMastery.concept_id == concept.id,
                ).first()
                if not existing_m:
                    mastery = ConceptMastery(
                        student_id=student.id,
                        subject_id=subj.id,
                        concept_id=concept.id,
                        mastery_score=0.0,
                        attempts=0,
                        correct_count=0,
                        incorrect_count=0,
                        current_difficulty="easy",
                    )
                    db.add(mastery)

    db.commit()
    db.refresh(student)

    # Issue token with verified database role
    token = create_access_token({
        "sub": str(student.id),
        "email": student.email,
        "name": student.name,
        "role": student.role,
    })
    student_out = _build_student_out(student, db)

    return AuthToken(access_token=token, student=student_out)


@router.post("/login", response_model=AuthToken)
def login(payload: StudentLogin, db: Session = Depends(get_db)):
    """Authenticate an existing B.Tech CSE student."""
    email_clean = payload.email.strip().lower()
    student = db.query(Student).filter(Student.email == email_clean).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password. Please check your credentials.",
        )

    # Verify password
    if not verify_password(payload.password, student.password_hash):
        # Support default demo password fallback if password_hash was initialized for demo
        if not (student.password_hash == "" and payload.password in ("Password123!", "demo123")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password. Please check your credentials.",
            )

    # Update last active
    student.last_active = datetime.utcnow()
    db.commit()

    token = create_access_token({
        "sub": str(student.id),
        "email": student.email,
        "name": student.name,
        "role": student.role,
    })
    student_out = _build_student_out(student, db)

    return AuthToken(access_token=token, student=student_out)


@router.get("/me", response_model=StudentOut)
def get_current_user_profile(
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Retrieve currently authenticated student profile."""
    return _build_student_out(student, db)


@router.put("/profile", response_model=StudentOut)
def update_profile(
    payload: StudentProfileUpdate,
    student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Update profile and enrolled B.Tech CSE subjects."""
    if payload.name:
        student.name = payload.name.strip()
    if payload.learning_level:
        student.learning_level = payload.learning_level

    if payload.selected_subject_ids is not None:
        # Reconcile enrolled subjects
        current_enrolled_ids = {es.subject_id for es in student.enrolled_subjects}
        new_ids = set(payload.selected_subject_ids)

        # Remove unselected
        for es in list(student.enrolled_subjects):
            if es.subject_id not in new_ids:
                db.delete(es)

        # Add newly selected
        for sid in new_ids:
            if sid not in current_enrolled_ids:
                subj = db.query(Subject).filter(Subject.id == sid).first()
                if subj:
                    db.add(
                        StudentSubject(
                            student_id=student.id,
                            subject_id=subj.id,
                            target_level=student.learning_level,
                            enrolled_at=datetime.utcnow(),
                        )
                    )
                    for concept in subj.concepts:
                        if not db.query(ConceptMastery).filter(
                            ConceptMastery.student_id == student.id,
                            ConceptMastery.concept_id == concept.id,
                        ).first():
                            db.add(
                                ConceptMastery(
                                    student_id=student.id,
                                    subject_id=subj.id,
                                    concept_id=concept.id,
                                    mastery_score=0.0,
                                    attempts=0,
                                    current_difficulty="easy",
                                )
                            )

    db.commit()
    db.refresh(student)
    return _build_student_out(student, db)
