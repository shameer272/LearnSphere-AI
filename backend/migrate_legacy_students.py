"""
LearnSphere AI — Legacy Student Migration Script.
Safely migrates student user records from legacy backup (learnsphere.db.backup)
into the new B.Tech CSE database (learnsphere_cse.db).

Rules:
1. Preserves existing student accounts (Alice, Bob, Carol, David, etc.) with emails and names.
2. Generates secure PBKDF2-HMAC-SHA256 password hash for authentication ('Password123!').
3. Sets degree to 'B.Tech Computer Science & Engineering'.
4. Enrolls each student into primary B.Tech CSE subjects (Python, Data Structures & Algorithms).
5. Does NOT migrate legacy physics concept mastery or physics questions, ensuring a clean CSE slate.
6. Safe and idempotent: will not duplicate existing students.
"""

import os
import sys
import sqlite3
from datetime import datetime

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.db import SessionLocal
from app.models.models import Student, Subject, StudentSubject
from app.utils.security import hash_password


def run_migration():
    backup_path = os.path.join(os.path.dirname(__file__), "learnsphere.db.backup")
    if not os.path.exists(backup_path):
        print(f"[-] Backup database not found at {backup_path}. Aborting.")
        return

    print(f"[+] Found backup database: {backup_path}")
    con_old = sqlite3.connect(backup_path)
    cur_old = con_old.cursor()

    old_students = cur_old.execute(
        "SELECT id, name, email, created_at FROM students"
    ).fetchall()
    print(f"[+] Found {len(old_students)} legacy student records in backup database.")

    db = SessionLocal()
    try:
        # Get default subjects to enroll in (e.g., Python and DSA)
        default_subjects = (
            db.query(Subject)
            .filter(Subject.code.in_(["CS-PY", "CS-DSA"]))
            .all()
        )
        if not default_subjects:
            default_subjects = db.query(Subject).limit(2).all()

        migrated_count = 0
        skipped_count = 0

        default_hash = hash_password("Password123!")

        for row in old_students:
            old_id, name, email, created_at_str = row
            existing = db.query(Student).filter(Student.email == email).first()
            if existing:
                skipped_count += 1
                continue

            try:
                created_at = (
                    datetime.fromisoformat(created_at_str)
                    if created_at_str
                    else datetime.utcnow()
                )
            except Exception:
                created_at = datetime.utcnow()

            student = Student(
                name=name,
                email=email,
                password_hash=default_hash,
                learning_level="Intermediate",
                degree="B.Tech Computer Science & Engineering",
                created_at=created_at,
                last_active=datetime.utcnow(),
                streak_days=1,
            )
            db.add(student)
            db.flush()

            # Enroll in default subjects
            for sub in default_subjects:
                enrollment = StudentSubject(
                    student_id=student.id,
                    subject_id=sub.id,
                    target_level="Intermediate",
                )
                db.add(enrollment)

            migrated_count += 1
            print(f"  [+] Migrated student: {name} ({email}) -> CSE ID {student.id}")

        db.commit()
        print(f"\n[OK] Migration Complete: {migrated_count} students migrated, {skipped_count} already existed.")

        # Display current total students
        total = db.query(Student).count()
        print(f"[OK] Total students in B.Tech CSE database: {total}")

    except Exception as e:
        db.rollback()
        print(f"[-] Migration error: {e}")
        raise
    finally:
        db.close()
        con_old.close()


if __name__ == "__main__":
    run_migration()
