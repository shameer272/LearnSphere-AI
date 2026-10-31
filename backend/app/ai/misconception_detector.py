"""
Programming Misconception Detector for LearnSphere AI.
Analyzes student reasoning in B.Tech Computer Science & Engineering using Gemini AI
with robust domain-specific heuristic fallbacks.
"""
import json
import logging
import re
from typing import Optional

from app.ai.gemini_client import get_gemini_client

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = """You are an expert Computer Science professor and senior software architect analyzing an engineering student's code understanding and reasoning.

Context:
Subject / Domain: {subject_name}
Concept: {concept_name}
Question: {question}
Code Snippet:
{code_snippet}
Correct Answer Option: {correct_answer}
Student Selected Option: {student_answer}
Student's Written Reasoning: {reasoning}

Tasks:
1. Determine if student's answer and reasoning are conceptually correct.
2. If incorrect or flawed, diagnose the exact conceptual misconception (e.g. mutable default argument mutation, reference vs value equality, variable hoisting vs block scope, state immutability in React, ACID isolation levels, RAG cosine similarity vs lexical search).
3. Explain WHY their mental model is flawed.

Return ONLY a valid JSON object with these exact keys:
{{
  "is_correct": true/false,
  "detected_misconception": "concise description of diagnosed misconception or null if fully correct",
  "misconception_category": "category name (e.g. 'Reference vs Value Equality', 'Async Event Loop Mechanics') or null",
  "reasoning_analysis": "insightful breakdown of the student's stated reasoning",
  "concept_understanding": "good/partial/poor",
  "explanation": "clear, authoritative technical explanation of why the correct option is right and how the concept behaves",
  "recommended_learning_action": "actionable next technical step or coding exercise",
  "suggested_difficulty": "easier/same/harder"
}}
"""

_REQUIRED_KEYS = {
    "is_correct",
    "detected_misconception",
    "misconception_category",
    "reasoning_analysis",
    "concept_understanding",
    "explanation",
    "recommended_learning_action",
    "suggested_difficulty",
}


def _extract_json(raw: str) -> dict:
    """Extract JSON from raw AI response text."""
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw.strip())


def _rule_based_fallback(
    is_correct: bool,
    difficulty: str = "medium",
    question: str = "",
    code_snippet: Optional[str] = None,
    student_answer: str = "",
    reasoning: Optional[str] = None,
    concept_name: str = "",
    subject_name: str = "",
) -> dict:
    """
    Rich rule-based diagnostic fallback for B.Tech Computer Science concepts.
    """
    q_lower = (question or "").lower()
    c_lower = (concept_name or "").lower()
    s_lower = (subject_name or "").lower()
    r_lower = (reasoning or "").lower()
    snippet_lower = (code_snippet or "").lower()

    if is_correct:
        analysis = (
            f"Strong technical reasoning aligned with core principles of {concept_name}."
            if reasoning and len(reasoning.strip()) > 3
            else "Correct answer option selected."
        )
        return {
            "is_correct": True,
            "detected_misconception": None,
            "misconception_category": None,
            "reasoning_analysis": analysis,
            "concept_understanding": "good",
            "explanation": f"Correct! Your selection matches standard {concept_name or 'Computer Science'} principles.",
            "recommended_learning_action": "Progress to advanced edge cases and implementation projects.",
            "suggested_difficulty": "harder" if difficulty != "hard" else "same",
            "is_ai_generated": False,
        }

    # Targeted Computer Science misconception heuristics
    detected_misconception = "Fundamental programming misconception or incorrect mental model."
    misconception_cat = "Conceptual Misapplication"
    explanation = f"Review the fundamental semantics and specification of {concept_name}."
    rec_action = "Trace code step-by-step and verify memory or runtime behavior in a REPL/debugger."

    # Python
    if "mutable" in c_lower or "list" in c_lower or "append" in snippet_lower:
        detected_misconception = "Assuming default arguments are re-evaluated on each function call or confusing mutable reference with new object."
        misconception_cat = "Mutable Object Reference Binding"
        explanation = "In Python, default arguments are created once when the function is defined. Mutating a default list modifies the persistent object across invocations."
        rec_action = "Use `def fn(val, my_list=None): if my_list is None: my_list = []` pattern."
    elif "slice" in c_lower or "index" in c_lower or "[-" in snippet_lower:
        detected_misconception = "Off-by-one error with negative slicing or inclusive vs exclusive interval boundaries."
        misconception_cat = "Index Boundaries and Strides"
        explanation = "Python slice `[start:stop:step]` includes `start` up to but not including `stop`. Negative indices count backward from len(list)."
        rec_action = "Practice array index-to-element mapping using 0-based and negative indices."

    # C / C++ / Pointers
    elif "pointer" in c_lower or "memory" in c_lower or "*" in snippet_lower:
        detected_misconception = "Confusing pointer dereferencing *(ptr + offset) with base address modification, or pointer arithmetic scale."
        misconception_cat = "Pointer Arithmetic & Memory Dereferencing"
        explanation = "*(ptr + 2) accesses the element at offset 2 without changing where `ptr` points. Pointer arithmetic scales by sizeof(type)."
        rec_action = "Draw memory block diagrams showing stack vs heap addresses and pointer values."
    elif "virtual" in c_lower or "polymorphism" in c_lower:
        detected_misconception = "Assuming compile-time binding resolves polymorphic destructors without `virtual` keyword."
        misconception_cat = "Dynamic Dispatch & VTable Binding"
        explanation = "Deleting an object of derived type via a base class pointer without a virtual destructor causes undefined behavior and resource leaks."
        rec_action = "Review C++ vtable mechanics and the RAII idiom."

    # Java / JavaScript
    elif "string" in c_lower or "pool" in c_lower or "==" in snippet_lower:
        detected_misconception = "Confusing object reference equality (==) with content/value equality (.equals())."
        misconception_cat = "Reference Identity vs Value Equality"
        explanation = "In Java, `==` checks whether both references point to the exact same heap address, while `.equals()` compares character values."
        rec_action = "Always use `.equals()` for value comparisons of objects."
    elif "closure" in c_lower or "scope" in c_lower or "var" in snippet_lower:
        detected_misconception = "Assuming `var` has block scope or creates a fresh binding per loop iteration."
        misconception_cat = "Lexical Scope and Variable Hoisting"
        explanation = "`var` is function-scoped. In a for loop, asynchronous callbacks share the single mutated `i` variable unless `let` is used."
        rec_action = "Use modern ES6 `let` and `const` for block scoping."

    # React / Frontend
    elif "react" in s_lower or "state" in c_lower or "hook" in c_lower or "useeffect" in c_lower:
        detected_misconception = "Mutating state in-place instead of treating React state as immutable."
        misconception_cat = "React State Immutability"
        explanation = "React compares old and new state using `Object.is` reference equality. In-place mutations preserve the same object reference, preventing re-render."
        rec_action = "Use immutable updates like `setItems([...items, newItem])`."
    elif "box" in c_lower or "css" in s_lower:
        detected_misconception = "Misunderstanding how padding and border alter total width under content-box vs border-box."
        misconception_cat = "CSS Box Model Dimensions"
        explanation = "`box-sizing: border-box` includes padding and border within the declared width, whereas `content-box` adds them on top."
        rec_action = "Set `* { box-sizing: border-box; }` and inspect layout dimensions in browser DevTools."

    # Backend / DB
    elif "rest" in s_lower or "idempotent" in c_lower or "http" in c_lower:
        detected_misconception = "Believing POST is idempotent or confusing safe methods (GET) with idempotent methods (PUT)."
        misconception_cat = "HTTP Protocol Semantics"
        explanation = "An idempotent method produces the same server state regardless of how many times it is repeated. PUT and DELETE are idempotent; POST is not."
        rec_action = "Review RFC 7231 specifications for HTTP methods."
    elif "jwt" in c_lower or "auth" in s_lower:
        detected_misconception = "Confusing digital signature integrity with payload confidentiality/encryption."
        misconception_cat = "JWT Signature vs Encryption"
        explanation = "Standard JWTs are signed (JWS) to prevent tampering, but the payload is plain base64url-encoded and publicly readable."
        rec_action = "Never put passwords or sensitive tokens inside standard JWT claims."
    elif "join" in c_lower or "sql" in s_lower or "acid" in c_lower:
        detected_misconception = "Using INNER JOIN when unmatched records must be retained, or confusing ACID isolation with atomicity."
        misconception_cat = "Relational Set Operations & Transaction Concurrency"
        explanation = "LEFT JOIN retains all rows from the left table regardless of matches in the right table. Isolation protects transactions from concurrency anomalies."
        rec_action = "Practice Venn diagram representations of SQL set joins."

    # AI / ML
    elif "overfitting" in c_lower or "machine learning" in s_lower or "regularization" in c_lower:
        detected_misconception = "Believing higher model complexity or training epochs solves generalization failure."
        misconception_cat = "Bias-Variance Tradeoff"
        explanation = "High training accuracy paired with poor test accuracy indicates overfitting. L1/L2 penalties, dropout, and early stopping constrain model complexity."
        rec_action = "Apply validation curves and cross-validation to tune regularization parameters."
    elif "rag" in c_lower or "genai" in s_lower or "embedding" in c_lower:
        detected_misconception = "Confusing high-dimensional vector embeddings with lexical keyword search."
        misconception_cat = "Semantic Vector Space vs Keyword Matching"
        explanation = "Embeddings map semantic intent into dense geometric vector space, enabling cosine similarity retrieval even without shared vocabulary."
        rec_action = "Experiment with cosine distance between synonym embeddings."

    reasoning_analysis = (
        f"Student stated: '{reasoning}'. This reflects: {detected_misconception}"
        if reasoning and len(reasoning.strip()) > 3
        else "No technical reasoning was provided to justify the selected option."
    )

    return {
        "is_correct": False,
        "detected_misconception": detected_misconception,
        "misconception_category": misconception_cat,
        "reasoning_analysis": reasoning_analysis,
        "concept_understanding": "poor" if reasoning else "partial",
        "explanation": explanation,
        "recommended_learning_action": rec_action,
        "suggested_difficulty": "easier" if difficulty != "easy" else "same",
        "is_ai_generated": False,
    }


def analyze_answer(
    question: str,
    correct_answer: str,
    student_answer: str,
    reasoning: Optional[str],
    concept_name: str,
    subject_name: str = "Computer Science",
    code_snippet: Optional[str] = None,
    difficulty: str = "medium",
) -> dict:
    """
    Analyze student's programming answer and reasoning using Gemini AI,
    with robust rule-based fallback.
    """
    is_correct = student_answer.upper().strip() == correct_answer.upper().strip()
    client = get_gemini_client()

    if not client.available:
        return _rule_based_fallback(
            is_correct=is_correct,
            difficulty=difficulty,
            question=question,
            code_snippet=code_snippet,
            student_answer=student_answer,
            reasoning=reasoning,
            concept_name=concept_name,
            subject_name=subject_name,
        )

    prompt = _PROMPT_TEMPLATE.format(
        subject_name=subject_name,
        concept_name=concept_name,
        question=question,
        code_snippet=code_snippet or "None",
        correct_answer=correct_answer,
        student_answer=student_answer,
        reasoning=reasoning or "No reasoning provided",
    )

    try:
        raw = client.generate_content(prompt)
        parsed = _extract_json(raw)

        missing = _REQUIRED_KEYS - set(parsed.keys())
        if missing:
            logger.warning("Gemini AI response missing keys: %s — falling back", missing)
            return _rule_based_fallback(
                is_correct=is_correct,
                difficulty=difficulty,
                question=question,
                code_snippet=code_snippet,
                student_answer=student_answer,
                reasoning=reasoning,
                concept_name=concept_name,
                subject_name=subject_name,
            )

        parsed["is_correct"] = bool(parsed.get("is_correct", is_correct))
        parsed["concept_understanding"] = parsed.get("concept_understanding", "partial").lower()
        if parsed["concept_understanding"] not in ("good", "partial", "poor"):
            parsed["concept_understanding"] = "partial"
        parsed["suggested_difficulty"] = parsed.get("suggested_difficulty", "same").lower()
        if parsed["suggested_difficulty"] not in ("easier", "same", "harder"):
            parsed["suggested_difficulty"] = "same"
        parsed["is_ai_generated"] = True
        return parsed

    except Exception as exc:
        logger.warning("Gemini misconception detection failed: %s — using rule-based fallback", exc)
        return _rule_based_fallback(
            is_correct=is_correct,
            difficulty=difficulty,
            question=question,
            code_snippet=code_snippet,
            student_answer=student_answer,
            reasoning=reasoning,
            concept_name=concept_name,
            subject_name=subject_name,
        )
