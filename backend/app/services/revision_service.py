"""
Spaced-repetition revision scheduling service for LearnSphere AI.
Implements Ebbinghaus-derived retention intervals for B.Tech CSE concepts.
"""
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from app.models.models import RevisionSchedule, ConceptMastery, Concept
from app.services.mastery_service import get_mastery_level


def schedule_revision(
    student_id: int,
    concept_id: int,
    mastery_score: float,
    db: Session,
    subject_id: Optional[int] = None,
) -> RevisionSchedule:
    """
    Schedule a revision based on current mastery level.
      weak       (<40):  1 day,  priority=high
      developing (40-70): 3 days, priority=medium
      mastered   (>70):  7 days, priority=low
    """
    level = get_mastery_level(mastery_score)

    if level == "weak":
        days_ahead = 1
        priority = "high"
        reason = f"Concept mastery is low ({mastery_score:.1f}%). High forgetting risk — immediate coding practice needed."
    elif level == "developing":
        days_ahead = 3
        priority = "medium"
        reason = f"Concept is developing ({mastery_score:.1f}%). Reinforce with algorithmic edge cases."
    else:
        days_ahead = 7
        priority = "low"
        reason = f"Concept mastered ({mastery_score:.1f}%). Scheduled for long-term retention check."

    scheduled_date = datetime.utcnow() + timedelta(days=days_ahead)

    if not subject_id:
        concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if concept:
            subject_id = concept.subject_id

    # Check for existing pending revision
    existing = (
        db.query(RevisionSchedule)
        .filter(
            RevisionSchedule.student_id == student_id,
            RevisionSchedule.concept_id == concept_id,
            RevisionSchedule.is_completed == False,
        )
        .first()
    )

    if existing:
        existing.scheduled_date = scheduled_date
        existing.priority = priority
        existing.reason = reason
        if subject_id:
            existing.subject_id = subject_id
        db.commit()
        db.refresh(existing)
        return existing

    revision = RevisionSchedule(
        student_id=student_id,
        subject_id=subject_id,
        concept_id=concept_id,
        scheduled_date=scheduled_date,
        priority=priority,
        reason=reason,
    )
    db.add(revision)
    db.commit()
    db.refresh(revision)
    return revision


def get_upcoming_revisions(
    student_id: int,
    db: Session,
    subject_id: Optional[int] = None,
) -> list[RevisionSchedule]:
    """Return revisions due within the next 14 days that are not completed."""
    now = datetime.utcnow()
    cutoff = now + timedelta(days=14)
    query = (
        db.query(RevisionSchedule)
        .filter(
            RevisionSchedule.student_id == student_id,
            RevisionSchedule.is_completed == False,
            RevisionSchedule.scheduled_date <= cutoff,
        )
    )
    if subject_id:
        query = query.filter(RevisionSchedule.subject_id == subject_id)

    return query.order_by(RevisionSchedule.scheduled_date.asc()).all()


def calculate_forgetting_risk(
    last_assessed: Optional[datetime],
    mastery_score: float,
) -> str:
    """
    Estimate forgetting risk based on time-since-last-assessment and mastery.
    """
    if last_assessed is None:
        return "high"

    days_since = (datetime.utcnow() - last_assessed).days

    if days_since >= 7 and mastery_score < 70:
        return "high"
    elif days_since >= 4 and mastery_score < 50:
        return "high"
    elif days_since >= 5 and mastery_score <= 70:
        return "medium"
    elif days_since >= 10:
        return "medium"
    else:
        return "low"
