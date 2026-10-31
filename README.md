# LearnSphere AI — B.Tech CSE Adaptive Educational Intelligence Platform

> **"Master Every Skill. Learn at Your Own Pace."**

LearnSphere AI is an enterprise-grade, full-stack AI-powered adaptive learning platform specifically engineered for **B.Tech Computer Science and Engineering** undergraduates and faculty.

Rather than a static dashboard or simple Q&A chatbot, LearnSphere AI features a **cognitive learner model**, **real-time code reasoning & misconception detection**, **adaptive question routing across 31 subjects**, **interactive knowledge prerequisite dependency graphs**, **secure JWT authentication**, and **Ebbinghaus-based spaced repetition scheduling**.

---

## 🌟 Key Features

1. **Comprehensive B.Tech CSE Curriculum (6 Categories, 31 Subjects, 43+ Concepts)**:
   - **Category A: Programming Languages**: Python Programming, C Programming, C++ Programming, Java Programming, JavaScript Programming.
   - **Category B: Frontend Development**: HTML, CSS, JavaScript, React.js, Tailwind CSS, Bootstrap.
   - **Category C: Backend Development**: Node.js, Express.js, Python FastAPI, REST API Development, Authentication and Authorization.
   - **Category D: Database Management**: DBMS Fundamentals, SQL, MySQL, MongoDB, Database Design.
   - **Category E: Computer Science Fundamentals**: Data Structures and Algorithms, Operating Systems, Computer Networks, Computer Organization, Object-Oriented Programming.
   - **Category F: Artificial Intelligence**: Artificial Intelligence, Machine Learning, Deep Learning, Generative AI, Prompt Engineering, AI Agents and Agentic AI.

2. **Secure Authentication & Route Protection**:
   - PBKDF2-HMAC-SHA256 password hashing with salt (100,000 rounds).
   - RFC 7519 HS256 JWT tokens with automatic frontend bearer token interceptors.
   - Dedicated Public routes (`/`, `/login`, `/register`), Protected student routes (`/dashboard`, `/assessment`, `/learn`, `/mastery`, `/revisions`, `/profile`), and Teacher routes (`/teacher`).
   - Clean public landing page without exposed student dashboards.

3. **Cognitive Programming Misconception Detector (Google Gemini AI + Heuristic Fallback)**:
   - Analyzes code snippets, selected options, and student-written natural language reasoning.
   - Diagnoses mental model errors: mutable default parameter binding in Python, pointer dereferencing vs offset in C/C++, reference identity (`==`) vs value equality (`.equals()`), React state immutability, async event loop mechanics, HTTP idempotency, ACID transaction isolation, vector embedding spaces, and agentic perceive-plan-act loops.
   - Returns structured JSON with category, reasoning analysis, technical explanation, and actionable next steps.

4. **Dynamic Adaptive Question Engine**:
   - Generates questions with code snippets, output predictions, debugging challenges, and conceptual inquiries across Easy/Medium/Hard tiers.
   - Targets the student's weakest prerequisite concepts in their enrolled subjects.
   - Avoids repeating recently answered questions.

5. **Subject-Independent Deterministic Mastery Engine**:
   - Base deltas: Easy (+5, -3), Medium (+8, -5), Hard (+12, -7).
   - Multipliers by understanding: Good (1.2), Partial (0.8), Poor (0.5 correct / 1.3 incorrect).
   - Bounded: max increase +15%, max decrease -10% per attempt. Clamped to [0.0, 100.0].

6. **Automated Spaced Repetition (Revision Scheduler)**:
   - Ebbinghaus forgetting curve intervals: Weak (<40%): **1 day** review (High Priority), Developing (40–70%): **3 days** (Medium Priority), Mastered (>70%): **7 days** (Low Priority).
   - One-click completion tracking and forgetting risk calculation.

7. **B.Tech CSE Knowledge Dependency Graph**:
   - Interactive SVG dependency graph demonstrating topic prerequisites (e.g. C/Python → Data Structures → Algorithms; HTML/CSS/JS → React; Node.js/FastAPI → REST APIs → Auth; DBMS/SQL → DB Design; Python → ML → Deep Learning → GenAI → AI Agents).
   - Color-coded node rings displaying live student mastery states.

8. **Faculty & Cohort Analytics Dashboard**:
   - Cohort-wide metrics: Class Average Mastery, Critical Intervention Watchlist (<40% overall mastery), Core Subject Performance Breakdown, Lowest Concept Masteries, and Live Diagnosed Misconception Feed.

---

## 🏗️ Architecture & Technology Stack

```
learnsphere-ai/
├── backend/
│   ├── app/
│   │   ├── ai/                 # Gemini API client, CS misconception detector & question generator
│   │   ├── database/           # SQLite schema, engine, and B.Tech CSE seed scripts
│   │   ├── models/             # SQLAlchemy ORM models (Students, Subjects, Topics, Concepts, Enrollments...)
│   │   ├── routes/             # FastAPI routers (auth, subjects, concepts, students, assessment, learning, revisions, teacher)
│   │   ├── schemas/            # Pydantic v2 validation models
│   │   ├── services/           # Deterministic mastery algorithm & spaced repetition logic
│   │   └── utils/              # PBKDF2 hashing, HS256 JWT security & calculation utilities
│   ├── main.py                 # FastAPI application with CORS & lifespan DB init
│   ├── requirements.txt        # Backend dependencies
│   ├── test_api.py             # 14-point live integration test suite
│   └── test_student_journey.py # End-to-end B.Tech CSE student journey verification
├── frontend/
│   ├── src/
│   │   ├── components/         # Navbar, QuestionCard, FeedbackCard, MasteryBar, KnowledgeGraph...
│   │   ├── context/            # AuthContext (JWT management, login, register, logout)
│   │   ├── pages/              # LandingPage, LoginPage, RegisterPage, Dashboard, DiagnosticAssessment...
│   │   ├── services/           # Centralized Axios API client with Bearer auth interceptor
│   │   ├── utils/              # Color mappers & formatters
│   │   ├── App.jsx             # React Router v6 route configuration & ProtectedRoute guards
│   │   └── main.jsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
└── README.md
```

- **Frontend**: React 19, Vite, Tailwind CSS, Framer Motion, Recharts, React Icons, React Router v6, Axios
- **Backend**: Python 3.10+, FastAPI, SQLAlchemy 2.0, Pydantic v2, Uvicorn, Google Generative AI SDK, PBKDF2, HS256 JWT
- **Database**: SQLite with persistent relational schema

---

## 🚀 Quickstart & Verification

### 1. Backend Setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 3. Run Automated Tests
```bash
# Run 14-point API integration tests
cd backend
python test_api.py

# Run Complete Student Journey Simulation
python test_student_journey.py

# Run Frontend Production Build
cd ../frontend
npm run build
```
