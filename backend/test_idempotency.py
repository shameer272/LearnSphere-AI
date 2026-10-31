"""
Idempotency Test Script for LearnSphere AI.
Executes init_database() multiple times and asserts table counts remain identical.
"""
import sqlite3
from app.database.init_db import init_database

db_path = "learnsphere_cse.db"

def get_counts():
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall() if not r[0].startswith("sqlite_")]
    counts = {t: cur.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0] for t in tables}
    con.close()
    return counts

counts_before = get_counts()
print("[1] Baseline row counts:")
for t, c in counts_before.items():
    print(f"  {t}: {c}")

print("\n[2] Executing init_database() - Run 1...")
init_database()
counts_run1 = get_counts()

print("\n[3] Executing init_database() - Run 2...")
init_database()
counts_run2 = get_counts()

print("\n=== IDEMPOTENCY VERIFICATION RESULTS ===")
mismatch = False
for t in counts_before:
    c_b = counts_before[t]
    c_1 = counts_run1[t]
    c_2 = counts_run2[t]
    status = "OK" if c_b == c_1 == c_2 else "DIFF"
    if status == "DIFF":
        mismatch = True
    print(f"  Table '{t}': Baseline={c_b}, Run1={c_1}, Run2={c_2} -> [{status}]")

assert not mismatch, "Idempotency failed: row counts changed across repeated runs!"
print("\n[OK] Idempotency verified: all 11 tables maintained 100% stable row counts across repeated executions.")
