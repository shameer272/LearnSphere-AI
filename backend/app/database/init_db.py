"""
Database initialization and curriculum seeding for LearnSphere AI.
Transforms curriculum to B.Tech Computer Science and Engineering across 6 categories.
"""
import logging
from datetime import datetime, timedelta
import random

from sqlalchemy.orm import Session

from app.database.db import engine, Base, SessionLocal
from app.models.models import (
    Student,
    Subject,
    Topic,
    Concept,
    StudentSubject,
    Question,
    ConceptMastery,
    AnswerHistory,
    RevisionSchedule,
    Assessment,
)
from app.ai.fallback_questions import FALLBACK_QUESTIONS
from app.utils.security import hash_password

logger = logging.getLogger(__name__)

# ── Curriculum Specification: 6 B.Tech CSE Categories ──────────────────────────
CSE_CURRICULUM = [
    {
        "category": "Programming Languages",
        "subjects": [
            {
                "code": "CS-PY",
                "name": "Python Programming",
                "description": "Core Python, data structures, OOP, decorators, generators, and standard library.",
                "icon": "FiCode",
                "topics": [
                    {
                        "name": "Core Syntax and Data Types",
                        "concepts": [
                            {"name": "Mutable vs Immutable Objects", "desc": "Lists, dicts, sets vs ints, strings, tuples, and parameter binding", "prereqs": []},
                            {"name": "List Slicing and Negative Indexing", "desc": "Sequence indexing, slicing mechanics, stride and reverse traversal", "prereqs": []},
                            {"name": "List Comprehensions & Generator Expressions", "desc": "Memory-efficient iterations, filtering and mapping semantics", "prereqs": [1]},
                        ]
                    },
                    {
                        "name": "Pythonic Functions and OOP",
                        "concepts": [
                            {"name": "Decorators and First-Class Functions", "desc": "Higher-order functions, closures, functools.wraps, and wrapper caching", "prereqs": [1]},
                            {"name": "Dunder Methods and Class Attributes", "desc": "__init__, __str__, __repr__, slots, and class vs instance attributes", "prereqs": [4]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-C",
                "name": "C Programming",
                "description": "Procedural programming, memory addresses, pointer arithmetic, dynamic memory allocation.",
                "icon": "FiCpu",
                "topics": [
                    {
                        "name": "Pointers and Memory",
                        "concepts": [
                            {"name": "Pointers and Memory Addresses", "desc": "Pointer dereferencing, void pointers, pass-by-reference simulation", "prereqs": []},
                            {"name": "Dynamic Memory Allocation (malloc, free)", "desc": "Heap vs stack memory management, memory leaks, and dangling pointers", "prereqs": [6]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-CPP",
                "name": "C++ Programming",
                "description": "Object-oriented C++, STL containers, virtual tables, RAII, templates, and move semantics.",
                "icon": "FiLayers",
                "topics": [
                    {
                        "name": "Advanced OOP and STL",
                        "concepts": [
                            {"name": "Virtual Functions and Polymorphism", "desc": "vptr, vtable dynamic dispatch, abstract classes, virtual destructors", "prereqs": [6]},
                            {"name": "Standard Template Library (STL) Containers", "desc": "std::vector, std::map, iterators, amortized growth, complexity", "prereqs": [8]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-JAVA",
                "name": "Java Programming",
                "description": "Platform independence, JVM architecture, garbage collection, collections framework.",
                "icon": "FiBox",
                "topics": [
                    {
                        "name": "Java Core and Memory Model",
                        "concepts": [
                            {"name": "String Pool and Equality Operators", "desc": "String interning, heap allocation, == vs .equals(), immutable string buffer", "prereqs": []},
                            {"name": "Java Collections Framework", "desc": "ArrayList vs LinkedList, HashMap internal hashing, collision resolution", "prereqs": [10]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-JS",
                "name": "JavaScript Programming",
                "description": "ECMAScript fundamentals, event loop, closures, promises, async/await, and modern ES6+.",
                "icon": "FiZap",
                "topics": [
                    {
                        "name": "Scope and Asynchrony",
                        "concepts": [
                            {"name": "Closures and Lexical Scope", "desc": "Scope chain, let vs const vs var, hoisting, and enclosed variable references", "prereqs": []},
                            {"name": "Promises and Async/Await", "desc": "Microtask queue, promise chaining, error propagation with try/catch", "prereqs": [12]},
                        ]
                    }
                ]
            },
        ]
    },
    {
        "category": "Frontend Development",
        "subjects": [
            {
                "code": "CS-HTML",
                "name": "HTML",
                "description": "Semantic markup, accessibility, modern forms, SEO, web storage.",
                "icon": "FiLayout",
                "topics": [
                    {
                        "name": "Structure and Semantics",
                        "concepts": [
                            {"name": "Semantic Elements and Accessibility", "desc": "header, nav, main, article, section, ARIA landmarks and screen readers", "prereqs": []},
                        ]
                    }
                ]
            },
            {
                "code": "CS-CSS",
                "name": "CSS",
                "description": "Box model, Flexbox, CSS Grid, animations, responsive design, media queries.",
                "icon": "FiEye",
                "topics": [
                    {
                        "name": "Layouts and Box Model",
                        "concepts": [
                            {"name": "CSS Box Model and Box-Sizing", "desc": "Content, padding, border, margin calculations, box-sizing: border-box", "prereqs": [14]},
                            {"name": "CSS Flexbox and Grid Layouts", "desc": "Main axis, cross axis, grid template areas, fractional units (fr), alignment", "prereqs": [15]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-REACT",
                "name": "React.js",
                "description": "Component architecture, virtual DOM, hooks, state management, effect lifecycle.",
                "icon": "FiRadio",
                "topics": [
                    {
                        "name": "React Hooks and Component Architecture",
                        "concepts": [
                            {"name": "State Immutability and useEffect Hook", "desc": "useState setter mechanics, shallow comparison, effect dependencies and cleanup", "prereqs": [12, 13]},
                            {"name": "Custom Hooks and Context API", "desc": "Extracting reusable stateful logic, avoiding prop drilling, memoization", "prereqs": [17]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-TAILWIND",
                "name": "Tailwind CSS",
                "description": "Utility-first CSS, responsive prefixes, dark mode, JIT compiler, theme customization.",
                "icon": "FiFeather",
                "topics": [
                    {
                        "name": "Utility Workflows",
                        "concepts": [
                            {"name": "Flexbox and Responsive Utilities", "desc": "Screen breakpoints (sm, md, lg), spacing scales, arbitrary values, flex utils", "prereqs": [15]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-BOOTSTRAP",
                "name": "Bootstrap",
                "description": "12-column grid system, component library, utility classes, responsive breakpoints.",
                "icon": "FiGrid",
                "topics": [
                    {
                        "name": "Grid and Components",
                        "concepts": [
                            {"name": "12-Column Grid System", "desc": "Containers, rows, column wrapping, gutters, offset classes", "prereqs": [15]},
                        ]
                    }
                ]
            },
        ]
    },
    {
        "category": "Backend Development",
        "subjects": [
            {
                "code": "CS-NODE",
                "name": "Node.js",
                "description": "Non-blocking event-driven architecture, event loop, streams, buffers, file system.",
                "icon": "FiServer",
                "topics": [
                    {
                        "name": "Runtime Architecture",
                        "concepts": [
                            {"name": "Event Loop and Asynchronous I/O", "desc": "Phases of libuv event loop, microtask queues, process.nextTick vs setImmediate", "prereqs": [12, 13]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-EXPRESS",
                "name": "Express.js",
                "description": "Routing, middleware pipeline, request/response lifecycle, error handling.",
                "icon": "FiTerminal",
                "topics": [
                    {
                        "name": "Middleware and Routing",
                        "concepts": [
                            {"name": "Middleware Chain and Error Handlers", "desc": "next() execution, app.use vs router, error middleware signature (err, req, res, next)", "prereqs": [21]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-FASTAPI",
                "name": "Python FastAPI",
                "description": "Modern ASGI framework, automatic OpenAPI docs, Pydantic type validation, async routes.",
                "icon": "FiZap",
                "topics": [
                    {
                        "name": "FastAPI Core",
                        "concepts": [
                            {"name": "Dependency Injection and Pydantic Validation", "desc": "Depends(), Request lifecycle, Pydantic v2 schemas, automated documentation", "prereqs": [1, 2]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-REST",
                "name": "REST API Development",
                "description": "REST architectural constraints, resource URIs, HTTP methods, headers, pagination, CORS.",
                "icon": "FiGlobe",
                "topics": [
                    {
                        "name": "API Architecture",
                        "concepts": [
                            {"name": "HTTP Idempotency and Status Codes", "desc": "Safe vs idempotent methods, 2xx, 3xx, 4xx, 5xx semantics, PUT vs PATCH", "prereqs": []},
                        ]
                    }
                ]
            },
            {
                "code": "CS-AUTH",
                "name": "Authentication and Authorization",
                "description": "JWT, OAuth2, session-based auth, RBAC, password hashing, salted PBKDF2/bcrypt.",
                "icon": "FiLock",
                "topics": [
                    {
                        "name": "Security and Tokens",
                        "concepts": [
                            {"name": "JWT Security and Password Hashing", "desc": "Header.Payload.Signature structure, claims, PBKDF2/bcrypt salt, token expiration", "prereqs": [24]},
                        ]
                    }
                ]
            },
        ]
    },
    {
        "category": "Database Management",
        "subjects": [
            {
                "code": "CS-DBMS",
                "name": "DBMS Fundamentals",
                "description": "Database architectures, relational model, transaction management, indexing, concurrency.",
                "icon": "FiDatabase",
                "topics": [
                    {
                        "name": "Transaction Management",
                        "concepts": [
                            {"name": "ACID Properties and Transactions", "desc": "Atomicity, Consistency, Isolation levels, Durability, write-ahead logging", "prereqs": []},
                        ]
                    }
                ]
            },
            {
                "code": "CS-SQL",
                "name": "SQL",
                "description": "Structured Query Language, DDL, DML, DQL, joins, subqueries, aggregation, window functions.",
                "icon": "FiHardDrive",
                "topics": [
                    {
                        "name": "Querying and Aggregations",
                        "concepts": [
                            {"name": "JOIN Operations and Aggregations", "desc": "INNER, LEFT, RIGHT, FULL OUTER joins, GROUP BY, HAVING, subquery optimization", "prereqs": [26]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-MYSQL",
                "name": "MySQL",
                "description": "InnoDB storage engine, B-Tree indexes, query execution plans, foreign keys.",
                "icon": "FiDatabase",
                "topics": [
                    {
                        "name": "Storage and Indexing",
                        "concepts": [
                            {"name": "InnoDB B-Tree Indexing and EXPLAIN", "desc": "Clustered vs secondary indexes, index scans, coverage indexes", "prereqs": [27]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-MONGO",
                "name": "MongoDB",
                "description": "NoSQL document store, BSON, aggregation pipeline, replica sets, sharding.",
                "icon": "FiLayers",
                "topics": [
                    {
                        "name": "Document Modeling",
                        "concepts": [
                            {"name": "Document Schemas and Aggregation Pipeline", "desc": "Embedding vs referencing, $match, $group, $lookup, document validation", "prereqs": [26]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-DBDESIGN",
                "name": "Database Design",
                "description": "Entity-Relationship modeling, functional dependencies, normalization, denormalization.",
                "icon": "FiShare2",
                "topics": [
                    {
                        "name": "Normalization",
                        "concepts": [
                            {"name": "Database Normalization (1NF, 2NF, 3NF, BCNF)", "desc": "Lossless joins, dependency preservation, eliminating anomalies", "prereqs": [26, 27]},
                        ]
                    }
                ]
            },
        ]
    },
    {
        "category": "Computer Science Fundamentals",
        "subjects": [
            {
                "code": "CS-DSA",
                "name": "Data Structures and Algorithms",
                "description": "Arrays, linked lists, trees, graphs, sorting, searching, dynamic programming.",
                "icon": "FiTrendingUp",
                "topics": [
                    {
                        "name": "Complexity and Data Structures",
                        "concepts": [
                            {"name": "Time Complexity and Big-O Notation", "desc": "Asymptotic bounds (O, Omega, Theta), recurrence relations, master theorem", "prereqs": []},
                            {"name": "Trees and Binary Search Trees", "desc": "BST invariant, tree traversals (inorder, preorder, postorder), AVL rotations", "prereqs": [31]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-OS",
                "name": "Operating Systems",
                "description": "Processes, threads, CPU scheduling, synchronization, memory management, file systems.",
                "icon": "FiCpu",
                "topics": [
                    {
                        "name": "Concurrency and Memory",
                        "concepts": [
                            {"name": "Process Synchronization and Deadlocks", "desc": "Semaphores, mutexes, race conditions, critical section, Coffman conditions", "prereqs": []},
                            {"name": "Virtual Memory and Paging", "desc": "Page tables, TLB, page faults, FIFO, LRU replacement policies", "prereqs": [33]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-CN",
                "name": "Computer Networks",
                "description": "OSI & TCP/IP models, routing protocols, transport layer, DNS, HTTP, sockets.",
                "icon": "FiGlobe",
                "topics": [
                    {
                        "name": "Protocols and Layers",
                        "concepts": [
                            {"name": "TCP vs UDP and 3-Way Handshake", "desc": "Reliable byte stream vs datagram, congestion control, windowing, SYN/ACK", "prereqs": []},
                        ]
                    }
                ]
            },
            {
                "code": "CS-COA",
                "name": "Computer Organization",
                "description": "Instruction set architectures, ALU, CPU datapath, pipelining, memory hierarchy, cache.",
                "icon": "FiCpu",
                "topics": [
                    {
                        "name": "CPU Architecture",
                        "concepts": [
                            {"name": "Pipelining and Cache Memory Hierarchy", "desc": "Pipeline hazards (data, structural, branch), L1/L2/L3 cache associativity", "prereqs": []},
                        ]
                    }
                ]
            },
            {
                "code": "CS-OOP",
                "name": "Object-Oriented Programming",
                "description": "Encapsulation, inheritance, polymorphism, abstraction, design patterns, SOLID principles.",
                "icon": "FiBox",
                "topics": [
                    {
                        "name": "OOP Principles and Design",
                        "concepts": [
                            {"name": "SOLID Principles and Design Patterns", "desc": "Single responsibility, open-closed, Liskov, interface segregation, dependency inversion", "prereqs": [8, 10]},
                        ]
                    }
                ]
            },
        ]
    },
    {
        "category": "Artificial Intelligence",
        "subjects": [
            {
                "code": "CS-AI",
                "name": "Artificial Intelligence",
                "description": "Knowledge representation, search algorithms (A*, minimax), constraint satisfaction.",
                "icon": "FiTarget",
                "topics": [
                    {
                        "name": "Heuristic Search and Problem Solving",
                        "concepts": [
                            {"name": "Heuristic Search and A* Algorithm", "desc": "Admissible heuristics, consistent heuristics, optimal pathfinding, evaluation functions", "prereqs": [31]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-ML",
                "name": "Machine Learning",
                "description": "Supervised, unsupervised, regression, classification, clustering, model evaluation.",
                "icon": "FiTrendingUp",
                "topics": [
                    {
                        "name": "Supervised Learning and Generalization",
                        "concepts": [
                            {"name": "Overfitting and Regularization Techniques", "desc": "Bias-variance tradeoff, L1/L2 regularization, cross-validation, dropout", "prereqs": [1]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-DL",
                "name": "Deep Learning",
                "description": "Artificial neural networks, backpropagation, CNNs, RNNs, transformers, attention mechanisms.",
                "icon": "FiZap",
                "topics": [
                    {
                        "name": "Neural Networks and Backpropagation",
                        "concepts": [
                            {"name": "Neural Networks and Gradient Descent", "desc": "Activation functions (ReLU, Sigmoid), chain rule backprop, Adam optimizer", "prereqs": [39]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-GENAI",
                "name": "Generative AI",
                "description": "Large language models, diffusion models, fine-tuning, RAG, vector embeddings.",
                "icon": "FiRadio",
                "topics": [
                    {
                        "name": "LLMs and Embeddings",
                        "concepts": [
                            {"name": "Retrieval-Augmented Generation (RAG) Architecture", "desc": "Dense vector retrieval, cosine similarity, context chunking, grounding", "prereqs": [39, 40]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-PROMPT",
                "name": "Prompt Engineering",
                "description": "Few-shot prompting, Chain-of-Thought, system instructions, structured output parsing.",
                "icon": "FiTerminal",
                "topics": [
                    {
                        "name": "Prompt Architectures",
                        "concepts": [
                            {"name": "Chain-of-Thought and Structured Generation", "desc": "Reasoning tokens, few-shot exemplars, JSON schema constraints, prompt security", "prereqs": [41]},
                        ]
                    }
                ]
            },
            {
                "code": "CS-AGENTS",
                "name": "AI Agents and Agentic AI",
                "description": "Autonomous agents, ReAct loops, tool execution, multi-agent collaboration, memory.",
                "icon": "FiCpu",
                "topics": [
                    {
                        "name": "Autonomous Agents",
                        "concepts": [
                            {"name": "Agentic AI Architectures and Tool Use", "desc": "Perceive-plan-act loop, tool routing, observation feedback, goal decomposition", "prereqs": [41, 42]},
                        ]
                    }
                ]
            },
        ]
    },
]

def init_database() -> None:
    """
    Create all tables and seed the B.Tech CSE curriculum and fallback question repository.
    Fully idempotent and purely curriculum-based: never generates dummy or pre-seeded students.
    """
    logger.info("Initializing LearnSphere AI B.Tech CSE database schema...")
    Base.metadata.create_all(bind=engine)

    # Enforce SQLite UNIQUE constraints and indexes
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_student_email ON students(email)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_code ON subjects(code)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_name ON subjects(name)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_topic ON topics(subject_id, name)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_subject_concept ON concepts(subject_id, name)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_concept_question ON questions(concept_id, question_text)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_student_subject ON student_subjects(student_id, subject_id)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_student_concept ON concept_mastery(student_id, concept_id)")
        conn.exec_driver_sql("CREATE UNIQUE INDEX IF NOT EXISTS uq_student_pending_revision ON revision_schedules(student_id, concept_id) WHERE is_completed = 0")

    db = SessionLocal()
    try:
        # 1. Idempotent Subject, Topic, and Concept Seeding
        logger.info("Synchronizing B.Tech CSE subjects, topics, and concepts...")
        order_counter = 1

        for cat_data in CSE_CURRICULUM:
            category_name = cat_data["category"]
            for sub_data in cat_data["subjects"]:
                subject = db.query(Subject).filter(Subject.code == sub_data["code"]).first()
                if not subject:
                    subject = Subject(
                        category=category_name,
                        name=sub_data["name"],
                        code=sub_data["code"],
                        description=sub_data["description"],
                        icon=sub_data["icon"],
                        order_index=order_counter,
                    )
                    db.add(subject)
                    db.flush()
                order_counter += 1

                for t_idx, top_data in enumerate(sub_data.get("topics", [])):
                    topic = db.query(Topic).filter(
                        Topic.subject_id == subject.id,
                        Topic.name == top_data["name"],
                    ).first()
                    if not topic:
                        topic = Topic(
                            subject_id=subject.id,
                            name=top_data["name"],
                            order_index=t_idx + 1,
                        )
                        db.add(topic)
                        db.flush()

                    for c_idx, con_data in enumerate(top_data.get("concepts", [])):
                        concept = db.query(Concept).filter(
                            Concept.subject_id == subject.id,
                            Concept.name == con_data["name"],
                        ).first()
                        if not concept:
                            concept = Concept(
                                subject_id=subject.id,
                                topic_id=topic.id,
                                name=con_data["name"],
                                description=con_data["desc"],
                                order_index=c_idx + 1,
                                prerequisites=con_data.get("prereqs", []),
                            )
                            db.add(concept)
                            db.flush()

        db.commit()

        # 2. Idempotent Question Seeding from FALLBACK_QUESTIONS
        logger.info("Synchronizing curated B.Tech CSE question bank...")
        for q_data in FALLBACK_QUESTIONS:
            subject = db.query(Subject).filter(Subject.code == q_data["subject_code"]).first()
            if not subject:
                continue
            concept = db.query(Concept).filter(
                Concept.subject_id == subject.id,
                Concept.name == q_data["concept_name"]
            ).first()
            if not concept:
                concept = db.query(Concept).filter(Concept.subject_id == subject.id).first()
            if not concept:
                continue

            q_text_clean = q_data["question_text"].strip()
            existing_q = db.query(Question).filter(
                Question.concept_id == concept.id,
                Question.question_text == q_text_clean,
            ).first()

            if not existing_q:
                q = Question(
                    subject_id=subject.id,
                    concept_id=concept.id,
                    question_type=q_data.get("question_type", "mcq"),
                    question_text=q_text_clean,
                    code_snippet=q_data.get("code_snippet"),
                    options=q_data["options"],
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation"),
                    difficulty=q_data.get("difficulty", "medium"),
                    misconception_targets=q_data.get("misconception_targets", []),
                    is_ai_generated=False,
                )
                db.add(q)
        db.commit()
        logger.info("LearnSphere AI database curriculum synchronization completed successfully.")

    except Exception as exc:
        db.rollback()
        logger.error("Error during database initialization: %s", exc)
        raise
    finally:
        db.close()
