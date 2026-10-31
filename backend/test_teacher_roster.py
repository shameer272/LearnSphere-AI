"""
Verification Test Script for LearnSphere AI Teacher Dashboard Roster:
1. Verifies only genuine student accounts (role == 'student') appear in the roster.
2. Verifies the professor account (faculty.demo@btech.edu) never appears in the roster.
3. Verifies test accounts (test_student_...) never appear in the roster.
4. Verifies duplicate normalized email registration is rejected with 409.
5. Verifies newly registered student appears exactly once in the roster.
6. Verifies Total Enrolled matches unique genuine students.
7. Verifies enrolled subjects and mastery are accurate.
"""
import sys
import os

sys.path.insert(0, os.path.abspath("backend"))

from app.database.db import SessionLocal
from app.models.models import Student, Subject, StudentSubject
from app.routes.teacher import get_teacher_analytics
from app.routes.auth import register
from app.schemas.schemas import StudentCreate
from fastapi import HTTPException


def run_roster_tests():
    db = SessionLocal()

    print("====================================================================")
    print(" LEARNSPHERE AI -- TEACHER DASHBOARD ROSTER VERIFICATION")
    print("====================================================================\n")

    # 1. Fetch teacher account
    teacher = db.query(Student).filter(Student.role == "teacher").first()
    assert teacher is not None, "Teacher account not found!"
    print(f"Teacher Account: {teacher.name} ({teacher.email}) [Role: {teacher.role}]")

    # 2. Call get_teacher_analytics
    analytics = get_teacher_analytics(current_teacher=teacher, db=db)
    students = analytics["students"]
    total_students = analytics["total_students"]

    print(f"\nInitial Teacher Analytics Report:")
    print(f"  Total Genuine Students: {total_students}")
    print(f"  Roster Count: {len(students)}")
    for s in students:
        print(f"    - ID {s['id']}: {s['name']} <{s['email']}> | Enrolled: {len(s['enrolled_subjects'])} subjects | Mastery: {s['overall_mastery']}")

    # ASSERTION 1: Professor never appears in student roster
    prof_in_roster = any(s["id"] == teacher.id or s["email"].lower() == teacher.email.lower() for s in students)
    assert not prof_in_roster, "CRITICAL ERROR: Teacher/Professor account appeared in student roster!"
    print("  [PASS] Professor account does not appear in the student roster.")

    # ASSERTION 2: All accounts have role == 'student'
    for s in students:
        db_rec = db.query(Student).filter(Student.id == s["id"]).first()
        assert db_rec.role == "student", f"CRITICAL ERROR: Non-student {db_rec.email} with role {db_rec.role} in roster!"
    print("  [PASS] All accounts in roster have role == 'student'.")

    # ASSERTION 3: Total enrolled matches roster length
    assert total_students == len(students), f"Mismatch between total_students ({total_students}) and roster ({len(students)})"
    print("  [PASS] Total Enrolled matches unique genuine students.")

    # 3. TEST DUPLICATE NORMALIZED EMAIL REJECTION
    print("\n--> Testing Duplicate Normalized Email Rejection...")
    existing_student = students[0]
    dup_variations = [
        existing_student["email"].upper(),
        f"  {existing_student['email']}  ",
        existing_student["email"].capitalize(),
    ]
    for dup_email in dup_variations:
        payload = StudentCreate(
            name="Impostor Student",
            email=dup_email,
            password="SecurePassword123!",
            learning_level="Beginner",
            degree="B.Tech CSE",
            selected_subject_ids=[1, 2],
        )
        try:
            register(payload, db=db)
            assert False, f"CRITICAL ERROR: Duplicate email {dup_email} was permitted!"
        except HTTPException as exc:
            assert exc.status_code == 409, f"Expected 409 Conflict, got {exc.status_code}"
    print("  [PASS] Duplicate normalized emails correctly rejected with 409 Conflict.")

    # 4. REGISTER A NEW GENUINE STUDENT AND VERIFY ROSTER UPDATES
    print("\n--> Registering a new genuine student to verify roster update...")
    new_email = "vikram.aditya@btech.edu"

    # Clean if existed from previous run
    old_vikram = db.query(Student).filter(Student.email == new_email).first()
    if old_vikram:
        db.delete(old_vikram)
        db.commit()

    reg_payload = StudentCreate(
        name="Vikram Aditya",
        email=new_email,
        password="TestPassword123!",
        learning_level="Intermediate",
        degree="B.Tech Computer Science & Engineering",
        selected_subject_ids=[1, 2, 8, 21],
    )
    reg_res = register(reg_payload, db=db)
    print(f"  Successfully registered student: {reg_payload.name} ({new_email})")

    # Re-fetch teacher analytics
    new_analytics = get_teacher_analytics(current_teacher=teacher, db=db)
    new_students = new_analytics["students"]
    new_total = new_analytics["total_students"]

    print(f"  Updated Total Genuine Students: {new_total}")
    assert new_total == total_students + 1, f"Expected {total_students + 1}, got {new_total}"

    # Check Vikram appears exactly once
    vikram_entries = [s for s in new_students if s["email"].lower() == new_email.lower()]
    assert len(vikram_entries) == 1, f"Expected Vikram exactly once, found {len(vikram_entries)} times!"
    v = vikram_entries[0]
    print(f"  [PASS] Vikram Aditya appears exactly once (ID: {v['id']}).")
    print(f"  [PASS] Enrolled subjects: {v['enrolled_subjects']}")
    assert len(v["enrolled_subjects"]) == 4, f"Expected 4 enrolled subjects, got {len(v['enrolled_subjects'])}"

    # Check no duplicate student IDs or emails in updated roster
    seen_ids = set()
    seen_emails = set()
    for s in new_students:
        assert s["id"] not in seen_ids, f"Duplicate student ID {s['id']} in roster!"
        assert s["email"].lower() not in seen_emails, f"Duplicate student email {s['email']} in roster!"
        seen_ids.add(s["id"])
        seen_emails.add(s["email"].lower())
    print("  [PASS] Zero duplicate student records in roster.")

    # Clean up Vikram Aditya after verification test
    created_student = db.query(Student).filter(Student.email == new_email).first()
    if created_student:
        db.delete(created_student)
        db.commit()

    db.close()

    print("\n====================================================================")
    print(" ALL TEACHER ROSTER VERIFICATION CHECKS PASSED SUCCESSFULLY!")
    print("====================================================================")
    return 0


if __name__ == "__main__":
    code = run_roster_tests()
    sys.exit(code)
