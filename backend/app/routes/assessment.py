"""
Assessment router for LearnSphere AI — B.Tech Computer Science & Engineering.
Provides diagnostic assessment generation and submission.
"""
from datetime import datetime
from typing import Optional
import random

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import (
    Assessment,
    AnswerHistory,
    ConceptMastery,
    Concept,
    Question,
    Student,
    Subject,
)
from app.schemas.schemas import AssessmentSubmit, AssessmentResult
from app.services.mastery_service import update_mastery, get_mastery_level
from app.services.revision_service import schedule_revision
from app.ai.fallback_questions import FALLBACK_QUESTIONS

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.get("/questions")
def get_diagnostic_questions(
    student_id: Optional[int] = Query(default=None),
    subject_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    Return diagnostic questions for B.Tech CSE subjects.
    Optionally scoped to a specific subject, or across student's enrolled subjects.
    """
    selected_subject = None
    if subject_id:
        selected_subject = db.query(Subject).filter(Subject.id == subject_id).first()

    if not selected_subject and student_id:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student and student.enrolled_subjects:
            selected_subject = student.enrolled_subjects[0].subject

    if not selected_subject:
        # Default to Python Programming or first subject
        selected_subject = db.query(Subject).filter(Subject.code == "CS-PY").first()
        if not selected_subject:
            selected_subject = db.query(Subject).first()

    if not selected_subject:
        raise HTTPException(status_code=500, detail="No subjects found in the database.")

    # Fetch concepts for this subject
    concepts = selected_subject.concepts
    if not concepts:
        concepts = db.query(Concept).limit(5).all()

    # Query questions from DB for these concepts
    concept_ids = [c.id for c in concepts]
    questions = db.query(Question).filter(Question.concept_id.in_(concept_ids)).all()

    # If questions in DB are fewer than 5, supplement from FALLBACK_QUESTIONS
    if len(questions) < 5:
        more_questions = db.query(Question).limit(10).all()
        questions.extend([q for q in more_questions if q not in questions])

    # Format questions (do not leak correct answer to client)
    formatted = []
    for q in questions[:10]:
        formatted.append({
            "id": q.id,
            "subject_id": q.subject_id,
            "concept_id": q.concept_id,
            "concept_name": q.concept.name if q.concept else selected_subject.name,
            "question_type": q.question_type or "mcq",
            "question_text": q.question_text,
            "code_snippet": q.code_snippet,
            "options": q.options,
            "difficulty": q.difficulty,
        })

    return {
        "subject_id": selected_subject.id,
        "subject_name": selected_subject.name,
        "subject_code": selected_subject.code,
        "total_questions": len(formatted),
        "questions": formatted,
    }


@router.post("/submit", response_model=AssessmentResult)
def submit_diagnostic(payload: AssessmentSubmit, db: Session = Depends(get_db)):
    """
    Score diagnostic assessment, initialize concept mastery, schedule revisions,
    and persist assessment result in the database.
    """
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # Deduplicate submitted answers by question_id (keep latest)
    seen_answers = {}
    for ans in payload.answers:
        seen_answers[ans.question_id] = ans
    answers = list(seen_answers.values())

    total = len(answers)
    if total == 0:
        raise HTTPException(status_code=400, detail="No answers provided.")

    correct_count = 0
    concept_stats: dict[int, dict] = {}

    for ans in answers:
        q = db.query(Question).filter(Question.id == ans.question_id).first()
        if not q:
            continue

        is_correct = ans.selected_answer.upper().strip() == q.correct_answer.upper().strip()
        if is_correct:
            correct_count += 1

        cid = q.concept_id
        if cid not in concept_stats:
            concept_stats[cid] = {"total": 0, "correct": 0, "subject_id": q.subject_id}
        concept_stats[cid]["total"] += 1
        if is_correct:
            concept_stats[cid]["correct"] += 1

        # Record answer history
        history = AnswerHistory(
            student_id=payload.student_id,
            subject_id=q.subject_id,
            question_id=q.id,
            concept_id=q.concept_id,
            selected_answer=ans.selected_answer,
            is_correct=is_correct,
            ai_feedback={
                "explanation": q.explanation or "Diagnostic assessment response.",
                "is_correct": is_correct,
            },
            answered_at=datetime.utcnow(),
        )
        db.add(history)

    score_pct = round((correct_count / total) * 100.0, 1) if total > 0 else 0.0

    # Save Assessment record
    assessment = Assessment(
        student_id=payload.student_id,
        subject_id=payload.subject_id,
        completed_at=datetime.utcnow(),
        total_questions=total,
        correct_answers=correct_count,
        score_percentage=score_pct,
    )
    db.add(assessment)
    db.flush()

    # Initialize concept mastery and schedule spaced revisions
    mastery_initialized = {}
    recommendations = []

    for cid, stats in concept_stats.items():
        concept = db.query(Concept).filter(Concept.id == cid).first()
        concept_accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0.0
        initial_score = round(concept_accuracy * 85.0 + 10.0, 1)  # base between 10% and 95%

        mastery = (
            db.query(ConceptMastery)
            .filter(
                ConceptMastery.student_id == payload.student_id,
                ConceptMastery.concept_id == cid,
            )
            .first()
        )
        if not mastery:
            mastery = ConceptMastery(
                student_id=payload.student_id,
                subject_id=stats["subject_id"],
                concept_id=cid,
                mastery_score=initial_score,
                attempts=stats["total"],
                correct_count=stats["correct"],
                incorrect_count=stats["total"] - stats["correct"],
                last_assessed=datetime.utcnow(),
                current_difficulty="medium" if initial_score >= 50 else "easy",
            )
            db.add(mastery)
        else:
            mastery.mastery_score = initial_score
            mastery.attempts += stats["total"]
            mastery.correct_count += stats["correct"]
            mastery.incorrect_count += (stats["total"] - stats["correct"])
            mastery.last_assessed = datetime.utcnow()

        if concept:
            mastery_initialized[concept.name] = initial_score
            if initial_score < 50:
                recommendations.append(f"Focus on {concept.name} (Mastery: {initial_score}%)")

            # Schedule spaced repetition
            schedule_revision(
                student_id=payload.student_id,
                concept_id=cid,
                mastery_score=initial_score,
                db=db,
                subject_id=stats["subject_id"],
            )

    db.commit()

    if not recommendations:
        recommendations.append("Great baseline performance! Advance to higher-tier algorithm questions.")

    return AssessmentResult(
        assessment_id=assessment.id,
        total_questions=total,
        correct_answers=correct_count,
        score_percentage=score_pct,
        completed_at=assessment.completed_at,
        mastery_initialized=mastery_initialized,
        recommendations=recommendations,
    )
