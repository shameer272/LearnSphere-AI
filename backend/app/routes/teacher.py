"""
Teacher analytics router for LearnSphere AI — B.Tech Computer Science & Engineering.
Calculates class intelligence strictly from genuine database records and verified activity.
Never displays hardcoded, fake, or synthetic demonstration data.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, not_
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import (
    Student,
    Subject,
    Concept,
    ConceptMastery,
    Misconception,
    AnswerHistory,
    Assessment,
)
from app.utils.helpers import safe_average
from app.utils.security import get_current_teacher

router = APIRouter(prefix="/teacher", tags=["teacher"])


@router.get("/analytics")
def get_teacher_analytics(
    current_teacher: Student = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    """
    Protected endpoint: Aggregate cohort analytics across genuine registered students.
    Strictly database-driven:
    - Enforces backend role verification (RBAC) via get_current_teacher (403 for non-teachers).
    - Excludes unassessed students from mastery averages.
    - Missing mastery is never treated as 0%.
    - Empty states clearly signaled when no genuine data exists.
    """
    # 1. Total genuine registered students (strictly role='student', excluding test/faculty/admin accounts)
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

    # Deduplicate strictly by ID and normalized email
    seen_ids = set()
    seen_emails = set()
    genuine_students = []

    for s in raw_students:
        norm_email = s.email.strip().lower() if s.email else ""
        if s.id in seen_ids or (norm_email and norm_email in seen_emails):
            continue
        seen_ids.add(s.id)
        if norm_email:
            seen_emails.add(norm_email)
        genuine_students.append(s)

    students = genuine_students
    total_students = len(students)
    student_ids = [s.id for s in students]

    subjects = db.query(Subject).order_by(Subject.order_index).all()
    concepts = db.query(Concept).all()

    # Query only concept mastery records that have actual student attempts by genuine registered students
    if student_ids:
        attempted_masteries = (
            db.query(ConceptMastery)
            .filter(
                ConceptMastery.student_id.in_(student_ids),
                ConceptMastery.attempts > 0,
            )
            .all()
        )
        total_answers_count = db.query(AnswerHistory).filter(AnswerHistory.student_id.in_(student_ids)).count()
        total_assessments_count = db.query(Assessment).filter(Assessment.student_id.in_(student_ids)).count()
    else:
        attempted_masteries = []
        total_answers_count = 0
        total_assessments_count = 0

    # 2. Map actual attempted masteries per student
    student_attempt_map: dict[int, list[float]] = {}
    for m in attempted_masteries:
        student_attempt_map.setdefault(m.student_id, []).append(m.mastery_score)

    # 3. Calculate genuine student performance
    student_profiles = []
    assessed_students = []

    for s in students:
        scores = student_attempt_map.get(s.id, [])
        has_assessed = len(scores) > 0
        avg_score = round(sum(scores) / len(scores), 1) if has_assessed else None

        info = {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "degree": s.degree,
            "level": s.learning_level,
            "has_assessed": has_assessed,
            "concepts_attempted": len(scores),
            "overall_mastery": avg_score,
            "enrolled_subjects": [es.subject.name for es in s.enrolled_subjects if es.subject],
        }
        student_profiles.append(info)
        if has_assessed:
            assessed_students.append(info)

    # 4. Overall Class Average Mastery (strictly among assessed students)
    if assessed_students:
        valid_class_scores = [s["overall_mastery"] for s in assessed_students if s["overall_mastery"] is not None]
        average_class_mastery = round(sum(valid_class_scores) / len(valid_class_scores), 1) if valid_class_scores else None
    else:
        average_class_mastery = None

    # 5. Intervention Watchlist: ONLY students who have assessed AND scored < 40%
    struggling_students = [
        s for s in assessed_students
        if s["overall_mastery"] is not None and s["overall_mastery"] < 40.0
    ]

    # 6. Subject Analytics: calculated only from actual student activity
    subject_analytics = []
    for subj in subjects:
        subj_cids = {c.id for c in subj.concepts}
        subj_ms = [m for m in attempted_masteries if m.concept_id in subj_cids]
        scores = [m.mastery_score for m in subj_ms]
        avg_score = round(sum(scores) / len(scores), 1) if scores else None

        subject_analytics.append({
            "subject_id": subj.id,
            "subject_name": subj.name,
            "subject_code": subj.code,
            "category": subj.category,
            "icon": subj.icon,
            "average_mastery": avg_score,
            "has_data": len(scores) > 0,
            "concepts_count": len(subj.concepts),
            "students_assessed": len(set(m.student_id for m in subj_ms)),
            "weak_count": sum(1 for s in scores if s < 40),
            "developing_count": sum(1 for s in scores if 40 <= s <= 70),
            "mastered_count": sum(1 for s in scores if s > 70),
        })

    # 7. Concept Analytics: calculated strictly from attempted concepts
    concept_analytics = []
    for c in concepts:
        c_ms = [m for m in attempted_masteries if m.concept_id == c.id]
        scores = [m.mastery_score for m in c_ms]
        avg = round(sum(scores) / len(scores), 1) if scores else None
        weak_count = sum(1 for s in scores if s < 40)
        dev_count = sum(1 for s in scores if 40 <= s <= 70)
        mastered_count = sum(1 for s in scores if s > 70)

        concept_analytics.append({
            "concept_id": c.id,
            "concept_name": c.name,
            "subject_name": c.subject.name if c.subject else "Computer Science",
            "subject_code": c.subject.code if c.subject else "CS",
            "average_mastery": avg,
            "has_data": len(scores) > 0,
            "students_assessed": len(scores),
            "students_weak": weak_count,
            "students_developing": dev_count,
            "students_mastered": mastered_count,
        })

    # 8. Weakest concepts: strictly concepts with actual recorded attempts
    most_difficult = sorted(
        [c for c in concept_analytics if c["students_assessed"] > 0 and c["average_mastery"] is not None],
        key=lambda x: x["average_mastery"]
    )[:8]

    # 9. Real Misconceptions detected from live learning attempts by genuine students
    recent_misconceptions = []
    if student_ids:
        recent_misconceptions = (
            db.query(Misconception)
            .filter(Misconception.student_id.in_(student_ids))
            .order_by(Misconception.detected_at.desc())
            .limit(10)
            .all()
        )
    misconception_feed = [
        {
            "id": m.id,
            "student_name": m.student.name if m.student else "Student",
            "student_email": m.student.email if m.student else "",
            "concept_name": m.concept.name if m.concept else "CS Concept",
            "misconception_type": m.misconception_type,
            "description": m.description,
            "detected_at": m.detected_at.isoformat(),
        }
        for m in recent_misconceptions
    ]

    return {
        "total_students": total_students,
        "assessed_students_count": len(assessed_students),
        "has_registered_students": total_students > 0,
        "has_assessment_data": len(assessed_students) > 0,
        "has_learning_activity": total_answers_count > 0 or total_assessments_count > 0,
        "average_class_mastery": average_class_mastery,
        "students": student_profiles,
        "struggling_students": struggling_students,
        "subject_analytics": subject_analytics,
        "concept_analytics": concept_analytics,
        "most_difficult_concepts": most_difficult,
        "recent_misconceptions": misconception_feed,
    }
