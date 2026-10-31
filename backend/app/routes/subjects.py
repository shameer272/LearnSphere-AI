"""
Subjects router for LearnSphere AI — B.Tech Computer Science & Engineering.
Provides curriculum browsing, category filtering, and subject details.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import Subject, Student, StudentSubject
from app.schemas.schemas import SubjectOut, SubjectDetailOut, ConceptOut, TopicOut
from app.utils.security import get_optional_student

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.get("", response_model=list[SubjectOut])
def list_subjects(
    category: Optional[str] = Query(default=None),
    student: Optional[Student] = Depends(get_optional_student),
    db: Session = Depends(get_db),
):
    """
    List all B.Tech CSE subjects, optionally filtered by category.
    Annotates each subject with student's enrollment status if logged in.
    """
    query = db.query(Subject)
    if category:
        query = query.filter(Subject.category.ilike(f"%{category}%"))
    subjects = query.order_by(Subject.order_index).all()

    enrolled_ids = set()
    if student:
        enrolled_ids = {es.subject_id for es in student.enrolled_subjects}

    results = []
    for s in subjects:
        results.append(
            SubjectOut(
                id=s.id,
                category=s.category,
                name=s.name,
                code=s.code,
                description=s.description,
                icon=s.icon,
                order_index=s.order_index,
                concept_count=len(s.concepts),
                is_enrolled=(s.id in enrolled_ids),
            )
        )
    return results


@router.get("/categories")
def list_categories(db: Session = Depends(get_db)):
    """List distinct B.Tech CSE categories and subject counts."""
    subjects = db.query(Subject).all()
    categories = {}
    for s in subjects:
        if s.category not in categories:
            categories[s.category] = {"category": s.category, "subjects_count": 0, "subjects": []}
        categories[s.category]["subjects_count"] += 1
        categories[s.category]["subjects"].append({
            "id": s.id,
            "name": s.name,
            "code": s.code,
            "icon": s.icon,
            "concept_count": len(s.concepts),
        })
    return list(categories.values())


@router.get("/{subject_id}", response_model=SubjectDetailOut)
def get_subject_detail(
    subject_id: int,
    student: Optional[Student] = Depends(get_optional_student),
    db: Session = Depends(get_db),
):
    """Return subject with its hierarchy of topics and concepts."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found.")

    enrolled_ids = set()
    if student:
        enrolled_ids = {es.subject_id for es in student.enrolled_subjects}

    topics_out = []
    for t in subject.topics:
        concepts_out = [
            ConceptOut(
                id=c.id,
                subject_id=c.subject_id,
                topic_id=c.topic_id,
                name=c.name,
                description=c.description,
                order_index=c.order_index,
                prerequisites=c.prerequisites or [],
                subject_name=subject.name,
            )
            for c in t.concepts
        ]
        topics_out.append(
            TopicOut(
                id=t.id,
                subject_id=t.subject_id,
                name=t.name,
                description=t.description,
                order_index=t.order_index,
                concepts=concepts_out,
            )
        )

    all_concepts_out = [
        ConceptOut(
            id=c.id,
            subject_id=c.subject_id,
            topic_id=c.topic_id,
            name=c.name,
            description=c.description,
            order_index=c.order_index,
            prerequisites=c.prerequisites or [],
            subject_name=subject.name,
        )
        for c in subject.concepts
    ]

    return SubjectDetailOut(
        id=subject.id,
        category=subject.category,
        name=subject.name,
        code=subject.code,
        description=subject.description,
        icon=subject.icon,
        order_index=subject.order_index,
        concept_count=len(subject.concepts),
        is_enrolled=(subject.id in enrolled_ids),
        topics=topics_out,
        concepts=all_concepts_out,
    )
