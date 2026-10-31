import sqlite3
import os
import sys

# Connect to backup
backup_path = "learnsphere.db.backup"
if not os.path.exists(backup_path):
    print("No backup database found.")
    sys.exit(0)

con_old = sqlite3.connect(backup_path)
cur_old = con_old.cursor()
tables = [r[0] for r in cur_old.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
print("Old tables:", tables)

old_students = []
if "students" in tables:
    old_students = cur_old.execute("SELECT id, name, email, created_at FROM students").fetchall()
    print(f"Found {len(old_students)} students in backup:")
    for s in old_students:
        print(f"  - ID: {s[0]}, Name: {s[1]}, Email: {s[2]}")

con_old.close()

# Connect to new database
con_new = sqlite3.connect("learnsphere_cse.db")
cur_new = con_new.cursor()
new_students = cur_new.execute("SELECT id, name, email FROM students").fetchall()
print(f"\nCurrent students in active database ({len(new_students)}):")
for s in new_students:
    print(f"  - ID: {s[0]}, Name: {s[1]}, Email: {s[2]}")

con_new.close()
