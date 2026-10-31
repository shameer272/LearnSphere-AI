"""
Mastery score calculation service for LearnSphere AI.
All algorithms are deterministic and bounded.
Subject-independent and adapted for B.Tech CSE learning.
"""


def update_mastery(
    current_mastery: float,
    is_correct: bool,
    difficulty: str,
    concept_understanding: str,
    attempts: int = 1,
) -> float:
    """
    Transparent bounded mastery update algorithm.

    Base deltas by difficulty:
      easy / beginner:       correct +5,  incorrect -3
      medium / intermediate: correct +8,  incorrect -5
      hard / advanced:       correct +12, incorrect -7

    Multipliers by concept_understanding:
      good:    1.2
      partial: 0.8
      poor:    0.5 (correct) / 1.3 (incorrect)

    Capped: max increase +15, max decrease -10
    Final score clamped to [0, 100].
    """
    diff_normalized = (difficulty or "medium").lower()
    if diff_normalized in ("beginner", "easy"):
        correct_delta, incorrect_delta = 5, -3
    elif diff_normalized in ("advanced", "hard"):
        correct_delta, incorrect_delta = 12, -7
    else:
        correct_delta, incorrect_delta = 8, -5

    understanding_normalized = (concept_understanding or "partial").lower()
    if understanding_normalized == "good":
        multiplier = 1.2
    elif understanding_normalized == "poor":
        multiplier = 0.5 if is_correct else 1.3
    else:
        multiplier = 0.8

    if is_correct:
        raw_delta = correct_delta * multiplier
        delta = min(raw_delta, 15.0)   # cap increase
    else:
        raw_delta = incorrect_delta * multiplier
        delta = max(raw_delta, -10.0)  # cap decrease (negative)

    new_mastery = current_mastery + delta
    return round(max(0.0, min(100.0, new_mastery)), 2)


def get_mastery_level(score: float) -> str:
    """Return human-readable mastery tier."""
    if score < 40:
        return "weak"
    elif score <= 70:
        return "developing"
    else:
        return "mastered"


def calculate_next_difficulty(
    mastery_score: float,
    recent_correct: int,
    recent_incorrect: int,
) -> str:
    """
    Dynamic difficulty adjustment based on mastery and recent performance.
    """
    total_recent = recent_correct + recent_incorrect
    recent_accuracy = (recent_correct / total_recent) if total_recent > 0 else 0.5

    if mastery_score < 35:
        return "easy"
    elif mastery_score < 65:
        if recent_accuracy >= 0.7:
            return "medium"
        return "easy"
    elif mastery_score < 80:
        if recent_accuracy >= 0.75:
            return "hard"
        elif recent_accuracy < 0.4:
            return "easy"
        return "medium"
    else:
        if recent_accuracy < 0.5:
            return "medium"
        return "hard"
