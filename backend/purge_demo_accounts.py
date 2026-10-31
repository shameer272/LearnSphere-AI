"""
Purge all pre-seeded demonstration students and mock data from learnsphere_cse.db.
Ensures zero dummy or fake student data exists in the active database.
Preserves the 31 B.Tech CSE subjects, topics, concepts, and questions.
"""
import sys
import os
import sqlite3

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.db import SessionLocal
from app.models.models import (
    Student, Misconception, AnswerHistory, Assessment,
    RevisionSchedule, ConceptMastery, StudentSubject
)

def purge_demo_students():
    db = SessionLocal()
    try:
        demo_emails = [
            "alice@demo.com",
            "bob@demo.com",
            "carol@demo.com",
            "david@demo.com",
            "aarav.sharma@btech.edu",
            "priya.patel@btech.edu",
            "rohan.verma@btech.edu",
            "demo.student@btech.edu",
        ]

        # Also catch any integration test accounts
        all_students = db.query(Student).all()
        to_delete = []
        for s in all_students:
            email_lower = s.email.strip().lower()
            if email_lower in demo_emails or "demo" in email_lower or "test" in email_lower:
                to_delete.append(s.id)
                print(f"Purging demo/test student: #{s.id} {s.name} ({s.email})")

        if to_delete:
            db.query(Misconception).filter(Misconception.student_id.in_(to_delete)).delete(synchronize_session=False)
            db.query(AnswerHistory).filter(AnswerHistory.student_id.in_(to_delete)).delete(synchronize_session=False)
            db.query(Assessment).filter(Assessment.student_id.in_(to_delete)).delete(synchronize_session=False)
            db.query(RevisionSchedule).filter(RevisionSchedule.student_id.in_(to_delete)).delete(synchronize_session=False)
            db.query(ConceptMastery).filter(ConceptMastery.student_id.in_(to_delete)).delete(synchronize_session=False)
            db.query(StudentSubject).filter(StudentSubject.student_id.in_(to_delete)).delete(synchronize_session=False)
            db.query(Student).filter(Student.id.in_(to_delete)).delete(synchronize_session=False)
            db.commit()
            print(f" -> Successfully purged {len(to_delete)} demo/test student profiles and their data.")

        remaining = db.query(Student).count()
        print(f"Active genuine registered students remaining: {remaining}")

    except Exception as e:
        db.rollback()
        print(f"Error purging: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    purge_demo_students()
