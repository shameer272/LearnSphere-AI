"""
Adaptive B.Tech Computer Science Question Generator for LearnSphere AI.
Uses Gemini AI with fallback to the curated B.Tech CSE question bank.
"""
import json
import logging
import re
from typing import Optional

from app.ai.gemini_client import get_gemini_client
from app.ai.fallback_questions import get_random_fallback_question

logger = logging.getLogger(__name__)

_PROMPT_TEMPLATE = """You are a senior Computer Science professor creating an adaptive assessment question for B.Tech CSE students.

Subject: {subject_name}
Concept: {concept_name}
Target Difficulty: {difficulty} (easy/medium/hard)
Question Type preference: {question_type} (mcq, output_prediction, code_debugging, conceptual, sql_query, scenario)
Avoid repeating these recently asked question texts: {recent_texts}

Requirements:
1. Make the question test deep conceptual understanding and engineering problem solving, not trivia.
2. If relevant for this concept, provide a clean, realistic code snippet (e.g. Python, C++, Java, JS, SQL).
3. Provide 4 distinct options (A, B, C, D) with realistic distractors targeting common programming misconceptions.
4. Exactly one option must be correct.

Return ONLY a valid JSON object matching this schema:
{{
  "question": "clear problem statement or question text",
  "code_snippet": "formatted code snippet or null if purely conceptual",
  "question_type": "output_prediction|code_debugging|conceptual|sql_query|scenario|mcq",
  "options": {{
    "A": "option text",
    "B": "option text",
    "C": "option text",
    "D": "option text"
  }},
  "correct_answer": "A",
  "explanation": "clear, rigorous technical explanation of the correct option",
  "difficulty": "easy/medium/hard",
  "misconception_targets": ["misconception 1 targeted by distractors", "misconception 2"]
}}
"""

_REQUIRED_KEYS = {"question", "options", "correct_answer", "explanation", "difficulty"}
_OPTION_KEYS = {"A", "B", "C", "D"}


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"```\s*$", "", raw)
    return json.loads(raw.strip())


def _validate_question(data: dict) -> bool:
    if not _REQUIRED_KEYS.issubset(set(data.keys())):
        return False
    if not isinstance(data.get("options"), dict):
        return False
    if not _OPTION_KEYS.issubset(set(data["options"].keys())):
        return False
    if data.get("correct_answer", "").upper() not in _OPTION_KEYS:
        return False
    return True


def generate_question(
    subject_id: int,
    concept_id: int,
    subject_name: str,
    concept_name: str,
    subject_code: Optional[str] = None,
    difficulty: str = "medium",
    recent_question_texts: Optional[list[str]] = None,
) -> dict:
    """
    Generate an adaptive question for the given B.Tech CSE concept.
    Tries Gemini AI first; falls back to curated static bank.
    """
    recent_texts = recent_question_texts or []
    client = get_gemini_client()

    if client.available:
        prompt = _PROMPT_TEMPLATE.format(
            subject_name=subject_name,
            concept_name=concept_name,
            difficulty=difficulty,
            question_type="output_prediction or conceptual",
            recent_texts=" | ".join(recent_texts[:5]) if recent_texts else "None",
        )
        try:
            raw = client.generate_content(prompt)
            data = _extract_json(raw)
            clean_q = data.get("question", "").strip()
            recent_set = {t.strip() for t in recent_texts}
            if _validate_question(data) and clean_q and clean_q not in recent_set:
                return {
                    "subject_id": subject_id,
                    "concept_id": concept_id,
                    "subject_name": subject_name,
                    "concept_name": concept_name,
                    "question_type": data.get("question_type", "mcq"),
                    "question_text": data["question"],
                    "code_snippet": data.get("code_snippet"),
                    "options": {k: str(v) for k, v in data["options"].items()},
                    "correct_answer": data["correct_answer"].upper(),
                    "explanation": data["explanation"],
                    "difficulty": data.get("difficulty", difficulty).lower(),
                    "misconception_targets": data.get("misconception_targets", []),
                    "is_ai_generated": True,
                }
            logger.warning("Gemini generated question failed validation: %s", data)
        except Exception as exc:
            logger.warning("Gemini question generation error: %s — falling back", exc)

    # Curated fallback
    fallback = get_random_fallback_question(
        subject_code=subject_code,
        concept_name=concept_name,
        difficulty=difficulty,
        exclude_texts=recent_texts,
    )

    return {
        "subject_id": subject_id,
        "concept_id": concept_id,
        "subject_name": subject_name,
        "concept_name": concept_name,
        "question_type": fallback.get("question_type", "mcq"),
        "question_text": fallback["question_text"],
        "code_snippet": fallback.get("code_snippet"),
        "options": fallback["options"],
        "correct_answer": fallback["correct_answer"],
        "explanation": fallback.get("explanation"),
        "difficulty": fallback.get("difficulty", difficulty),
        "misconception_targets": fallback.get("misconception_targets", []),
        "is_ai_generated": False,
    }
