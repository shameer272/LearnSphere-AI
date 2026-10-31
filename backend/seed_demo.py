"""
seed_demo.py — Script to synchronize curriculum and questions.
Does NOT create dummy or fake students.
"""
import os
import sys

from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from app.database.init_db import init_database

if __name__ == "__main__":
    print("Synchronizing B.Tech CSE curriculum schema...")
    init_database()
    print("Done. Pure curriculum initialized without demo students.")
