"""
Concepts router for LearnSphere AI — B.Tech Computer Science & Engineering.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import Concept, Subject
from app.schemas.schemas import ConceptOut

router = APIRouter(prefix="/concepts", tags=["concepts"])


@router.get("", response_model=list[ConceptOut])
def list_concepts(
    subject_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """List B.Tech CSE concepts with descriptions and prerequisites."""
    query = db.query(Concept).join(Subject, Concept.subject_id == Subject.id)
    if subject_id:
        query = query.filter(Concept.subject_id == subject_id)
    concepts = query.order_by(Subject.order_index, Concept.order_index).all()

    return [
        ConceptOut(
            id=c.id,
            subject_id=c.subject_id,
            topic_id=c.topic_id,
            name=c.name,
            description=c.description,
            order_index=c.order_index,
            prerequisites=c.prerequisites or [],
            subject_name=c.subject.name if c.subject else None,
        )
        for c in concepts
    ]
