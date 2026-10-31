import sqlite3

con = sqlite3.connect("learnsphere_cse.db")
cols = [r[1] for r in con.execute("PRAGMA table_info(students)").fetchall()]
print("Columns in students table:", cols)
if "role" not in cols:
    con.execute("ALTER TABLE students ADD COLUMN role VARCHAR(20) DEFAULT 'student'")
    con.commit()
    print("Added role column to students table.")
else:
    print("role column already exists.")
con.close()
