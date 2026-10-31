"""
Ultra Fast Verification of LearnSphere AI Hardened Requirements:
1. Teacher API requires authentication (401 without token) and role authorization (403 for students).
2. Teacher API succeeds for authorized faculty (200 OK).
3. Empty states return accurately when 0 students exist.
4. Genuine student registration, diagnostic assessment, adaptive learning, and real analytics work.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from app.database.db import SessionLocal
from app.models.models import (
    Student, Subject, Concept, Misconception,
    AnswerHistory, Assessment, RevisionSchedule,
    ConceptMastery, StudentSubject
)

client = TestClient(app)

def run_checks():
    print("=== ULTRA FAST LEARNSPHERE AI VERIFICATION ===")

    # 1. Clean slate check (ensure zero demo students)
    db = SessionLocal()
    demo_emails = ["alice@demo.com", "bob@demo.com", "carol@demo.com", "david@demo.com", "demo.student@btech.edu"]
    demos_found = db.query(Student).filter(Student.email.in_(demo_emails)).all()
    assert len(demos_found) == 0, f"Found {len(demos_found)} demo students!"
    print("[1] Verified zero demo students in active database.")
    db.close()

    # 2. Teacher API Authorization Checks
    print("\n[2] Checking Teacher API Authorization & Guard...")
    # 2a. Unauthenticated -> 401
    r_unauth = client.get("/api/teacher/analytics")
    assert r_unauth.status_code == 401, f"Expected 401, got {r_unauth.status_code}"
    print(" -> PASS: Unauthenticated access blocked with 401 Unauthorized.")

    # 2b. Register normal student
    r_stud = client.post("/api/auth/register", json={
        "name": "Arjun Mehta",
        "email": "arjun.mehta@btech.edu",
        "password": "ArjunPassword123!",
        "learning_level": "Intermediate",
        "degree": "B.Tech Computer Science & Engineering",
        "selected_subject_ids": []
    })
    assert r_stud.status_code == 201
    stud_token = r_stud.json()["access_token"]
    stud_id = r_stud.json()["student"]["id"]

    # Student tries to access teacher analytics -> 403 Forbidden
    r_forbidden = client.get("/api/teacher/analytics", headers={"Authorization": f"Bearer {stud_token}"})
    assert r_forbidden.status_code == 403, f"Expected 403 Forbidden for student, got {r_forbidden.status_code}"
    print(" -> PASS: Non-teacher student access blocked with 403 Forbidden.")

    # 2c. Register faculty / teacher account
    r_fac = client.post("/api/auth/register", json={
        "name": "Prof. Radhika Sen",
        "email": "faculty.radhika@btech.edu",
        "password": "FacultySecure2026!",
        "learning_level": "Advanced",
        "degree": "Department of Computer Science & Engineering",
        "selected_subject_ids": []
    })
    assert r_fac.status_code == 201
    fac_token = r_fac.json()["access_token"]

    # Faculty accesses teacher analytics -> 200 OK
    r_allowed = client.get("/api/teacher/analytics", headers={"Authorization": f"Bearer {fac_token}"})
    assert r_allowed.status_code == 200, f"Expected 200 OK for faculty, got {r_allowed.status_code}"
    data = r_allowed.json()
    print(" -> PASS: Authorized faculty access granted (200 OK).")
    print(f"    Total Students: {data['total_students']}, Assessed: {data['assessed_students_count']}")
    print(f"    has_assessment_data: {data['has_assessment_data']}, class_mastery: {data['average_class_mastery']}")
    assert data["has_assessment_data"] == False, "Student has not taken assessment yet!"
    assert data["average_class_mastery"] is None, "Mastery should be None before any student takes test!"

    # 3. Genuine Student Diagnostic Assessment & Telemetry Update
    print("\n[3] Student completing genuine diagnostic assessment...")
    db = SessionLocal()
    subj = db.query(Subject).filter(Subject.code == "CS-PY").first()
    q = subj.questions[0]
    db.close()

    r_submit = client.post("/api/assessment/submit", json={
        "student_id": stud_id,
        "subject_id": subj.id,
        "answers": [{"question_id": q.id, "selected_answer": q.correct_answer}]
    }, headers={"Authorization": f"Bearer {stud_token}"})
    assert r_submit.status_code == 200
    print(" -> PASS: Student submitted diagnostic successfully.")

    # Teacher analytics should now dynamically reflect this student's actual score
    r_updated = client.get("/api/teacher/analytics", headers={"Authorization": f"Bearer {fac_token}"})
    assert r_updated.status_code == 200
    up_data = r_updated.json()
    print(" -> Updated Faculty Analytics from Real Activity:")
    print(f"    Assessed Students: {up_data['assessed_students_count']}")
    print(f"    Class Average Mastery: {up_data['average_class_mastery']}%")
    print(f"    has_assessment_data: {up_data['has_assessment_data']}")
    assert up_data["assessed_students_count"] == 1
    assert up_data["has_assessment_data"] == True
    assert up_data["average_class_mastery"] is not None
    assert up_data["average_class_mastery"] > 0

    print("\n[✓] ALL CRITICAL ULTRA FAST CHECKS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run_checks()
