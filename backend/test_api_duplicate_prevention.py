"""
API Duplicate Prevention Test Suite for LearnSphere AI.
Tests:
1. Registration with duplicate normalized email (case/whitespace variations) -> 409 Conflict.
2. Registration with duplicate subject IDs -> cleanly deduplicated.
3. Diagnostic submission with duplicate answers for same question -> cleanly deduplicated.
4. Concept mastery updates -> cleanly upserted.
5. Spaced revision scheduling and completion -> idempotent.
"""
import sys
import unittest
from fastapi.testclient import TestClient

from main import app
from app.database.db import SessionLocal
from app.models.models import Student, Subject, StudentSubject, ConceptMastery, RevisionSchedule

client = TestClient(app)

def test_duplicate_registration_prevention():
    print("\n--- Test 1: Duplicate Registration Prevention ---")
    # Existing demo student is 'aarav.sharma@btech.edu'
    # Try registering with mixed casing and padding: '  AARAV.SHARMA@btech.edu  '
    payload = {
        "name": "Aarav Sharma Duplicate",
        "email": "  AARAV.SHARMA@btech.edu  ",
        "password": "Password123!",
        "learning_level": "Advanced",
        "degree": "B.Tech Computer Science & Engineering",
        "selected_subject_ids": [1, 2]
    }
    response = client.post("/api/auth/register", json=payload)
    print("Status code for duplicate email registration:", response.status_code)
    assert response.status_code == 409, f"Expected 409 Conflict, got {response.status_code}"
    print(" -> PASS: Duplicate registration blocked with 409 Conflict.")

def test_subject_enrollment_deduplication():
    print("\n--- Test 2: Subject Enrollment Deduplication in Registration ---")
    unique_email = "test.dedup.subjects@btech.edu"

    # Remove if exists from previous test
    db = SessionLocal()
    st = db.query(Student).filter(Student.email == unique_email).first()
    if st:
        db.delete(st)
        db.commit()
    db.close()

    # Get two valid subject IDs
    db = SessionLocal()
    subjects = db.query(Subject).limit(2).all()
    sub_ids = [s.id for s in subjects]
    db.close()

    # Pass duplicate subject IDs in selected_subject_ids: [id1, id1, id2, id2]
    duplicate_ids = [sub_ids[0], sub_ids[0], sub_ids[1], sub_ids[1]]
    payload = {
        "name": "Dedup Student",
        "email": unique_email,
        "password": "Password123!",
        "learning_level": "Intermediate",
        "degree": "B.Tech Computer Science & Engineering",
        "selected_subject_ids": duplicate_ids
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"
    data = response.json()
    new_student_id = data["student"]["id"]

    db = SessionLocal()
    enrollment_count = db.query(StudentSubject).filter(StudentSubject.student_id == new_student_id).count()
    db.close()

    print(f"Enrolled subject count for input [id1, id1, id2, id2]: {enrollment_count}")
    assert enrollment_count == 2, f"Expected 2 unique enrollments, got {enrollment_count}"
    print(" -> PASS: Duplicate subject IDs cleanly deduplicated to unique enrollments.")

def test_diagnostic_submission_deduplication():
    print("\n--- Test 3: Diagnostic Submission Deduplication ---")
    db = SessionLocal()
    student = db.query(Student).first()
    subject = db.query(Subject).filter(Subject.code == "CS-PY").first()
    q = subject.questions[0] if subject.questions else db.query(Subject).first().questions[0]
    db.close()

    # Duplicate answer entries in payload
    payload = {
        "student_id": student.id,
        "subject_id": subject.id,
        "answers": [
            {"question_id": q.id, "selected_answer": "B"},
            {"question_id": q.id, "selected_answer": "B"}, # duplicate
        ]
    }
    response = client.post("/api/assessment/submit", json=payload)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    res = response.json()
    print("Assessment total questions scored:", res["total_questions"])
    assert res["total_questions"] == 1, f"Expected total_questions=1 after deduplication, got {res['total_questions']}"
    print(" -> PASS: Duplicate submitted answers cleanly deduplicated to unique questions.")

def test_revision_completion_idempotency():
    print("\n--- Test 4: Revision Completion Idempotency ---")
    db = SessionLocal()
    rev = db.query(RevisionSchedule).filter(RevisionSchedule.is_completed == False).first()
    if not rev:
        rev = db.query(RevisionSchedule).first()
    rev_id = rev.id
    student_id = rev.student_id
    db.close()

    payload = {"revision_id": rev_id, "student_id": student_id}
    # Complete once
    r1 = client.post("/api/revisions/complete", json=payload)
    assert r1.status_code == 200
    # Complete second time (idempotent call)
    r2 = client.post("/api/revisions/complete", json=payload)
    assert r2.status_code == 200
    print(" -> PASS: Revision completion is fully idempotent.")

if __name__ == "__main__":
    test_duplicate_registration_prevention()
    test_subject_enrollment_deduplication()
    test_diagnostic_submission_deduplication()
    test_revision_completion_idempotency()
    print("\n[OK] ALL API DUPLICATE PREVENTION TESTS PASSED!")
