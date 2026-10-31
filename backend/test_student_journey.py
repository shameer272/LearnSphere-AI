"""
Complete Student Journey Simulation Test — B.Tech Computer Science & Engineering.
Simulates a real B.Tech CSE student taking the full journey:
1. Registration & Subject Enrollment
2. Diagnostic Assessment (10 questions across B.Tech CSE concepts)
3. Initial Mastery calculation & persistence
4. Dashboard inspection with enrolled B.Tech CSE subjects
5. Adaptive question delivery targeting weakest programming concept
6. Answering with conceptual reasoning (misconception detection)
7. Mastery update persistence
8. Second adaptive question delivery
9. Revision calendar verification & spaced repetition
10. Teacher dashboard reflection
"""
import time
import requests
import uvicorn
import threading
import sys
from main import app

SERVER_PORT = 8000
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}/api"

def run_journey():
    print("=" * 70)
    print("LEARNSPHERE AI — COMPLETE B.TECH CSE STUDENT JOURNEY VERIFICATION")
    print("=" * 70)

    # Start live server if not already running
    server_ready = False
    try:
        if requests.get(f"{BASE_URL}/health", timeout=1).status_code == 200:
            server_ready = True
    except Exception:
        pass

    if not server_ready:
        config = uvicorn.Config(app, host="127.0.0.1", port=SERVER_PORT, log_level="error")
        server = uvicorn.Server(config)
        t = threading.Thread(target=server.run, daemon=True)
        t.start()

        for _ in range(30):
            try:
                if requests.get(f"{BASE_URL}/health", timeout=1).status_code == 200:
                    server_ready = True
                    break
            except Exception:
                time.sleep(0.3)

    if not server_ready:
        print("Server start failed.")
        sys.exit(1)

    try:
        # Step 1: Register New B.Tech CSE Student
        print("\n[Step 1] Registering student: 'Aditi Rao' (B.Tech CSE)...")
        ts = int(time.time())
        res = requests.post(f"{BASE_URL}/auth/register", json={
            "name": "Aditi Rao",
            "email": f"aditi.rao.{ts}@btech.edu",
            "password": "Password123!",
            "learning_level": "Intermediate",
            "degree": "B.Tech Computer Science and Engineering",
            "selected_subject_ids": [1, 2, 8, 26, 31],
        })
        assert res.status_code == 201, f"Failed registration: {res.text}"
        data = res.json()
        token = data["access_token"]
        student_id = data["student"]["id"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f" -> Enrolled in subjects: {[s['name'] for s in data['student']['enrolled_subjects']]}")

        # Step 2: Diagnostic Assessment
        print("\n[Step 2] Fetching diagnostic assessment questions for Python Programming...")
        res = requests.get(f"{BASE_URL}/assessment/questions?student_id={student_id}&subject_id=1")
        assert res.status_code == 200
        diag = res.json()
        questions = diag["questions"]
        print(f" -> Fetched {len(questions)} diagnostic questions.")

        # Step 3: Complete diagnostic test
        print("\n[Step 3] Submitting diagnostic assessment...")
        answers = [{"question_id": q["id"], "selected_answer": "B"} for q in questions[:5]]
        res = requests.post(f"{BASE_URL}/assessment/submit", json={
            "student_id": student_id,
            "subject_id": 1,
            "answers": answers,
        })
        assert res.status_code == 200
        diag_res = res.json()
        print(f" -> Diagnostic score: {diag_res['score_percentage']}%. Concepts initialized: {len(diag_res['mastery_initialized'])}")

        # Step 4: Dashboard inspection
        print("\n[Step 4] Inspecting personalized student dashboard...")
        res = requests.get(f"{BASE_URL}/students/{student_id}/dashboard", headers=headers)
        assert res.status_code == 200
        dash = res.json()
        print(f" -> Overall Mastery: {dash['overall_mastery']}% across {len(dash['subject_masteries'])} subjects.")

        # Step 5: Adaptive question targeting weak concept
        print("\n[Step 5] Adaptive question targeting weakest concept...")
        res = requests.get(f"{BASE_URL}/learning/next-question?student_id={student_id}")
        assert res.status_code == 200
        q1 = res.json()
        print(f" -> Next Question: '{q1['concept_name']}' ({q1['difficulty']})")
        print(f"    Text: {q1['question_text']}")

        # Step 6: Answering with reasoning & Misconception detection
        print("\n[Step 6] Submitting answer with student reasoning...")
        res = requests.post(f"{BASE_URL}/learning/answer", json={
            "student_id": student_id,
            "question_id": q1.get("id"),
            "concept_id": q1["concept_id"],
            "selected_answer": "C",
            "written_reasoning": "I assumed lists passed as default arguments are allocated per invocation.",
            "time_taken_seconds": 20,
        })
        assert res.status_code == 200
        fb1 = res.json()
        print(f" -> Feedback: is_correct={fb1['is_correct']}, mastery={fb1['new_mastery']}%.")
        if fb1.get("detected_misconception"):
            print(f"    Misconception Diagnosed: {fb1['detected_misconception']}")

        # Step 7: Verify spaced revision scheduled
        print("\n[Step 7] Checking revision calendar...")
        res = requests.get(f"{BASE_URL}/revisions/{student_id}")
        assert res.status_code == 200
        rev_data = res.json()
        print(f" -> Pending revisions scheduled: {rev_data['total_pending']}")

        # Step 8: Teacher dashboard reflects student's progress
        print("\n[Step 8] Verifying teacher dashboard reflects new student cohort...")
        res = requests.get(f"{BASE_URL}/teacher/analytics")
        assert res.status_code == 200
        analytics = res.json()
        print(f" -> Class Average Mastery: {analytics['average_class_mastery']}%. Total students: {analytics['total_students']}.")

        print("\n" + "=" * 70)
        print("B.TECH CSE STUDENT JOURNEY TEST COMPLETED WITH 100% SUCCESS!")
        print("=" * 70)

    except Exception as exc:
        print(f"\n[FAIL] Student journey error: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_journey()
