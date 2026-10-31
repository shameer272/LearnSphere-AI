"""
LearnSphere AI — Safe Database Backup and Restoration Utility.
Uses SQLite Online Backup API for hot, non-locking, crash-consistent backups.
"""
import os
import sys
import sqlite3
import shutil
from datetime import datetime


def get_db_path():
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(backend_dir, "learnsphere_cse.db")


def create_backup(dest_dir=None):
    """
    Creates an atomic, online backup of the SQLite database without locking active readers/writers.
    Performs an immediate integrity check on the produced snapshot.
    """
    source_db = get_db_path()
    if not os.path.exists(source_db):
        raise FileNotFoundError(f"Database not found at {source_db}")

    if dest_dir is None:
        dest_dir = os.path.join(os.path.dirname(source_db), "backups")
    os.makedirs(dest_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(dest_dir, f"learnsphere_cse_{timestamp}.db")

    source_conn = sqlite3.connect(source_db)
    dest_conn = sqlite3.connect(backup_file)
    try:
        source_conn.backup(dest_conn)
    finally:
        dest_conn.close()
        source_conn.close()

    # Integrity verification
    verify_conn = sqlite3.connect(backup_file)
    try:
        integrity = verify_conn.execute("PRAGMA integrity_check;").fetchone()[0]
    finally:
        verify_conn.close()

    if integrity != "ok":
        if os.path.exists(backup_file):
            os.remove(backup_file)
        raise RuntimeError(f"Backup failed integrity check: {integrity}")

    size_bytes = os.path.getsize(backup_file)
    return backup_file, size_bytes


def restore_backup(backup_file):
    """
    Restores the database from a verified backup file.
    Takes a pre-restore safety snapshot before applying.
    """
    if not os.path.exists(backup_file):
        raise FileNotFoundError(f"Backup file not found at {backup_file}")

    verify_conn = sqlite3.connect(backup_file)
    try:
        integrity = verify_conn.execute("PRAGMA integrity_check;").fetchone()[0]
    finally:
        verify_conn.close()

    if integrity != "ok":
        raise ValueError(f"Cannot restore from corrupt backup: {integrity}")

    dest_db = get_db_path()
    if os.path.exists(dest_db):
        safety_path = dest_db + ".pre_restore_safety"
        shutil.copy2(dest_db, safety_path)

    source_conn = sqlite3.connect(backup_file)
    dest_conn = sqlite3.connect(dest_db)
    try:
        source_conn.backup(dest_conn)
    finally:
        dest_conn.close()
        source_conn.close()

    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--restore":
        if len(sys.argv) < 3:
            print("Usage: python backup.py --restore <path_to_backup.db>")
            sys.exit(1)
        restore_backup(sys.argv[2])
        print(f"[OK] Database successfully restored from {sys.argv[2]}")
    else:
        path, size = create_backup()
        print(f"[OK] Created verified backup: {path} ({size:,} bytes)")
