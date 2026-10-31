import sqlite3
import os

db_path = "learnsphere_cse.db"
con = sqlite3.connect(db_path)
cur = con.cursor()

tables = [
    r[0]
    for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ).fetchall()
    if not r[0].startswith("sqlite_")
]

print("=== TABLE ROW COUNTS BEFORE CLEANUP ===")
table_counts = {}
for t in tables:
    count = cur.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
    table_counts[t] = count
    print(f"  - {t}: {count} rows")

print("\n=== FOREIGN KEY INTEGRITY CHECK ===")
fk_violations = cur.execute("PRAGMA foreign_key_check").fetchall()
print(f"Foreign key violations: {len(fk_violations)}")
for fkv in fk_violations:
    print(f"  Violation: {fkv}")

print("\n=== STUDENTS: DUPLICATE EMAIL CHECK ===")
dup_emails = cur.execute("""
    SELECT LOWER(TRIM(email)) as norm_email, COUNT(*), GROUP_CONCAT(id), GROUP_CONCAT(name)
    FROM students
    GROUP BY LOWER(TRIM(email))
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate normalized emails found: {len(dup_emails)}")
for row in dup_emails:
    print(f"  {row}")

print("\n=== STUDENTS: SAME NAME MULTIPLE EMAILS (AMBIGUITY CHECK) ===")
same_names = cur.execute("""
    SELECT name, COUNT(*), GROUP_CONCAT(id), GROUP_CONCAT(email)
    FROM students
    GROUP BY name
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Same names across different IDs: {len(same_names)}")
for row in same_names:
    print(f"  {row}")

print("\n=== SUBJECTS DUPLICATE CHECK ===")
dup_subjects = cur.execute("""
    SELECT code, COUNT(*), GROUP_CONCAT(name)
    FROM subjects
    GROUP BY code
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate subject codes: {len(dup_subjects)}")

dup_subject_names = cur.execute("""
    SELECT LOWER(TRIM(name)), COUNT(*), GROUP_CONCAT(code)
    FROM subjects
    GROUP BY LOWER(TRIM(name))
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate subject names: {len(dup_subject_names)}")

print("\n=== TOPICS DUPLICATE CHECK ===")
dup_topics = cur.execute("""
    SELECT subject_id, LOWER(TRIM(name)), COUNT(*), GROUP_CONCAT(id)
    FROM topics
    GROUP BY subject_id, LOWER(TRIM(name))
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate topics per subject: {len(dup_topics)}")
for row in dup_topics:
    print(f"  {row}")

print("\n=== CONCEPTS DUPLICATE CHECK ===")
dup_concepts = cur.execute("""
    SELECT subject_id, LOWER(TRIM(name)), COUNT(*), GROUP_CONCAT(id)
    FROM concepts
    GROUP BY subject_id, LOWER(TRIM(name))
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate concepts per subject: {len(dup_concepts)}")
for row in dup_concepts:
    print(f"  {row}")

print("\n=== QUESTIONS DUPLICATE CHECK ===")
dup_questions = cur.execute("""
    SELECT concept_id, difficulty, LOWER(TRIM(question_text)), COUNT(*), GROUP_CONCAT(id)
    FROM questions
    GROUP BY concept_id, difficulty, LOWER(TRIM(question_text))
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate questions (same concept, difficulty, text): {len(dup_questions)}")
for row in dup_questions:
    print(f"  {row}")

print("\n=== STUDENT SUBJECT ENROLLMENTS DUPLICATE CHECK ===")
dup_enrollments = cur.execute("""
    SELECT student_id, subject_id, COUNT(*), GROUP_CONCAT(id)
    FROM student_subjects
    GROUP BY student_id, subject_id
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate enrollments: {len(dup_enrollments)}")
for row in dup_enrollments:
    print(f"  {row}")

print("\n=== CONCEPT MASTERY DUPLICATE CHECK ===")
dup_mastery = cur.execute("""
    SELECT student_id, concept_id, COUNT(*), GROUP_CONCAT(id)
    FROM concept_mastery
    GROUP BY student_id, concept_id
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate concept mastery records: {len(dup_mastery)}")
for row in dup_mastery:
    print(f"  {row}")

print("\n=== REVISION SCHEDULES DUPLICATE CHECK ===")
dup_revisions = cur.execute("""
    SELECT student_id, concept_id, date(scheduled_date), is_completed, COUNT(*), GROUP_CONCAT(id)
    FROM revision_schedules
    GROUP BY student_id, concept_id, date(scheduled_date), is_completed
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate revision schedules: {len(dup_revisions)}")
for row in dup_revisions:
    print(f"  {row}")

print("\n=== ASSESSMENTS / ANSWER HISTORY / MISCONCEPTIONS DUPLICATE CHECK ===")
dup_answers = cur.execute("""
    SELECT student_id, question_id, answered_at, COUNT(*), GROUP_CONCAT(id)
    FROM answer_history
    GROUP BY student_id, question_id, answered_at
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate answer histories (same student, question, timestamp): {len(dup_answers)}")

dup_misconceptions = cur.execute("""
    SELECT student_id, concept_id, answer_history_id, COUNT(*), GROUP_CONCAT(id)
    FROM misconceptions
    GROUP BY student_id, concept_id, answer_history_id
    HAVING COUNT(*) > 1
""").fetchall()
print(f"Duplicate misconceptions: {len(dup_misconceptions)}")

con.close()

if os.path.exists("learnsphere.db.backup"):
    print("\n=== AUDITING BACKUP DATABASE (learnsphere.db.backup) ===")
    con_bk = sqlite3.connect("learnsphere.db.backup")
    cur_bk = con_bk.cursor()
    bk_tables = [r[0] for r in cur_bk.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall() if not r[0].startswith("sqlite_")]
    for t in bk_tables:
        c = cur_bk.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
        print(f"  Backup table {t}: {c} rows")
    bk_dup_emails = cur_bk.execute("SELECT LOWER(TRIM(email)), count(*) FROM students GROUP BY LOWER(TRIM(email)) HAVING count(*) > 1").fetchall()
    print("Duplicate emails in backup:", bk_dup_emails)
    con_bk.close()
