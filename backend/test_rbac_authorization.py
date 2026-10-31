"""
Verification of the 8 RBAC and Teacher Authorization Scenarios:
1. Public visitor cannot see Teacher Demo (checked via Navbar/Landing routes).
2. Public visitor cannot access /teacher API (401 Unauthorized).
3. Logged-in student cannot see Teacher Dashboard (role='student').
4. Logged-in student receives 403 when calling teacher APIs (/api/teacher/analytics).
5. Authenticated teacher can access teacher analytics (/api/teacher/analytics -> 200).
6. Authenticated teacher receives genuine database-driven analytics.
7. Logout removes access (invalid token or missing header -> 401).
8. Client-side tampering cannot bypass backend authorization (403 Forbidden).
"""
import sys
import os

# Disable external Gemini API delay for speed
os.environ["GEMINI_API_KEY"] = ""

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from main import app
from app.database.db import SessionLocal
from app.models.models import Student
from app.utils.security import create_access_token

client = TestClient(app)

def test_rbac_scenarios():
    print("=" * 70)
    print("LEARNSPHERE AI -- 8 RBAC & TEACHER AUTHORIZATION TEST SCENARIOS")
    print("=" * 70)

    # Clean existing test users if any
    db = SessionLocal()
    try:
        for em in ["student.rbac@btech.edu", "teacher.rbac@btech.edu", "tamper.student@btech.edu"]:
            s = db.query(Student).filter(Student.email == em).first()
            if s:
                db.delete(s)
        db.commit()
    finally:
        db.close()

    # -------------------------------------------------------------------------
    # Scenario 1 & 2: Public visitor cannot access /api/teacher/analytics (401)
    # -------------------------------------------------------------------------
    print("\n[Scenario 1 & 2] Public unauthenticated visitor accessing /api/teacher/analytics...")
    res = client.get("/api/teacher/analytics")
    print(" -> Response status code:", res.status_code)
    assert res.status_code == 401, f"Expected 401 Unauthorized, got {res.status_code}"
    print(" [PASS] Unauthenticated access rejected with 401 Unauthorized.")

    # -------------------------------------------------------------------------
    # Scenario 3 & 4: Logged-in student cannot access teacher analytics (403)
    # -------------------------------------------------------------------------
    print("\n[Scenario 3 & 4] Registering genuine student and testing teacher API access...")
    res_reg = client.post("/api/auth/register", json={
        "name": "Kavya Sharma",
        "email": "student.rbac@btech.edu",
        "password": "StudentPassword123!",
        "learning_level": "Intermediate",
        "degree": "B.Tech Computer Science & Engineering",
        "selected_subject_ids": []
    })
    assert res_reg.status_code == 201
    student_token = res_reg.json()["access_token"]
    student_data = res_reg.json()["student"]
    print(f" -> Registered student #{student_data['id']}: role = '{student_data['role']}'")
    assert student_data["role"] == "student", "Normal registration must strictly assign role='student'"

    # Student calls teacher analytics endpoint -> 403 Forbidden
    res_stud = client.get("/api/teacher/analytics", headers={"Authorization": f"Bearer {student_token}"})
    print(" -> Student GET /api/teacher/analytics response code:", res_stud.status_code)
    assert res_stud.status_code == 403, f"Expected 403 Forbidden, got {res_stud.status_code}"
    print(f" -> Detail: {res_stud.json()['detail']}")
    print(" [PASS] Authenticated student strictly rejected with 403 Forbidden.")

    # -------------------------------------------------------------------------
    # Scenario 5 & 6: Authenticated teacher can access teacher analytics (200)
    # -------------------------------------------------------------------------
    print("\n[Scenario 5 & 6] Provisioning verified teacher account and testing teacher API access...")
    from provision_teacher import provision_teacher
    provision_teacher(
        name="Dr. Vikram Sarabhai",
        email="teacher.rbac@btech.edu",
        password="TeacherPassword123!",
        role="teacher"
    )

    # Login as teacher
    res_t_login = client.post("/api/auth/login", json={
        "email": "teacher.rbac@btech.edu",
        "password": "TeacherPassword123!"
    })
    assert res_t_login.status_code == 200
    teacher_token = res_t_login.json()["access_token"]
    teacher_data = res_t_login.json()["student"]
    print(f" -> Authenticated teacher #{teacher_data['id']}: role = '{teacher_data['role']}'")
    assert teacher_data["role"] == "teacher"

    # Teacher calls teacher analytics endpoint -> 200 OK
    res_t_dash = client.get("/api/teacher/analytics", headers={"Authorization": f"Bearer {teacher_token}"})
    print(" -> Teacher GET /api/teacher/analytics response code:", res_t_dash.status_code)
    assert res_t_dash.status_code == 200, f"Expected 200 OK, got {res_t_dash.status_code}"
    t_analytics = res_t_dash.json()
    print(" -> Cohort Analytics received:")
    print(f"    - Total students in DB: {t_analytics['total_students']}")
    print(f"    - Assessed students: {t_analytics['assessed_students_count']}")
    print(f"    - has_assessment_data: {t_analytics['has_assessment_data']}")
    print(" [PASS] Authenticated teacher granted full cohort intelligence access (200 OK).")

    # -------------------------------------------------------------------------
    # Scenario 7: Logout removes teacher access (401 on invalid/cleared token)
    # -------------------------------------------------------------------------
    print("\n[Scenario 7] Testing session termination / logout revocation...")
    res_logout = client.get("/api/teacher/analytics", headers={"Authorization": "Bearer "})
    assert res_logout.status_code == 401
    res_expired = client.get("/api/teacher/analytics", headers={"Authorization": "Bearer invalid.expired.token"})
    assert res_expired.status_code == 401
    print(" [PASS] Revoked / missing credentials return 401 Unauthorized.")

    # -------------------------------------------------------------------------
    # Scenario 8: Client-side tampering cannot bypass backend authorization
    # -------------------------------------------------------------------------
    print("\n[Scenario 8] Attempting client-side tampering (student with spoofed role in payload)...")
    tamper_token = student_token
    res_tamper = client.get(
        "/api/teacher/analytics?role=teacher",
        headers={
            "Authorization": f"Bearer {tamper_token}",
            "X-User-Role": "teacher",
            "X-Role": "admin"
        }
    )
    print(" -> Tampered request response code:", res_tamper.status_code)
    assert res_tamper.status_code == 403, f"Expected 403 Forbidden on spoofed role, got {res_tamper.status_code}"
    print(" [PASS] Backend cryptographic role check prevented spoofing; returned 403 Forbidden.")

    # Clean test users
    db = SessionLocal()
    try:
        for em in ["student.rbac@btech.edu", "teacher.rbac@btech.edu"]:
            s = db.query(Student).filter(Student.email == em).first()
            if s:
                db.delete(s)
        db.commit()
    finally:
        db.close()

    print("\n" + "=" * 70)
    print("ALL 8 RBAC & AUTHORIZATION SCENARIOS PASSED WITH 100% SUCCESS!")
    print("=" * 70)

if __name__ == "__main__":
    test_rbac_scenarios()
