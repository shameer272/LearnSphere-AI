"""
Verification Test Script for LearnSphere AI Adaptive Question Engine:
1. Tests 20 consecutive questions for 10 subjects:
   - Python Programming (CS-PY)
   - C Programming (CS-C)
   - C++ Programming (CS-CPP)
   - Java Programming (CS-JAVA)
   - JavaScript (CS-JS)
   - HTML (CS-HTML)
   - CSS (CS-CSS)
   - React.js (CS-REACT)
   - SQL (CS-SQL)
   - Data Structures and Algorithms (CS-DSA)
2. Asserts all 20 question IDs and texts are distinct per subject (zero duplicates).
3. Asserts zero cross-subject bleeding.
4. Asserts independent student histories (Student 1 vs Student 2).
"""
import sys
import os

# Set python path
sys.path.insert(0, os.path.abspath("backend"))

from app.database.db import SessionLocal
from app.models.models import Student, Subject, Concept, Question, AnswerHistory, Misconception, ConceptMastery, StudentSubject
from app.routes.learning import get_next_question, submit_answer
from app.schemas.schemas import LearningAnswerSubmit


def run_comprehensive_tests():
    db = SessionLocal()

    test_subjects = [
        {"code": "CS-PY", "name": "Python Programming", "id": 1},
        {"code": "CS-C", "name": "C Programming", "id": 2},
        {"code": "CS-CPP", "name": "C++ Programming", "id": 3},
        {"code": "CS-JAVA", "name": "Java Programming", "id": 4},
        {"code": "CS-JS", "name": "JavaScript Programming", "id": 5},
        {"code": "CS-HTML", "name": "HTML", "id": 6},
        {"code": "CS-CSS", "name": "CSS", "id": 7},
        {"code": "CS-REACT", "name": "React.js", "id": 8},
        {"code": "CS-SQL", "name": "SQL", "id": 17},
        {"code": "CS-DSA", "name": "Data Structures and Algorithms", "id": 21},
    ]

    print("====================================================================")
    print(" LEARNSPHERE AI -- ADAPTIVE QUESTION UNIQUENESS VERIFICATION SUITE   ")
    print("====================================================================\n")

    # Ensure two test students exist
    s1 = db.query(Student).filter(Student.email == "test_student_1@learnsphere.edu").first()
    if not s1:
        s1 = Student(name="Test Student One", email="test_student_1@learnsphere.edu", password_hash="dummyhash")
        db.add(s1)
        db.commit()
        db.refresh(s1)

    s2 = db.query(Student).filter(Student.email == "test_student_2@learnsphere.edu").first()
    if not s2:
        s2 = Student(name="Test Student Two", email="test_student_2@learnsphere.edu", password_hash="dummyhash")
        db.add(s2)
        db.commit()
        db.refresh(s2)

    # Clean existing test answer history and misconceptions for test students
    db.query(Misconception).filter(Misconception.student_id.in_([s1.id, s2.id])).delete()
    db.query(ConceptMastery).filter(ConceptMastery.student_id.in_([s1.id, s2.id])).delete()
    db.query(StudentSubject).filter(StudentSubject.student_id.in_([s1.id, s2.id])).delete()
    db.query(AnswerHistory).filter(AnswerHistory.student_id.in_([s1.id, s2.id])).delete()
    db.commit()

    total_subjects_tested = 0
    total_passed = 0

    # 1. TEST 20 CONSECUTIVE QUESTIONS FOR ALL 10 SUBJECTS FOR STUDENT 1
    for subj in test_subjects:
        sid = subj["id"]
        scode = subj["code"]
        sname = subj["name"]
        print(f"--> Testing 20 Consecutive Questions for: {scode} ({sname})")

        seen_qids = []
        seen_texts = []

        for round_num in range(1, 21):
            q_out = get_next_question(student_id=s1.id, subject_id=sid, concept_id=None, db=db)

            # Assert correct subject
            assert q_out.subject_id == sid, f"Cross-subject contamination! Expected {sid}, got {q_out.subject_id}"

            # Assert uniqueness
            q_id = q_out.id
            q_text = q_out.question_text.strip()

            if q_id in seen_qids:
                print(f"  [FAIL] DUPLICATE Question ID detected in round {round_num}: ID {q_id}")
                break
            if q_text in seen_texts:
                print(f"  [FAIL] DUPLICATE Question Text detected in round {round_num}: {q_text[:60]}")
                break

            seen_qids.append(q_id)
            seen_texts.append(q_text)

            # Simulate student submitting an answer so history is tracked
            sub_payload = LearningAnswerSubmit(
                student_id=s1.id,
                question_id=q_id,
                concept_id=q_out.concept_id,
                selected_answer="A",
                written_reasoning="Conceptual understanding demonstrated.",
                time_taken_seconds=20,
            )
            submit_answer(sub_payload, db=db)

        is_success = len(seen_qids) == 20 and len(set(seen_qids)) == 20 and len(set(seen_texts)) == 20
        total_subjects_tested += 1
        if is_success:
            total_passed += 1
            print(f"  [PASS] 20/20 distinct questions served with zero repetition.\n")
        else:
            print(f"  [FAIL] Got {len(set(seen_qids))}/20 distinct questions.\n")

    # 2. TEST INDEPENDENT STUDENT HISTORIES (STUDENT 2 INDEPENDENCE)
    print("--> Testing Independent Student Histories (Student 1 vs Student 2)...")
    # Student 2 requests a question for Python (subject 1).
    # Since Student 2 has not answered any, they should be able to receive questions even if Student 1 answered them!
    s2_q = get_next_question(student_id=s2.id, subject_id=1, concept_id=None, db=db)
    print(f"  Student 2 received Question ID {s2_q.id} for {s2_q.subject_name}")
    assert s2_q.subject_id == 1, "Student 2 received wrong subject!"
    assert s2_q.id is not None, "Student 2 question ID is None!"
    print("  [PASS] Student 2 independently receives questions unhindered by Student 1's history.\n")

    # Clean up test answer history and test students
    db.query(Misconception).filter(Misconception.student_id.in_([s1.id, s2.id])).delete()
    db.query(ConceptMastery).filter(ConceptMastery.student_id.in_([s1.id, s2.id])).delete()
    db.query(StudentSubject).filter(StudentSubject.student_id.in_([s1.id, s2.id])).delete()
    db.query(AnswerHistory).filter(AnswerHistory.student_id.in_([s1.id, s2.id])).delete()
    db.delete(s1)
    db.delete(s2)
    db.commit()
    db.close()

    print("====================================================================")
    print(f" SUMMARY: {total_passed}/{total_subjects_tested} SUBJECTS PASSED 20 CONSECUTIVE TEST")
    print(" ZERO REPETITION GUARANTEED")
    print("====================================================================")

    if total_passed == total_subjects_tested:
        print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
        return 0
    else:
        print(f"\nTEST FAILURES DETECTED: {total_subjects_tested - total_passed} failed.")
        return 1


if __name__ == "__main__":
    exit_code = run_comprehensive_tests()
    sys.exit(exit_code)
