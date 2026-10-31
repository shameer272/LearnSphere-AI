"""
Students router for LearnSphere AI — B.Tech Computer Science & Engineering.
Provides student dashboards, mastery breakdown, and profile endpoints.
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, not_
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import (
    Student,
    Subject,
    Concept,
    ConceptMastery,
    Assessment,
    AnswerHistory,
    RevisionSchedule,
    StudentSubject,
)
from app.schemas.schemas import StudentOut, DashboardOut, EnrolledSubjectOut
from app.services.revision_service import get_upcoming_revisions, calculate_forgetting_risk
from app.services.mastery_service import get_mastery_level
from app.utils.helpers import safe_average
from app.utils.security import get_optional_student

router = APIRouter(tags=["students"])


def _build_student_out(student: Student) -> StudentOut:
    enrolled = [
        EnrolledSubjectOut(
            id=es.subject.id,
            name=es.subject.name,
            code=es.subject.code,
            category=es.subject.category,
            icon=es.subject.icon,
            target_level=es.target_level,
            enrolled_at=es.enrolled_at,
        )
        for es in student.enrolled_subjects if es.subject
    ]
    return StudentOut(
        id=student.id,
        name=student.name,
        email=student.email,
        learning_level=student.learning_level,
        degree=student.degree,
        created_at=student.created_at,
        last_active=student.last_active,
        streak_days=student.streak_days,
        enrolled_subjects=enrolled,
    )


@router.get("/students", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    """List all genuine registered B.Tech students."""
    student_query = (
        db.query(Student)
        .filter(func.lower(Student.role) == "student")
        .filter(not_(func.lower(Student.email).like("test_student%")))
        .filter(not_(func.lower(Student.email).like("%@learnsphere.edu")))
        .filter(not_(func.lower(Student.email).like("%automated%")))
        .filter(not_(func.lower(Student.email).like("%test%@%")))
        .filter(not_(func.lower(Student.name).like("test student%")))
    )
    raw_students = student_query.order_by(Student.id.asc()).all()

    seen_ids = set()
    seen_emails = set()
    genuine = []
    for s in raw_students:
        norm = s.email.strip().lower() if s.email else ""
        if s.id in seen_ids or (norm and norm in seen_emails):
            continue
        seen_ids.add(s.id)
        if norm:
            seen_emails.add(norm)
        genuine.append(s)

    return [_build_student_out(s) for s in genuine]


@router.get("/students/{student_id}", response_model=StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Return a student's basic profile."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return _build_student_out(student)


@router.get("/students/{student_id}/dashboard")
def get_dashboard(
    student_id: int,
    subject_id: Optional[int] = Query(default=None),
    current_student: Optional[Student] = Depends(get_optional_student),
    db: Session = Depends(get_db),
):
    """
    Return full personalized dashboard data for an authenticated B.Tech student.
    All data is derived from actual database records.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # Get enrolled subjects or all subjects if not yet enrolled
    enrolled_subject_ids = [es.subject_id for es in student.enrolled_subjects]
    if enrolled_subject_ids:
        subjects_query = db.query(Subject).filter(Subject.id.in_(enrolled_subject_ids))
    else:
        subjects_query = db.query(Subject).order_by(Subject.order_index).limit(5)
    subjects = subjects_query.all()

    # If subject_id filter is passed, focus on that subject
    if subject_id:
        target_subject = db.query(Subject).filter(Subject.id == subject_id).first()
        target_concepts = target_subject.concepts if target_subject else []
    else:
        # Aggregate across enrolled subjects
        target_concepts = []
        for s in subjects:
            target_concepts.extend(s.concepts)

    if not target_concepts:
        # Fallback to all concepts
        target_concepts = db.query(Concept).all()

    concept_ids = [c.id for c in target_concepts]
    masteries = (
        db.query(ConceptMastery)
        .filter(
            ConceptMastery.student_id == student_id,
            ConceptMastery.concept_id.in_(concept_ids),
        )
        .all()
    )
    mastery_map = {m.concept_id: m for m in masteries}

    # Concept-wise mastery items
    mastery_by_concept = []
    for c in target_concepts:
        m = mastery_map.get(c.id)
        score = m.mastery_score if m else 0.0
        mastery_by_concept.append({
            "concept_id": c.id,
            "concept_name": c.name,
            "subject_id": c.subject_id,
            "subject_name": c.subject.name if c.subject else "Computer Science",
            "mastery_score": score,
            "attempts": m.attempts if m else 0,
            "correct_count": m.correct_count if m else 0,
            "incorrect_count": m.incorrect_count if m else 0,
            "current_difficulty": m.current_difficulty if m else "easy",
            "last_assessed": m.last_assessed.isoformat() if (m and m.last_assessed) else None,
            "mastery_level": get_mastery_level(score),
            "forgetting_risk": calculate_forgetting_risk(m.last_assessed if m else None, score),
        })

    # Subject-wise progress summary
    subject_masteries = []
    for s in subjects:
        s_concepts = s.concepts
        s_scores = [mastery_map[c.id].mastery_score for c in s_concepts if c.id in mastery_map]
        avg = safe_average(s_scores) if s_scores else 0.0
        subject_masteries.append({
            "subject_id": s.id,
            "subject_name": s.name,
            "subject_code": s.code,
            "category": s.category,
            "icon": s.icon,
            "average_mastery": round(avg, 1),
            "concepts_count": len(s_concepts),
            "mastered_count": sum(1 for score in s_scores if score >= 70),
        })

    overall_mastery = safe_average([item["mastery_score"] for item in mastery_by_concept])
    concepts_mastered = sum(1 for item in mastery_by_concept if item["mastery_score"] >= 70)
    concepts_needing_attention = [
        item for item in mastery_by_concept if item["mastery_score"] < 40
    ]

    # Recent assessments (last 5)
    recent_assessments_raw = (
        db.query(Assessment)
        .filter(Assessment.student_id == student_id)
        .order_by(Assessment.completed_at.desc())
        .limit(5)
        .all()
    )
    recent_assessments = [
        {
            "id": a.id,
            "completed_at": a.completed_at.isoformat(),
            "total_questions": a.total_questions,
            "correct_answers": a.correct_answers,
            "score_percentage": a.score_percentage,
            "subject_name": a.subject.name if a.subject else "B.Tech CSE Core",
        }
        for a in recent_assessments_raw
    ]

    # Weekly learning activity
    now = datetime.utcnow()
    weekly_progress = []
    for i in range(6, -1, -1):
        day_date = (now - timedelta(days=i)).date()
        day_start = datetime.combine(day_date, datetime.min.time())
        day_end = datetime.combine(day_date, datetime.max.time())
        day_count = (
            db.query(AnswerHistory)
            .filter(
                AnswerHistory.student_id == student_id,
                AnswerHistory.answered_at >= day_start,
                AnswerHistory.answered_at <= day_end,
            )
            .count()
        )
        weekly_progress.append({
            "day": day_date.strftime("%a"),
            "date": day_date.isoformat(),
            "questions_answered": day_count,
        })

    # Upcoming revisions
    revisions_raw = get_upcoming_revisions(student_id, db, subject_id=subject_id)
    upcoming_revisions = [
        {
            "id": r.id,
            "concept_id": r.concept_id,
            "concept_name": r.concept.name if r.concept else "CS Concept",
            "subject_name": r.concept.subject.name if (r.concept and r.concept.subject) else "Computer Science",
            "scheduled_date": r.scheduled_date.isoformat(),
            "priority": r.priority,
            "reason": r.reason,
            "is_completed": r.is_completed,
        }
        for r in revisions_raw
    ]

    # Recommended next activity
    recommended_activity = None
    if concepts_needing_attention:
        weakest = min(concepts_needing_attention, key=lambda x: x["mastery_score"])
        recommended_activity = {
            "type": "reinforce_weak_concept",
            "concept_id": weakest["concept_id"],
            "concept_name": weakest["concept_name"],
            "subject_id": weakest["subject_id"],
            "subject_name": weakest["subject_name"],
            "current_mastery": weakest["mastery_score"],
            "action_text": f"Reinforce {weakest['concept_name']} in {weakest['subject_name']}",
        }
    elif mastery_by_concept:
        next_concept = min(mastery_by_concept, key=lambda x: x["mastery_score"])
        recommended_activity = {
            "type": "adaptive_practice",
            "concept_id": next_concept["concept_id"],
            "concept_name": next_concept["concept_name"],
            "subject_id": next_concept["subject_id"],
            "subject_name": next_concept["subject_name"],
            "current_mastery": next_concept["mastery_score"],
            "action_text": f"Practice {next_concept['concept_name']}",
        }

    return {
        "student": _build_student_out(student),
        "overall_mastery": round(overall_mastery, 1),
        "enrolled_subjects_count": len(enrolled_subject_ids),
        "concepts_mastered": concepts_mastered,
        "concepts_needing_attention": concepts_needing_attention,
        "recent_assessments": recent_assessments,
        "streak_days": student.streak_days,
        "weekly_progress": weekly_progress,
        "upcoming_revisions": upcoming_revisions,
        "recommended_next_activity": recommended_activity,
        "subject_masteries": subject_masteries,
        "mastery_by_concept": mastery_by_concept,
    }


@router.get("/students/{student_id}/mastery")
def get_student_mastery(student_id: int, db: Session = Depends(get_db)):
    """Return student's full mastery profile across B.Tech CSE subjects."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    masteries = db.query(ConceptMastery).filter(ConceptMastery.student_id == student_id).all()
    results = []
    for m in masteries:
        concept = m.concept
        if not concept:
            continue
        results.append({
            "concept_id": concept.id,
            "concept_name": concept.name,
            "subject_id": concept.subject_id,
            "subject_name": concept.subject.name if concept.subject else "Computer Science",
            "mastery_score": m.mastery_score,
            "attempts": m.attempts,
            "correct_count": m.correct_count,
            "incorrect_count": m.incorrect_count,
            "last_assessed": m.last_assessed.isoformat() if m.last_assessed else None,
            "current_difficulty": m.current_difficulty,
            "mastery_level": get_mastery_level(m.mastery_score),
            "forgetting_risk": calculate_forgetting_risk(m.last_assessed, m.mastery_score),
        })

    return results
