"""
Database Constraints and Index Enforcement Script for LearnSphere AI.
Applies unique indexes, normalizes email addresses, and checks integrity.
"""
import sqlite3
import sys

db_path = "learnsphere_cse.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

try:
    con.execute("BEGIN TRANSACTION")

    print("[1] Normalizing existing student emails (lowercase & stripped)...")
    cur.execute("UPDATE students SET email = LOWER(TRIM(email))")
    print(f" -> Updated {cur.rowcount} student rows.")

    print("\n[2] Applying database UNIQUE indexes...")
    indexes = [
        ("uq_student_email", "CREATE UNIQUE INDEX IF NOT EXISTS uq_student_email ON students(email)"),
        ("uq_subject_code", "CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_code ON subjects(code)"),
        ("uq_subject_name", "CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_name ON subjects(name)"),
        ("uq_subject_topic", "CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_topic ON topics(subject_id, name)"),
        ("uq_subject_concept", "CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_concept ON concepts(subject_id, name)"),
        ("uq_concept_question", "CREATE UNIQUE INDEX IF NOT EXISTS uq_concept_question ON questions(concept_id, question_text)"),
        ("uq_student_subject", "CREATE UNIQUE INDEX IF NOT EXISTS uq_student_subject ON student_subjects(student_id, subject_id)"),
        ("uq_student_concept", "CREATE UNIQUE INDEX IF NOT EXISTS uq_student_concept ON concept_mastery(student_id, concept_id)"),
        ("uq_student_pending_revision", "CREATE UNIQUE INDEX IF NOT EXISTS uq_student_pending_revision ON revision_schedules(student_id, concept_id) WHERE is_completed = 0"),
    ]

    for idx_name, idx_sql in indexes:
        cur.execute(idx_sql)
        print(f" -> Index enforced: {idx_name}")

    con.commit()
    print("\n[OK] All unique constraints successfully committed.")

except Exception as e:
    con.rollback()
    print(f"\n[ERROR] Failed to apply constraints: {e}")
    sys.exit(1)
finally:
    con.close()
