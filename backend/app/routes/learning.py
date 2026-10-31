"""
Learning router for LearnSphere AI — B.Tech Computer Science & Engineering.
Adaptive next-question delivery and programming misconception feedback.
"""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import (
    AnswerHistory,
    Concept,
    ConceptMastery,
    Misconception,
    Question,
    Student,
    StudentSubject,
    Subject,
)
from app.schemas.schemas import LearningAnswerSubmit, LearningFeedback, QuestionOut
from app.ai.misconception_detector import analyze_answer
from app.ai.question_generator import generate_question
from app.services.mastery_service import (
    update_mastery,
    get_mastery_level,
    calculate_next_difficulty,
)
from app.services.revision_service import schedule_revision

router = APIRouter(prefix="/learning", tags=["learning"])


@router.get("/subjects")
def get_learning_subjects(
    student_id: Optional[int] = Query(default=None, description="Optional Student ID to filter enrolled subjects"),
    db: Session = Depends(get_db),
):
    """
    Get subjects for the learning workspace selector.
    Returns only the student's enrolled subjects if student_id is provided.
    """
    if hasattr(student_id, "default"):
        student_id = student_id.default

    if student_id:
        student = db.query(Student).filter(Student.id == student_id).first()
        if student and student.enrolled_subjects:
            enrolled_list = []
            for es in student.enrolled_subjects:
                subj = es.subject
                if subj:
                    enrolled_list.append({
                        "id": subj.id,
                        "name": subj.name,
                        "code": subj.code,
                        "category": subj.category,
                        "icon": subj.icon,
                    })
            if enrolled_list:
                return enrolled_list

    # Fallback to all available subjects
    all_subjects = db.query(Subject).order_by(Subject.category, Subject.name).all()
    return [
        {
            "id": s.id,
            "name": s.name,
            "code": s.code,
            "category": s.category,
            "icon": s.icon,
        }
        for s in all_subjects
    ]


@router.get("/history")
def get_learning_history(
    student_id: int = Query(..., description="Student ID"),
    subject_id: Optional[int] = Query(default=None, description="Optional Subject ID filter"),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Retrieve recent adaptive question attempt history for a student."""
    if hasattr(student_id, "default"):
        student_id = student_id.default
    if hasattr(subject_id, "default"):
        subject_id = subject_id.default
    if hasattr(limit, "default"):
        limit = limit.default

    query = (
        db.query(AnswerHistory)
        .filter(AnswerHistory.student_id == student_id)
        .order_by(AnswerHistory.answered_at.desc())
    )
    if subject_id:
        query = query.filter(AnswerHistory.subject_id == subject_id)

    records = query.limit(limit).all()
    history_items = []
    for r in records:
        q_text = r.question.question_text if r.question else (r.concept.name if r.concept else "Question")
        history_items.append({
            "id": r.id,
            "question_id": r.question_id,
            "question_text": q_text,
            "selected_answer": r.selected_answer,
            "is_correct": r.is_correct,
            "subject_id": r.subject_id,
            "subject_name": r.subject.name if r.subject else "Computer Science",
            "concept_id": r.concept_id,
            "concept_name": r.concept.name if r.concept else "",
            "time_taken_seconds": r.time_taken_seconds,
            "answered_at": r.answered_at.isoformat() if r.answered_at else None,
        })
    return history_items


@router.get("/next-question", response_model=QuestionOut)
def get_next_question(
    student_id: int = Query(..., description="Student ID"),
    subject_id: Optional[int] = Query(default=None, description="Optional Subject ID"),
    concept_id: Optional[int] = Query(default=None, description="Optional Concept ID"),
    db: Session = Depends(get_db),
):
    """
    Adaptively select the next B.Tech CSE question for a student.
    - If concept_id is provided, practice that concept.
    - Else picks the weakest concept from the selected or enrolled subjects.
    - Strictly prevents repeating previously attempted questions for this student.
    - Calibrates difficulty based on current concept mastery.
    """
    if hasattr(concept_id, "default"):
        concept_id = concept_id.default
    if hasattr(subject_id, "default"):
        subject_id = subject_id.default
    if hasattr(student_id, "default"):
        student_id = student_id.default

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    enrolled_ids = [es.subject_id for es in student.enrolled_subjects]
    if subject_id and enrolled_ids and subject_id not in enrolled_ids:
        # Seamlessly auto-enroll in self-study mode for this subject
        auto_enroll = StudentSubject(student_id=student.id, subject_id=subject_id, enrolled_at=datetime.utcnow())
        db.add(auto_enroll)
        db.commit()
        enrolled_ids.append(subject_id)

    # 1. Determine target subject strictly
    if subject_id:
        target_subject_id = subject_id
    elif enrolled_ids:
        target_subject_id = enrolled_ids[0]
    else:
        first_sub = db.query(Subject).first()
        target_subject_id = first_sub.id if first_sub else 1

    subject_obj = db.query(Subject).filter(Subject.id == target_subject_id).first()
    subject_name = subject_obj.name if subject_obj else "Computer Science"
    subject_code = subject_obj.code if subject_obj else "CS"

    # 2. Get all concepts for this target subject
    subject_concepts = db.query(Concept).filter(Concept.subject_id == target_subject_id).order_by(Concept.order_index, Concept.id).all()
    if not subject_concepts:
        # Create baseline concept if none exists
        default_concept = Concept(subject_id=target_subject_id, name=f"{subject_name} Core Fundamentals", order_index=1)
        db.add(default_concept)
        db.commit()
        db.refresh(default_concept)
        subject_concepts = [default_concept]

    concept_ids = [c.id for c in subject_concepts]

    # Calculate student concept mastery map
    masteries = (
        db.query(ConceptMastery)
        .filter(
            ConceptMastery.student_id == student_id,
            ConceptMastery.concept_id.in_(concept_ids),
        )
        .all()
    )
    mastery_map = {m.concept_id: m for m in masteries}

    # Pick target concept: if concept_id is explicitly specified, use it; else choose weakest concept
    target_concept = None
    if concept_id:
        target_concept = db.query(Concept).filter(Concept.id == concept_id).first()
        if target_concept and target_concept.subject_id != target_subject_id:
            target_concept = None

    if not target_concept:
        def score_of(c: Concept) -> float:
            m = mastery_map.get(c.id)
            return m.mastery_score if m else 0.0
        target_concept = min(subject_concepts, key=score_of)

    # Calibrate difficulty based on mastery
    mastery_rec = mastery_map.get(target_concept.id)
    current_mastery = mastery_rec.mastery_score if mastery_rec else 0.0
    if mastery_rec:
        if mastery_rec.mastery_score < 0.40 or (mastery_rec.attempts >= 2 and mastery_rec.incorrect_count > mastery_rec.correct_count):
            difficulty = "easy"
        elif mastery_rec.mastery_score < 0.75:
            difficulty = "medium"
        else:
            difficulty = "hard"
    else:
        difficulty = "easy"

    # 3. Retrieve ALL previously attempted questions by this student across entire DB history
    answered_records = (
        db.query(AnswerHistory.question_id, Question.question_text)
        .outerjoin(Question, AnswerHistory.question_id == Question.id)
        .filter(AnswerHistory.student_id == student_id)
        .all()
    )
    answered_qids = {r[0] for r in answered_records if r[0] is not None}
    answered_texts = {r[1].strip() for r in answered_records if r[1]}

    # Ensure any answered history without joined question is also covered
    for ah in db.query(AnswerHistory.question_id).filter(AnswerHistory.student_id == student_id).all():
        if ah[0] is not None:
            answered_qids.add(ah[0])

    # 4. Search DB for unattempted questions strictly in this subject
    base_query = db.query(Question).filter(
        (Question.subject_id == target_subject_id) | (Question.concept_id.in_(concept_ids))
    )
    if answered_qids:
        base_query = base_query.filter(Question.id.notin_(answered_qids))

    candidate_questions = base_query.all()
    # Filter out any matching text
    unattempted_pool = [q for q in candidate_questions if q.question_text.strip() not in answered_texts]

    db_question = None

    if unattempted_pool:
        # Prioritize matching concept if available
        concept_pool = [q for q in unattempted_pool if q.concept_id == target_concept.id]
        pool_to_use = concept_pool if concept_pool else unattempted_pool

        # Try matching target difficulty
        diff_pool = [q for q in pool_to_use if q.difficulty == difficulty]
        if diff_pool:
            db_question = diff_pool[0]
        else:
            db_question = pool_to_use[0]

        if db_question and db_question.concept:
            target_concept = db_question.concept

    # 5. If all DB questions in this subject have been attempted, generate a novel question
    if not db_question:
        q_data = generate_question(
            subject_id=target_subject_id,
            concept_id=target_concept.id,
            subject_name=subject_name,
            concept_name=target_concept.name,
            subject_code=subject_code,
            difficulty=difficulty,
            recent_question_texts=list(answered_texts),
        )

        q_text_clean = q_data["question_text"].strip()
        saved = Question(
            subject_id=target_subject_id,
            concept_id=target_concept.id,
            question_type=q_data.get("question_type", "mcq"),
            question_text=q_text_clean,
            code_snippet=q_data.get("code_snippet"),
            options=q_data["options"],
            correct_answer=q_data["correct_answer"],
            explanation=q_data.get("explanation"),
            difficulty=q_data.get("difficulty", difficulty),
            misconception_targets=q_data.get("misconception_targets", []),
            is_ai_generated=q_data.get("is_ai_generated", True),
            created_at=datetime.utcnow(),
        )
        db.add(saved)
        db.commit()
        db.refresh(saved)
        db_question = saved

    return QuestionOut(
        id=db_question.id,
        subject_id=target_subject_id,
        concept_id=target_concept.id if target_concept else db_question.concept_id,
        subject_name=subject_name,
        concept_name=target_concept.name if target_concept else "Core Subject Concept",
        question_type=db_question.question_type or "mcq",
        question_text=db_question.question_text,
        code_snippet=db_question.code_snippet,
        options=db_question.options,
        difficulty=db_question.difficulty,
        is_ai_generated=db_question.is_ai_generated,
        current_mastery=current_mastery,
    )


@router.post("/answer", response_model=LearningFeedback)
def submit_answer(payload: LearningAnswerSubmit, db: Session = Depends(get_db)):
    """
    Submit an answer with written reasoning to an adaptive B.Tech CSE question.
    Analyzes conceptual understanding, updates mastery, and schedules revisions.
    """
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    concept = db.query(Concept).filter(Concept.id == payload.concept_id).first()
    if not concept:
        raise HTTPException(status_code=404, detail="Concept not found.")

    # Retrieve question
    question = None
    if payload.question_id:
        question = db.query(Question).filter(Question.id == payload.question_id).first()

    correct_answer = question.correct_answer if question else "A"
    question_text = question.question_text if question else concept.name
    code_snippet = question.code_snippet if question else None
    difficulty = question.difficulty if question else "medium"
    subject_name = concept.subject.name if concept.subject else "Computer Science"

    is_correct = payload.selected_answer.upper().strip() == correct_answer.upper().strip()

    # AI Misconception Detection
    ai_feedback = analyze_answer(
        question=question_text,
        correct_answer=correct_answer,
        student_answer=payload.selected_answer,
        reasoning=payload.written_reasoning,
        concept_name=concept.name,
        subject_name=subject_name,
        code_snippet=code_snippet,
        difficulty=difficulty,
    )

    # Concept Mastery Update
    mastery = (
        db.query(ConceptMastery)
        .filter(
            ConceptMastery.student_id == payload.student_id,
            ConceptMastery.concept_id == payload.concept_id,
        )
        .first()
    )
    if not mastery:
        mastery = ConceptMastery(
            student_id=payload.student_id,
            subject_id=concept.subject_id,
            concept_id=payload.concept_id,
            mastery_score=0.0,
            attempts=0,
            correct_count=0,
            incorrect_count=0,
            current_difficulty="easy",
        )
        db.add(mastery)
        db.flush()

    previous_mastery = mastery.mastery_score
    mastery.attempts += 1
    if is_correct:
        mastery.correct_count += 1
    else:
        mastery.incorrect_count += 1
    mastery.last_assessed = datetime.utcnow()

    new_score = update_mastery(
        current_mastery=previous_mastery,
        is_correct=is_correct,
        difficulty=difficulty,
        concept_understanding=ai_feedback.get("concept_understanding", "partial"),
        attempts=mastery.attempts,
    )
    mastery.mastery_score = new_score

    # Adjust difficulty tier
    new_diff = calculate_next_difficulty(
        mastery_score=new_score,
        recent_correct=mastery.correct_count,
        recent_incorrect=mastery.incorrect_count,
    )
    mastery.current_difficulty = new_diff

    # Persist answer history
    history = AnswerHistory(
        student_id=payload.student_id,
        subject_id=concept.subject_id,
        question_id=payload.question_id,
        concept_id=payload.concept_id,
        selected_answer=payload.selected_answer,
        is_correct=is_correct,
        written_reasoning=payload.written_reasoning,
        ai_feedback=ai_feedback,
        time_taken_seconds=payload.time_taken_seconds,
        answered_at=datetime.utcnow(),
    )
    db.add(history)
    db.flush()

    # Record misconception if detected
    if not is_correct and ai_feedback.get("detected_misconception"):
        mis = Misconception(
            student_id=payload.student_id,
            subject_id=concept.subject_id,
            concept_id=payload.concept_id,
            answer_history_id=history.id,
            misconception_type=ai_feedback.get("misconception_category"),
            description=ai_feedback.get("detected_misconception"),
            detected_at=datetime.utcnow(),
        )
        db.add(mis)

    # Schedule revision if needed
    revision = schedule_revision(
        student_id=payload.student_id,
        concept_id=payload.concept_id,
        mastery_score=new_score,
        db=db,
        subject_id=concept.subject_id,
    )

    db.commit()

    return LearningFeedback(
        is_correct=is_correct,
        correct_answer=correct_answer,
        detected_misconception=ai_feedback.get("detected_misconception"),
        misconception_category=ai_feedback.get("misconception_category"),
        reasoning_analysis=ai_feedback.get("reasoning_analysis", ""),
        concept_understanding=ai_feedback.get("concept_understanding", "partial"),
        explanation=ai_feedback.get("explanation", ""),
        recommended_learning_action=ai_feedback.get("recommended_learning_action", ""),
        suggested_difficulty=new_diff,
        previous_mastery=previous_mastery,
        new_mastery=new_score,
        mastery_level=get_mastery_level(new_score),
        revision_scheduled={
            "scheduled_date": revision.scheduled_date.isoformat(),
            "priority": revision.priority,
            "reason": revision.reason,
        } if revision else None,
        is_ai_generated=ai_feedback.get("is_ai_generated", False),
    )
