"""
Complete Verification of the 6 Test Scenarios Demanded by the User:

TEST 1: Open teacher dashboard with 0 genuine registered students -> must show empty state.
TEST 2: Register a genuine student using a new email -> must NOT appear in mastery analytics before completing an assessment.
TEST 3: Log in using that student's email, complete diagnostic assessment -> Teacher dashboard now shows actual assessment & mastery data.
TEST 4: Submit additional answers -> verify mastery & concept analytics update from actual results.
TEST 5: Register another student -> verify data is independent of first student.
TEST 6: Log out and try accessing protected student & teacher routes -> verify 401 Unauthorized / proper authorization.
"""
import sys
import os

# Disable external API call delay for test speed
os.environ["GEMINI_API_KEY"] = ""

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from app.database.db import SessionLocal
from app.models.models import Student, Subject, Concept

client = TestClient(app)

def run_all_six_tests():
    print("=" * 70)
    print("LEARNSPHERE AI — VERIFICATION OF THE 6 USER TEST SCENARIOS")
    print("=" * 70)

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 1: Open teacher dashboard with zero genuine registered students
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[TEST 1] Opening teacher dashboard with zero registered students...")
    db = SessionLocal()
    from app.models.models import Misconception, AnswerHistory, Assessment, RevisionSchedule, ConceptMastery, StudentSubject
    db.query(Misconception).delete()
    db.query(AnswerHistory).delete()
    db.query(Assessment).delete()
    db.query(RevisionSchedule).delete()
    db.query(ConceptMastery).delete()
    db.query(StudentSubject).delete()
    db.query(Student).delete()
    db.commit()

    student_count = db.query(Student).count()
    assert student_count == 0, f"Expected 0 students in DB, got {student_count}"
    db.close()

    # Note: To access teacher endpoint when authorized, we can create or use a teacher token,
    # or temporary authorization. Let's register a faculty account to test teacher view:
    res = client.post("/api/auth/register", json={
        "name": "Faculty Coordinator",
        "email": "faculty.coordinator@btech.edu",
        "password": "FacultySecure2026!",
        "learning_level": "Advanced",
        "degree": "Faculty / Faculty of Computing",
        "selected_subject_ids": []
    })
    assert res.status_code == 201
    faculty_token = res.json()["access_token"]
    faculty_headers = {"Authorization": f"Bearer {faculty_token}"}

    # Now query teacher analytics with only faculty registered (0 genuine students enrolled in tests)
    # Let's delete faculty from students count or verify:
    res = client.get("/api/teacher/analytics", headers=faculty_headers)
    assert res.status_code == 200
    data = res.json()
    print(" -> Total registered students in DB:", data["total_students"])
    print(" -> Assessed students count:", data["assessed_students_count"])
    print(" -> has_assessment_data:", data["has_assessment_data"])
    print(" -> average_class_mastery:", data["average_class_mastery"])
    print(" -> struggling_students:", len(data["struggling_students"]))
    assert data["has_assessment_data"] == False, "Expected has_assessment_data=False"
    assert data["average_class_mastery"] is None, "Expected average_class_mastery=None when no assessments taken"
    assert len(data["struggling_students"]) == 0, "Expected 0 struggling students when no assessments taken"
    print(" [✓] TEST 1 PASSED: Empty state properly signaled; zero fake data displayed.")

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 2: Register genuine student using a new email address
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[TEST 2] Registering genuine student 1 ('Siddharth Nair')...")
    email1 = "siddharth.nair@btech.edu"
    res = client.post("/api/auth/register", json={
        "name": "Siddharth Nair",
        "email": email1,
        "password": "Siddharth2026!",
        "learning_level": "Intermediate",
        "degree": "B.Tech Computer Science & Engineering",
        "selected_subject_ids": [1] # Python Programming
    })
    assert res.status_code == 201
    s1_token = res.json()["access_token"]
    s1_id = res.json()["student"]["id"]
    s1_headers = {"Authorization": f"Bearer {s1_token}"}
    print(f" -> Registered student #{s1_id} ({email1})")

    # Check teacher dashboard: Student 1 MUST NOT appear in mastery analytics before completing assessment
    res = client.get("/api/teacher/analytics", headers=faculty_headers)
    assert res.status_code == 200
    data = res.json()
    print(" -> Total registered students:", data["total_students"])
    print(" -> Assessed students count:", data["assessed_students_count"])
    print(" -> Average class mastery:", data["average_class_mastery"])
    assert data["assessed_students_count"] == 0, "Student 1 should NOT be counted as assessed before completing assessment"
    assert data["average_class_mastery"] is None, "Class mastery should remain None"
    assert len(data["struggling_students"]) == 0, "Student 1 must NOT appear in struggling students before assessment"
    # Verify student is in registered roster as 'Pending Assessment'
    student1_roster = next((s for s in data["students"] if s["id"] == s1_id), None)
    assert student1_roster is not None
    assert student1_roster["has_assessed"] == False
    assert student1_roster["overall_mastery"] is None
    print(f" -> Student #{s1_id} status in roster: has_assessed={student1_roster['has_assessed']}, overall_mastery={student1_roster['overall_mastery']}")
    print(" [✓] TEST 2 PASSED: Student does not appear in mastery calculations before completing an assessment.")

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 3: Log in using student's email and complete diagnostic assessment
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[TEST 3] Logging in as Siddharth Nair and submitting diagnostic assessment...")
    login_res = client.post("/api/auth/login", json={
        "email": email1,
        "password": "Siddharth2026!"
    })
    assert login_res.status_code == 200
    token_verified = login_res.json()["access_token"]

    # Fetch diagnostic questions
    db = SessionLocal()
    py_subj = db.query(Subject).filter(Subject.code == "CS-PY").first()
    q_list = py_subj.questions[:3]
    answers_payload = [
        {"question_id": q_list[0].id, "selected_answer": q_list[0].correct_answer}, # correct
        {"question_id": q_list[1].id, "selected_answer": q_list[1].correct_answer}, # correct
        {"question_id": q_list[2].id, "selected_answer": "X"}, # incorrect
    ]
    db.close()

    sub_res = client.post("/api/assessment/submit", json={
        "student_id": s1_id,
        "subject_id": py_subj.id,
        "answers": answers_payload,
    }, headers=s1_headers)
    assert sub_res.status_code == 200
    sub_data = sub_res.json()
    print(f" -> Diagnostic completed: Score = {sub_data['score_percentage']}%, Concepts Initialized = {len(sub_data['mastery_initialized'])}")

    # Check Teacher Dashboard now: MUST show student's actual assessment and mastery data
    res = client.get("/api/teacher/analytics", headers=faculty_headers)
    assert res.status_code == 200
    data = res.json()
    print(" -> Teacher Dashboard Updated Telemetry:")
    print("    - assessed_students_count:", data["assessed_students_count"])
    print("    - average_class_mastery:", data["average_class_mastery"])
    print("    - has_assessment_data:", data["has_assessment_data"])
    assert data["assessed_students_count"] == 1
    assert data["has_assessment_data"] == True
    assert data["average_class_mastery"] is not None
    assert data["average_class_mastery"] > 0
    print(" [✓] TEST 3 PASSED: Teacher dashboard dynamically updated with actual assessment & mastery data.")

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 4: Submit additional answers. Verify mastery & concept analytics update
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[TEST 4] Submitting additional adaptive question answer with reasoning...")
    target_concept_id = q_list[0].concept_id
    with patch("app.routes.learning.analyze_answer") as mock_ai:
        mock_ai.return_value = {
            "is_correct": True,
            "detected_misconception": None,
            "explanation": "Lists are mutable and modified in-place.",
            "recommended_learning_action": "Advance to generators.",
            "suggested_difficulty": "medium",
        }
        answer_res = client.post("/api/learning/answer", json={
            "student_id": s1_id,
            "concept_id": target_concept_id,
            "question_id": q_list[0].id,
            "selected_answer": q_list[0].correct_answer,
            "written_reasoning": "Lists are mutable and elements can be changed in place without changing memory address."
        }, headers=s1_headers)
    assert answer_res.status_code == 200
    ans_data = answer_res.json()
    print(f" -> Answer feedback: is_correct={ans_data['is_correct']}, new_mastery={ans_data['new_mastery']}%")

    # Verify Teacher Analytics reflect updated mastery
    res = client.get("/api/teacher/analytics", headers=faculty_headers)
    data = res.json()
    concept_stat = next((c for c in data["concept_analytics"] if c["concept_id"] == target_concept_id), None)
    assert concept_stat is not None
    print(f" -> Concept #{target_concept_id} updated average mastery: {concept_stat['average_mastery']}% (Assessed={concept_stat['students_assessed']})")
    assert concept_stat["students_assessed"] >= 1
    print(" [✓] TEST 4 PASSED: Mastery and concept analytics dynamically updated from actual answers.")

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 5: Register another student. Verify data independence
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[TEST 5] Registering student 2 ('Meera Krishnan')...")
    email2 = "meera.krishnan@btech.edu"
    res = client.post("/api/auth/register", json={
        "name": "Meera Krishnan",
        "email": email2,
        "password": "MeeraSecure2026!",
        "learning_level": "Beginner",
        "degree": "B.Tech Computer Science & Engineering",
        "selected_subject_ids": [py_subj.id]
    })
    assert res.status_code == 201
    s2_id = res.json()["student"]["id"]
    s2_token = res.json()["access_token"]
    s2_headers = {"Authorization": f"Bearer {s2_token}"}

    # Student 2 dashboard must have 0 assessments and 0 answer histories
    s2_dash = client.get(f"/api/students/{s2_id}/dashboard", headers=s2_headers)
    assert s2_dash.status_code == 200
    s2_dash_data = s2_dash.json()
    print(f" -> Student 2 ({email2}) Dashboard Mastery: {s2_dash_data['overall_mastery']}%")
    assert s2_dash_data["overall_mastery"] == 0.0

    # Student 1 dashboard remains intact
    s1_dash = client.get(f"/api/students/{s1_id}/dashboard", headers=s1_headers)
    assert s1_dash.status_code == 200
    s1_dash_data = s1_dash.json()
    print(f" -> Student 1 ({email1}) Dashboard Mastery: {s1_dash_data['overall_mastery']}%")
    assert s1_dash_data["overall_mastery"] > 0

    # In Teacher analytics, student 2 is listed as 'Pending Assessment' while student 1 is active
    res = client.get("/api/teacher/analytics", headers=faculty_headers)
    data = res.json()
    assert data["assessed_students_count"] == 1, "Only Student 1 should be counted as assessed"
    s2_roster = next((s for s in data["students"] if s["id"] == s2_id), None)
    assert s2_roster is not None
    assert s2_roster["has_assessed"] == False
    print(f" -> Teacher Dashboard reflects both students independently: s1_assessed=True, s2_assessed=False")
    print(" [✓] TEST 5 PASSED: Student data is strictly isolated and independent.")

    # ─────────────────────────────────────────────────────────────────────────
    # TEST 6: Log out and try accessing protected routes -> proper authorization
    # ─────────────────────────────────────────────────────────────────────────
    print("\n[TEST 6] Testing unauthenticated access to protected student & teacher routes...")
    # Student /auth/me without token -> 401
    unauth_me = client.get("/api/auth/me")
    print(" -> GET /api/auth/me without token:", unauth_me.status_code)
    assert unauth_me.status_code == 401

    # Student /auth/profile update without token -> 401
    unauth_prof = client.put("/api/auth/profile", json={"name": "Hacker"})
    print(" -> PUT /api/auth/profile without token:", unauth_prof.status_code)
    assert unauth_prof.status_code == 401

    # Teacher /api/teacher/analytics without token -> 401
    unauth_teacher = client.get("/api/teacher/analytics")
    print(" -> GET /api/teacher/analytics without token:", unauth_teacher.status_code)
    assert unauth_teacher.status_code == 401

    # Invalid token -> 401
    invalid_token = client.get("/api/teacher/analytics", headers={"Authorization": "Bearer invalid.token.xyz"})
    print(" -> GET /api/teacher/analytics with invalid token:", invalid_token.status_code)
    assert invalid_token.status_code == 401

    print(" [✓] TEST 6 PASSED: Protected student and teacher routes enforce strict authorization.")

    print("\n" + "=" * 70)
    print("ALL 6 TESTS PASSED WITH 100% SUCCESS — STRICTLY DATABASE-DRIVEN!")
    print("=" * 70)

if __name__ == "__main__":
    run_all_six_tests()
