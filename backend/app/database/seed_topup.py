"""
Top-up seed to ensure every single core CSE subject has 25+ questions.
"""
import json
import sqlite3
from datetime import datetime

DB_PATH = "backend/learnsphere_cse.db"

EXTRA_QUESTIONS = [
    # ── HTML ──
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What does the HTML <progress> element represent compared to <meter>?",
        "code_snippet": "<progress value=\"70\" max=\"100\"></progress>\n<meter value=\"0.6\">60%</meter>",
        "options": {"A": "<progress> represents the completion progress of a task; <meter> represents a scalar measurement within a known range", "B": "<progress> is for audio; <meter> is for battery", "C": "They are synonymous and render identically", "D": "<meter> is deprecated in HTML5"},
        "correct_answer": "A",
        "explanation": "<progress> indicates how much of a task has been completed (dynamic progression), whereas <meter> represents a gauge or gauge measurement within known bounds.",
        "difficulty": "medium",
        "misconception_targets": ["progress vs meter semantic distinction"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the primary role of the `aria-expanded=\"true|false\"` attribute?",
        "code_snippet": None,
        "options": {"A": "Informs assistive technologies whether an accordion or dropdown menu container is currently open or collapsed", "B": "Zooms the container text size", "C": "Automatically triggers CSS animations", "D": "Toggles full screen display"},
        "correct_answer": "A",
        "explanation": "aria-expanded indicates the state of collapsible elements (e.g. navigation menus, accordions, trees) to screen readers.",
        "difficulty": "easy",
        "misconception_targets": ["ARIA state attributes for interactive widgets"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "Why should <button> be used for interactive click handlers rather than a <div onClick=... >?",
        "code_snippet": None,
        "options": {"A": "<button> is keyboard focusable via Tab, responds to Enter/Space keypresses, and announces as a button to screen readers by default", "B": "div tags cannot have Javascript click listeners", "C": "button renders faster in the browser engine", "D": "div tags cause CORS errors"},
        "correct_answer": "A",
        "explanation": "Native buttons have built-in keyboard accessibility, focus management, and accessibility tree role without needing manual tabindex or keydown handlers.",
        "difficulty": "easy",
        "misconception_targets": ["Div with onClick vs native semantic button accessibility"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the purpose of the <picture> element with multiple <source> child elements?",
        "code_snippet": "<picture>\n  <source media=\"(min-width: 800px)\" srcset=\"large.webp\">\n  <source media=\"(min-width: 450px)\" srcset=\"medium.webp\">\n  <img src=\"small.jpg\" alt=\"Landscape\">\n</picture>",
        "options": {"A": "Art direction and serving optimized modern image formats (e.g. WebP/AVIF) based on media query screen widths", "B": "Plays sequential image slide animations", "C": "Combines images into a CSS sprite", "D": "Applies real-time CSS filters to images"},
        "correct_answer": "A",
        "explanation": "<picture> allows web developers to provide multiple alternate image sources optimized for different screen resolutions and formats, falling back to <img>.",
        "difficulty": "medium",
        "misconception_targets": ["Responsive image art direction with picture element"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What does the `sandbox` attribute on an <iframe> do by default?",
        "code_snippet": "<iframe src=\"untrusted.html\" sandbox></iframe>",
        "options": {"A": "Applies maximum security restrictions: disables scripts, form submissions, popups, and treats content as unique origin", "B": "Runs the iframe in a separate browser window", "C": "Caches the iframe in indexedDB", "D": "Disables CSS styling inside iframe"},
        "correct_answer": "A",
        "explanation": "An empty sandbox attribute enforces maximum isolation, restricting all dangerous capabilities unless explicitly re-enabled with tokens like allow-scripts.",
        "difficulty": "medium",
        "misconception_targets": ["Iframe sandboxing security model"]
    },
    {
        "subject_code": "CS-HTML",
        "concept_name": "Semantic Elements and Accessibility",
        "question_type": "conceptual",
        "question_text": "What is the purpose of the `download` attribute on an HTML anchor tag?",
        "code_snippet": "<a href=\"report.pdf\" download=\"AnnualReport.pdf\">Download Report</a>",
        "options": {"A": "Prompts the browser to download the linked URL as a local file with the specified filename rather than navigating to it", "B": "Encrypts the downloaded file with SSL", "C": "Forces file compression into a zip archive", "D": "Triggers background torrent downloading"},
        "correct_answer": "A",
        "explanation": "The download attribute instructs browsers to save the target resource locally using the provided value as suggested filename.",
        "difficulty": "easy",
        "misconception_targets": ["HTML5 anchor download attribute behavior"]
    },

    # ── CSS ──
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "What does `align-self` do in CSS Flexbox?",
        "code_snippet": ".item {\n  align-self: flex-end;\n}",
        "options": {"A": "Overrides the parent flex container's `align-items` property for that specific individual flex child", "B": "Overrides justify-content for that child", "C": "Aligns the container relative to its sibling", "D": "Inverts the flex direction for that child"},
        "correct_answer": "A",
        "explanation": "align-self allows individual flex items to override the container's default cross-axis alignment rule.",
        "difficulty": "easy",
        "misconception_targets": ["align-self individual override of align-items"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "conceptual",
        "question_text": "What is a Block Formatting Context (BFC) and which property triggers it cleanly?",
        "code_snippet": ".container {\n  display: flow-root;\n}",
        "options": {"A": "display: flow-root creates a BFC containing internal floats and preventing margin collapsing with outside elements without unintended side effects", "B": "display: inline", "C": "color: inherit", "D": "font-weight: bold"},
        "correct_answer": "A",
        "explanation": "display: flow-root establishes a new Block Formatting Context, cleanly containing child floats and clearing margins without overflow: hidden clipping.",
        "difficulty": "hard",
        "misconception_targets": ["Block formatting context triggers: display flow-root vs overflow hidden"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "In CSS Grid, what is the meaning of the `min-content` keyword?",
        "code_snippet": "grid-template-columns: min-content 1fr;",
        "options": {"A": "Sizes the column to the smallest possible width without causing text overflow (the width of the longest word or element)", "B": "Sets column width to 0", "C": "Equal to 1 pixel", "D": "Expands column to fill viewport"},
        "correct_answer": "A",
        "explanation": "min-content is the intrinsic minimum width: the narrowest size the content can fit without overflowing (e.g. longest unbreakable word).",
        "difficulty": "medium",
        "misconception_targets": ["min-content vs max-content intrinsic sizing"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "output_prediction",
        "question_text": "What happens when `overflow: hidden` is applied to a container containing floated children?",
        "code_snippet": ".clearfix {\n  overflow: hidden;\n}",
        "options": {"A": "It establishes a new BFC, causing the container to expand to enclose its floated child elements", "B": "Floats are removed from the DOM", "C": "The container collapses to height 0", "D": "Floats are converted to inline elements"},
        "correct_answer": "A",
        "explanation": "overflow values other than visible trigger a BFC, forcing the parent to encompass all child floats to calculate its height.",
        "difficulty": "medium",
        "misconception_targets": ["Clearfix mechanics and BFC float containment"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Flexbox and Grid Layouts",
        "question_type": "conceptual",
        "question_text": "What does the `clamp(MIN, VAL, MAX)` function do in modern responsive CSS?",
        "code_snippet": "font-size: clamp(1rem, 2.5vw, 2rem);",
        "options": {"A": "Constrains a dynamic value between an absolute minimum and maximum boundary", "B": "Rounds numbers to nearest integer", "C": "Animates font-size between min and max", "D": "Disables font scaling"},
        "correct_answer": "A",
        "explanation": "clamp(min, preferred, max) selects the preferred value (e.g. 2.5vw) while guaranteeing it never drops below 1rem or exceeds 2rem.",
        "difficulty": "easy",
        "misconception_targets": ["Fluid typography using CSS clamp"]
    },
    {
        "subject_code": "CS-CSS",
        "concept_name": "CSS Box Model and Box-Sizing",
        "question_type": "conceptual",
        "question_text": "What is the difference between CSS custom properties (--variable) and preprocessor variables (Sass/Less)?",
        "code_snippet": ":root {\n  --brand-color: #6366f1;\n}",
        "options": {"A": "CSS variables exist in the live browser DOM, cascade down the tree, and can be read or modified dynamically via JavaScript", "B": "CSS variables are compiled away at build time", "C": "Sass variables cascade dynamically in runtime DOM", "D": "CSS variables cannot be used for colors"},
        "correct_answer": "A",
        "explanation": "Native CSS custom properties participate in the cascade, inherit down DOM subtrees, and update live in real-time when changed with JS.",
        "difficulty": "medium",
        "misconception_targets": ["Runtime CSS custom properties vs compile-time preprocessor variables"]
    },

    # ── SQL ──
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "What is the purpose of Common Table Expressions (WITH clause) in SQL?",
        "code_snippet": "WITH RankedScores AS (\n  SELECT student_id, score, DENSE_RANK() OVER (ORDER BY score DESC) as rnk\n  FROM assessments\n)\nSELECT student_id FROM RankedScores WHERE rnk <= 3;",
        "options": {"A": "Defines a temporary named result set (CTE) improving query modularity, readability, and enabling recursive hierarchical queries", "B": "Creates a permanent table on disk", "C": "Indexes the specified columns permanently", "D": "Disables query caching"},
        "correct_answer": "A",
        "explanation": "CTEs (WITH clause) allow breaking complex joins and window functions into readable named subqueries and support recursive execution.",
        "difficulty": "medium",
        "misconception_targets": ["CTE temporary lifecycle and recursive queries"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "What is an index seek vs an index scan in relational database execution plans?",
        "code_snippet": None,
        "options": {"A": "Index Seek navigates the B-Tree directly to specific matching rows; Index Scan reads all pages of the index sequentially", "B": "Index Seek is slower than Table Scan", "C": "Index Scan only works on primary keys", "D": "They are identical operations"},
        "correct_answer": "A",
        "explanation": "Index Seek uses the B-Tree root-to-leaf traversal with O(log N) operations. Index Scan traverses all index leaf nodes sequentially.",
        "difficulty": "medium",
        "misconception_targets": ["Index Seek vs Index Scan performance profile"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "What does CASE WHEN expression do when no ELSE branch is specified and no condition matches?",
        "code_snippet": "SELECT id, CASE WHEN score >= 90 THEN 'A' END as grade FROM results;",
        "options": {"A": "Returns NULL", "B": "Throws a SQL runtime error", "C": "Returns empty string", "D": "Returns 0"},
        "correct_answer": "A",
        "explanation": "If no WHEN branch evaluates to true and no ELSE clause is provided, the CASE expression evaluates to NULL.",
        "difficulty": "easy",
        "misconception_targets": ["Default NULL evaluation in CASE statements"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "conceptual",
        "question_text": "What is the ACID property 'Isolation' concerned with in DBMS?",
        "code_snippet": None,
        "options": {"A": "Ensuring concurrent transactions execute without interfering with one another (preventing dirty reads, non-repeatable reads, phantom reads)", "B": "Ensuring data is written to non-volatile disk", "C": "Ensuring all-or-nothing execution", "D": "Ensuring foreign key constraints are not violated"},
        "correct_answer": "A",
        "explanation": "Isolation guarantees that concurrently running transactions appear to execute sequentially, managed via transaction isolation levels.",
        "difficulty": "easy",
        "misconception_targets": ["ACID Isolation vs Atomicity vs Durability"]
    },
    {
        "subject_code": "CS-SQL",
        "concept_name": "JOIN Operations and Aggregations",
        "question_type": "sql_query",
        "question_text": "How does `TRUNCATE TABLE` differ from `DELETE FROM table` in SQL databases?",
        "code_snippet": None,
        "options": {"A": "TRUNCATE is a DDL operation that deallocates pages (faster, resets identity counter, minimal logging); DELETE is DML logging row deletions", "B": "DELETE cannot be rolled back; TRUNCATE can", "C": "TRUNCATE fires row-level triggers", "D": "They are completely identical"},
        "correct_answer": "A",
        "explanation": "TRUNCATE deallocates data pages directly, does not activate row-level triggers, resets identity seeds, and operates with minimal logging.",
        "difficulty": "medium",
        "misconception_targets": ["TRUNCATE DDL page deallocation vs DELETE DML row removal"]
    },

    # ── DSA ──
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "conceptual",
        "question_text": "What is the time complexity of building a Binary Heap of N elements using the bottom-up Heapify approach?",
        "code_snippet": None,
        "options": {"A": "O(N)", "B": "O(N log N)", "C": "O(N^2)", "D": "O(log N)"},
        "correct_answer": "A",
        "explanation": "Bottom-up heap construction runs in linear O(N) time because nodes near the leaves require significantly fewer sift-down swaps than root nodes (sum of h/2^h series).",
        "difficulty": "medium",
        "misconception_targets": ["Linear O(N) time of bottom-up build-heap vs O(N log N) successive insertions"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "In a Red-Black Tree, what is the maximum possible height of a tree with N internal nodes?",
        "code_snippet": None,
        "options": {"A": "2 * log2(N + 1)", "B": "N", "C": "log2(N)", "D": "N / 2"},
        "correct_answer": "A",
        "explanation": "Because no path can contain two consecutive red nodes and all paths share identical black-height, the longest path is at most twice the shortest, giving h <= 2 * log2(N + 1).",
        "difficulty": "hard",
        "misconception_targets": ["Red-Black tree maximum height invariant"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "conceptual",
        "question_text": "What is the average and worst-case time complexity of accessing an element by key in a well-designed Hash Table?",
        "code_snippet": None,
        "options": {"A": "Average O(1), Worst-case O(N)", "B": "Average O(log N), Worst-case O(N)", "C": "O(1) for both", "D": "O(N) for both"},
        "correct_answer": "A",
        "explanation": "Uniform hashing distributes keys into buckets in O(1) average time. If all keys hash to the same bucket (pathological collisions), lookup degrades to O(N).",
        "difficulty": "easy",
        "misconception_targets": ["Worst-case hash table collision complexity"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Time Complexity and Big-O Notation",
        "question_type": "conceptual",
        "question_text": "What is the Master Theorem asymptotic solution for T(N) = 2T(N/2) + O(N)?",
        "code_snippet": None,
        "options": {"A": "O(N log N)", "B": "O(N^2)", "C": "O(N)", "D": "O(log N)"},
        "correct_answer": "A",
        "explanation": "Here a = 2, b = 2, f(N) = O(N). Since log_b(a) = log_2(2) = 1 and f(N) = Theta(N^1), Case 2 applies, giving T(N) = Theta(N log N) (standard MergeSort recurrence).",
        "difficulty": "medium",
        "misconception_targets": ["Master Theorem Case 2 resolution"]
    },
    {
        "subject_code": "CS-DSA",
        "concept_name": "Trees and Binary Search Trees",
        "question_type": "conceptual",
        "question_text": "How many null pointer references exist in a binary tree with N nodes?",
        "code_snippet": None,
        "options": {"A": "N + 1", "B": "N - 1", "C": "2N", "D": "N / 2"},
        "correct_answer": "A",
        "explanation": "Every node has 2 pointer fields (2N total). Every node except the root has exactly one incoming edge (N - 1 edges used). Remaining null pointers = 2N - (N - 1) = N + 1.",
        "difficulty": "medium",
        "misconception_targets": ["Tree structural properties and null pointer count"]
    },
]


def run_topup():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT id, code, name FROM subjects")
    subjects = {r[1]: r[0] for r in cur.fetchall()}

    cur.execute("SELECT id, subject_id, name FROM concepts")
    concept_map = {}
    subject_first_concept = {}
    for cid, sid, cname in cur.fetchall():
        concept_map[(sid, cname.strip().lower())] = cid
        if sid not in subject_first_concept:
            subject_first_concept[sid] = cid

    inserted_count = 0
    now = datetime.utcnow().isoformat()

    for q in EXTRA_QUESTIONS:
        code = q["subject_code"]
        sid = subjects.get(code)
        if not sid:
            continue

        cname = q.get("concept_name", "").strip().lower()
        cid = concept_map.get((sid, cname))
        if not cid:
            cid = subject_first_concept.get(sid)

        if not cid:
            continue

        q_text = q["question_text"].strip()
        cur.execute("SELECT id FROM questions WHERE concept_id = ? AND question_text = ?", (cid, q_text))
        if cur.fetchone():
            continue

        cur.execute(
            """
            INSERT INTO questions (
                subject_id, concept_id, question_type, question_text,
                code_snippet, options, correct_answer, explanation,
                difficulty, misconception_targets, is_ai_generated, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                sid,
                cid,
                q.get("question_type", "mcq"),
                q_text,
                q.get("code_snippet"),
                json.dumps(q["options"]),
                q["correct_answer"],
                q.get("explanation", ""),
                q.get("difficulty", "medium"),
                json.dumps(q.get("misconception_targets", [])),
                0,
                now,
            ),
        )
        inserted_count += 1

    conn.commit()
    print(f"Top-up inserted {inserted_count} questions.")

    cur.execute(
        """
        SELECT s.id, s.code, s.name, count(q.id)
        FROM subjects s
        LEFT JOIN questions q ON q.subject_id = s.id
        WHERE s.code IN ('CS-PY', 'CS-C', 'CS-CPP', 'CS-JAVA', 'CS-JS', 'CS-HTML', 'CS-CSS', 'CS-REACT', 'CS-SQL', 'CS-DSA')
        GROUP BY s.id, s.code, s.name
        ORDER BY s.id
        """
    )
    for row in cur.fetchall():
        print(f"Subject {row[1]} ({row[2]}): {row[3]} questions in DB")

    conn.close()


if __name__ == "__main__":
    run_topup()
