"""
Secure Teacher Account Provisioning CLI for LearnSphere AI.
Usage:
    python provision_teacher.py --name "Dr. Alan Turing" --email "faculty.turing@btech.edu" --password "TuringSecure2026!"
"""
import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from app.database.db import SessionLocal
from app.models.models import Student
from app.utils.security import hash_password

def provision_teacher(name: str, email: str, password: str, role: str = "teacher"):
    email_clean = email.strip().lower()
    db = SessionLocal()
    try:
        existing = db.query(Student).filter(Student.email == email_clean).first()
        if existing:
            existing.name = name
            existing.role = role
            existing.password_hash = hash_password(password)
            existing.degree = "Faculty / Department of Computer Science"
            db.commit()
            print(f"[OK] Promoted existing account #{existing.id} ({email_clean}) to role: '{role}'.")
            return

        teacher = Student(
            name=name.strip(),
            email=email_clean,
            password_hash=hash_password(password),
            learning_level="Advanced",
            degree="Faculty / Department of Computer Science",
            role=role,
            created_at=datetime.utcnow(),
            last_active=datetime.utcnow(),
            streak_days=1,
        )
        db.add(teacher)
        db.commit()
        print(f"[OK] Successfully provisioned new verified teacher account #{teacher.id}: {name} ({email_clean}) [Role: {role}].")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Provisioning failed: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision a verified teacher account.")
    parser.add_argument("--name", default="Dr. Sarah Jenkins", help="Teacher full name")
    parser.add_argument("--email", default="faculty.jenkins@btech.edu", help="Teacher official email")
    parser.add_argument("--password", default="FacultySecure2026!", help="Teacher password")
    args = parser.parse_args()

    provision_teacher(args.name, args.email, args.password)
