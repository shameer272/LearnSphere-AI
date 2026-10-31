"""
Revisions router for LearnSphere AI — B.Tech Computer Science & Engineering.
Manages spaced repetition schedules and revision completions.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import RevisionSchedule, Student, ConceptMastery

router = APIRouter(prefix="/revisions", tags=["revisions"])


class CompleteRevisionPayload(BaseModel):
    revision_id: int
    student_id: int


@router.get("/{student_id}")
def get_revisions(
    student_id: int,
    subject_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """Return all pending and completed revisions for a student."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    query = db.query(RevisionSchedule).filter(RevisionSchedule.student_id == student_id)
    if subject_id:
        query = query.filter(RevisionSchedule.subject_id == subject_id)

    revisions = query.order_by(RevisionSchedule.scheduled_date.asc()).all()

    pending = []
    completed = []

    for r in revisions:
        concept = r.concept
        item = {
            "id": r.id,
            "concept_id": r.concept_id,
            "concept_name": concept.name if concept else "CS Concept",
            "subject_name": concept.subject.name if (concept and concept.subject) else "Computer Science",
            "subject_code": concept.subject.code if (concept and concept.subject) else "CS",
            "scheduled_date": r.scheduled_date.isoformat(),
            "priority": r.priority,
            "reason": r.reason,
            "is_completed": r.is_completed,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
        }
        if r.is_completed:
            completed.append(item)
        else:
            pending.append(item)

    return {
        "student_id": student_id,
        "total_pending": len(pending),
        "total_completed": len(completed),
        "pending": pending,
        "completed": completed,
    }


@router.post("/complete")
def complete_revision(payload: CompleteRevisionPayload, db: Session = Depends(get_db)):
    """Mark a spaced revision item as completed."""
    rev = (
        db.query(RevisionSchedule)
        .filter(
            RevisionSchedule.id == payload.revision_id,
            RevisionSchedule.student_id == payload.student_id,
        )
        .first()
    )
    if not rev:
        raise HTTPException(status_code=404, detail="Revision schedule not found.")

    rev.is_completed = True
    rev.completed_at = datetime.utcnow()
    db.commit()

    return {
        "status": "success",
        "message": f"Revision marked completed.",
        "revision_id": rev.id,
    }
