"""
Complete end-to-end integration tests for LearnSphere AI — B.Tech CSE.
Starts a live server via uvicorn.Server and tests every single API endpoint.
"""
import time
import threading
import sys
import requests
import uvicorn
from main import app

SERVER_PORT = 8000
BASE_URL = f"http://127.0.0.1:{SERVER_PORT}/api"

def run_tests():
    print("=" * 70)
    print("LEARNSPHERE AI — B.TECH CSE LIVE API INTEGRATION TEST SUITE")
    print("=" * 70)

    config = uvicorn.Config(app, host="127.0.0.1", port=SERVER_PORT, log_level="error")
    server = uvicorn.Server(config)
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()

    # Wait for server ready
    for _ in range(40):
        try:
            r = requests.get(f"{BASE_URL}/health", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.25)
    else:
        print("ERROR: Server failed to start within 10s.")
        sys.exit(1)

    print(f"[OK] Live FastAPI server ready on {BASE_URL}")

    try:
        # 1. Health check
        print("\n[1] Testing GET /api/health...")
        res = requests.get(f"{BASE_URL}/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        print(" -> PASS:", data)

        # 2. Subject categories
        print("\n[2] Testing GET /api/subjects/categories...")
        res = requests.get(f"{BASE_URL}/subjects/categories")
        assert res.status_code == 200
        cats = res.json()
        assert len(cats) >= 6, f"Expected 6 B.Tech CSE categories, got {len(cats)}"
        cat_names = [c["category"] for c in cats]
        print(f" -> PASS: Found {len(cats)} categories: {', '.join(cat_names)}")

        # 3. List subjects
        print("\n[3] Testing GET /api/subjects...")
        res = requests.get(f"{BASE_URL}/subjects")
        assert res.status_code == 200
        subjects = res.json()
        assert len(subjects) >= 25, f"Expected 25+ subjects, got {len(subjects)}"
        print(f" -> PASS: Found {len(subjects)} B.Tech CSE subjects across all 6 categories.")

        # 4. Concepts list
        print("\n[4] Testing GET /api/concepts...")
        res = requests.get(f"{BASE_URL}/concepts")
        assert res.status_code == 200
        concepts = res.json()
        assert len(concepts) >= 30, f"Expected 30+ concepts, got {len(concepts)}"
        print(f" -> PASS: Found {len(concepts)} computer science concepts.")

        # 5. Register new B.Tech student
        print("\n[5] Testing POST /api/auth/register...")
        test_email = f"student.test.{int(time.time())}@btech.edu"
        reg_payload = {
            "name": "Devansh Singhania",
            "email": test_email,
            "password": "SecurePassword123!",
            "learning_level": "Intermediate",
            "degree": "B.Tech Computer Science & Engineering",
            "selected_subject_ids": [subjects[0]["id"], subjects[1]["id"], subjects[2]["id"]],
        }
        res = requests.post(f"{BASE_URL}/auth/register", json=reg_payload)
        assert res.status_code == 201, f"Register failed: {res.text}"
        auth_data = res.json()
        assert "access_token" in auth_data
        assert "student" in auth_data
        token = auth_data["access_token"]
        student_id = auth_data["student"]["id"]
        headers = {"Authorization": f"Bearer {token}"}
        print(f" -> PASS: Registered student #{student_id} with JWT token.")

        # 6. Login existing student
        print("\n[6] Testing POST /api/auth/login...")
        login_payload = {
            "email": test_email,
            "password": "SecurePassword123!",
        }
        res = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        assert res.status_code == 200, f"Login failed: {res.text}"
        login_data = res.json()
        assert "access_token" in login_data
        print(f" -> PASS: Successfully logged in with email and password.")

        # 7. Get authenticated profile
        print("\n[7] Testing GET /api/auth/me (Protected Route)...")
        res = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        assert res.status_code == 200
        profile = res.json()
        assert profile["email"] == test_email
        print(f" -> PASS: Verified student profile for '{profile['name']}' ({profile['degree']}).")

        # 8. Diagnostic assessment questions
        print("\n[8] Testing GET /api/assessment/questions...")
        res = requests.get(f"{BASE_URL}/assessment/questions?student_id={student_id}")
        assert res.status_code == 200
        diag = res.json()
        assert "questions" in diag and len(diag["questions"]) > 0
        questions = diag["questions"]
        print(f" -> PASS: Received {len(questions)} diagnostic questions for subject: {diag.get('subject_name')}")

        # 9. Submit diagnostic assessment
        print("\n[9] Testing POST /api/assessment/submit...")
        answers = [{"question_id": q["id"], "selected_answer": "A"} for q in questions[:5]]
        submit_payload = {
            "student_id": student_id,
            "subject_id": diag.get("subject_id"),
            "answers": answers,
        }
        res = requests.post(f"{BASE_URL}/assessment/submit", json=submit_payload)
        assert res.status_code == 200, f"Assessment submit failed: {res.text}"
        result = res.json()
        assert "score_percentage" in result
        assert "mastery_initialized" in result
        print(f" -> PASS: Diagnostic scored {result['score_percentage']}%. Initialized mastery for {len(result['mastery_initialized'])} concepts.")

        # 10. Adaptive next question
        print("\n[10] Testing GET /api/learning/next-question...")
        res = requests.get(f"{BASE_URL}/learning/next-question?student_id={student_id}")
        assert res.status_code == 200, f"Next question failed: {res.text}"
        next_q = res.json()
        assert "question_text" in next_q
        assert "options" in next_q
        print(f" -> PASS: Adaptive engine delivered question for '{next_q['concept_name']}' ({next_q['difficulty']}).")

        # 11. Submit answer with reasoning (misconception detection)
        print("\n[11] Testing POST /api/learning/answer (Misconception Detection)...")
        answer_payload = {
            "student_id": student_id,
            "question_id": next_q.get("id"),
            "concept_id": next_q["concept_id"],
            "selected_answer": "B",
            "written_reasoning": "I thought default list arguments get re-created freshly every time the function is called.",
            "time_taken_seconds": 25,
        }
        res = requests.post(f"{BASE_URL}/learning/answer", json=answer_payload)
        assert res.status_code == 200, f"Learning answer failed: {res.text}"
        feedback = res.json()
        assert "is_correct" in feedback
        assert "new_mastery" in feedback
        assert "explanation" in feedback
        print(f" -> PASS: Received feedback: is_correct={feedback['is_correct']}, new_mastery={feedback['new_mastery']}%.")
        if feedback.get("detected_misconception"):
            print(f"    - Diagnosed Misconception: {feedback['detected_misconception']}")

        # 12. Student dashboard
        print("\n[12] Testing GET /api/students/{id}/dashboard...")
        res = requests.get(f"{BASE_URL}/students/{student_id}/dashboard", headers=headers)
        assert res.status_code == 200, f"Dashboard failed: {res.text}"
        dashboard = res.json()
        assert "overall_mastery" in dashboard
        assert "subject_masteries" in dashboard
        print(f" -> PASS: Dashboard returned overall_mastery={dashboard['overall_mastery']}%, {len(dashboard['subject_masteries'])} enrolled subjects.")

        # 13. Revisions
        print("\n[13] Testing GET /api/revisions/{id} and complete...")
        res = requests.get(f"{BASE_URL}/revisions/{student_id}")
        assert res.status_code == 200
        revs = res.json()
        print(f" -> PASS: Student has {revs['total_pending']} pending revision sessions.")
        if revs["pending"]:
            first_rev = revs["pending"][0]
            comp_res = requests.post(f"{BASE_URL}/revisions/complete", json={"revision_id": first_rev["id"], "student_id": student_id})
            assert comp_res.status_code == 200
            print(f"    - Completed revision #{first_rev['id']} for '{first_rev['concept_name']}'")

        # 14. Teacher Analytics
        print("\n[14] Testing GET /api/teacher/analytics...")
        res = requests.get(f"{BASE_URL}/teacher/analytics")
        assert res.status_code == 200, f"Teacher analytics failed: {res.text}"
        analytics = res.json()
        assert "total_students" in analytics
        assert "subject_analytics" in analytics
        assert len(analytics["subject_analytics"]) >= 20
        print(f" -> PASS: Cohort analytics active across {analytics['total_students']} students and {len(analytics['subject_analytics'])} B.Tech CSE subjects.")

        print("\n" + "=" * 70)
        print("ALL 14 LIVE B.TECH CSE INTEGRATION TESTS PASSED SUCCESSFULLY!")
        print("=" * 70)

    except Exception as exc:
        print(f"\n[FAIL] Test assertion error: {exc}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
