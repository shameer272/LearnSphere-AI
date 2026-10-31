"""
LearnSphere AI — Hackathon Demo Preparation Script.
1. Preserves full database backup.
2. Removes automated test artifacts while preserving genuine student records.
3. Sets up a dedicated clean demo account: demo.student@btech.edu / DemoStudent2026!
4. Ensures unique passwords across demo and student accounts.
"""
import shutil
import sqlite3
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.db import SessionLocal
from app.models.models import (
    Student, Subject, Concept, StudentSubject,
    ConceptMastery, RevisionSchedule, AnswerHistory, Assessment, Misconception
)
from app.utils.security import hash_password

DB_PATH = "learnsphere_cse.db"
BACKUP_PATH = "learnsphere_cse.db.demo_backup"

def prepare_demo():
    print(f"[1] Creating backup of active database to {BACKUP_PATH}...")
    shutil.copyfile(DB_PATH, BACKUP_PATH)
    print(" -> Backup created successfully.")

    db = SessionLocal()
    try:
        print("\n[2] Identifying and cleaning automated test accounts...")
        # Patterns for test accounts
        test_patterns = [
            "test_%@learnsphere.io",
            "student.test.%@btech.edu",
            "aditi.rao.%@btech.edu",
            "elena_%@demo.com",
            "test.dedup%@btech.edu",
        ]

        test_student_ids = []
        for pat in test_patterns:
            matches = db.query(Student.id, Student.name, Student.email).filter(Student.email.like(pat)).all()
            for s_id, s_name, s_email in matches:
                test_student_ids.append(s_id)
                print(f"  - Removing automated test student: #{s_id} {s_name} ({s_email})")

        if test_student_ids:
            # Delete associated records cleanly
            db.query(Misconception).filter(Misconception.student_id.in_(test_student_ids)).delete(synchronize_session=False)
            db.query(AnswerHistory).filter(AnswerHistory.student_id.in_(test_student_ids)).delete(synchronize_session=False)
            db.query(Assessment).filter(Assessment.student_id.in_(test_student_ids)).delete(synchronize_session=False)
            db.query(RevisionSchedule).filter(RevisionSchedule.student_id.in_(test_student_ids)).delete(synchronize_session=False)
            db.query(ConceptMastery).filter(ConceptMastery.student_id.in_(test_student_ids)).delete(synchronize_session=False)
            db.query(StudentSubject).filter(StudentSubject.student_id.in_(test_student_ids)).delete(synchronize_session=False)
            db.query(Student).filter(Student.id.in_(test_student_ids)).delete(synchronize_session=False)
            db.commit()
            print(f" -> Removed {len(test_student_ids)} automated test student records.")

        print("\n[3] Setting up dedicated clean demo student account...")
        demo_email = "demo.student@btech.edu"
        demo_student = db.query(Student).filter(Student.email == demo_email).first()

        if not demo_student:
            demo_student = Student(
                name="Alex Chen",
                email=demo_email,
                password_hash=hash_password("DemoStudent2026!"),
                learning_level="Intermediate",
                degree="B.Tech Computer Science & Engineering",
                created_at=datetime.utcnow() - timedelta(days=7),
                last_active=datetime.utcnow(),
                streak_days=5,
            )
            db.add(demo_student)
            db.flush()
        else:
            demo_student.name = "Alex Chen"
            demo_student.password_hash = hash_password("DemoStudent2026!")
            demo_student.learning_level = "Intermediate"
            demo_student.streak_days = 5
            demo_student.last_active = datetime.utcnow()
            db.flush()

        # Enroll in core demo subjects
        demo_codes = ["CS-PY", "CS-REACT", "CS-DSA", "CS-AI"]
        demo_subjects = db.query(Subject).filter(Subject.code.in_(demo_codes)).all()

        for subj in demo_subjects:
            enrollment = db.query(StudentSubject).filter(
                StudentSubject.student_id == demo_student.id,
                StudentSubject.subject_id == subj.id,
            ).first()
            if not enrollment:
                db.add(StudentSubject(
                    student_id=demo_student.id,
                    subject_id=subj.id,
                    target_level="Intermediate",
                    enrolled_at=datetime.utcnow() - timedelta(days=7),
                ))

            # Initialize realistic mastery distribution
            for idx, concept in enumerate(subj.concepts):
                mastery = db.query(ConceptMastery).filter(
                    ConceptMastery.student_id == demo_student.id,
                    ConceptMastery.concept_id == concept.id,
                ).first()

                # Make one concept weak (35%) for dynamic AI targeting, others moderate/high (65-85%)
                score = 35.0 if idx == 0 and subj.code == "CS-PY" else (78.0 if idx % 2 == 0 else 62.0)
                diff = "easy" if score < 50 else "medium"

                if not mastery:
                    mastery = ConceptMastery(
                        student_id=demo_student.id,
                        subject_id=subj.id,
                        concept_id=concept.id,
                        mastery_score=score,
                        attempts=8,
                        correct_count=int(score / 12),
                        incorrect_count=max(1, 8 - int(score / 12)),
                        current_difficulty=diff,
                        last_assessed=datetime.utcnow() - timedelta(days=1),
                    )
                    db.add(mastery)
                else:
                    mastery.mastery_score = score
                    mastery.current_difficulty = diff

                # Add a pending revision for the weak concept
                if score < 50:
                    rev = db.query(RevisionSchedule).filter(
                        RevisionSchedule.student_id == demo_student.id,
                        RevisionSchedule.concept_id == concept.id,
                        RevisionSchedule.is_completed == False,
                    ).first()
                    if not rev:
                        db.add(RevisionSchedule(
                            student_id=demo_student.id,
                            subject_id=subj.id,
                            concept_id=concept.id,
                            scheduled_date=datetime.utcnow() + timedelta(days=1),
                            priority="high",
                            reason=f"Spaced practice: Mutable vs Immutable Objects",
                        ))

        # Assign unique random passwords to legacy demo students (not shared)
        unique_passwords = {
            "aarav.sharma@btech.edu": "AaravDev2026!",
            "priya.patel@btech.edu": "PriyaCode2026!",
            "rohan.verma@btech.edu": "RohanCSE2026!",
            "alice@demo.com": "AliceSecure2026!",
            "bob@demo.com": "BobSecure2026!",
            "carol@demo.com": "CarolSecure2026!",
            "david@demo.com": "DavidSecure2026!",
        }
        for email, pwd in unique_passwords.items():
            st = db.query(Student).filter(Student.email == email).first()
            if st:
                st.password_hash = hash_password(pwd)
                print(f"  - Configured unique password hash for: {email}")

        db.commit()
        print(f"\n[OK] Dedicated demo student ready:")
        print(f"     Name: Alex Chen")
        print(f"     Email: {demo_email}")
        print(f"     Password: DemoStudent2026!")

        remaining_students = db.query(Student).all()
        print(f"\n[OK] Total genuine students in demo database: {len(remaining_students)}")
        for s in remaining_students:
            print(f"  #{s.id}: {s.name} ({s.email}) - {s.degree}")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed demo prep: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    prepare_demo()
