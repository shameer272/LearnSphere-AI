"""
Utility helpers for LearnSphere AI.
"""
from datetime import datetime, timedelta
from typing import Any


def paginate(query_result: list, page: int = 1, page_size: int = 20) -> dict[str, Any]:
    """Simple in-memory pagination helper."""
    total = len(query_result)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "items": query_result[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


def days_ago(n: int) -> datetime:
    """Return a datetime n days in the past (UTC)."""
    return datetime.utcnow() - timedelta(days=n)


def safe_average(values: list[float]) -> float:
    """Return the average of a list; return 0.0 if the list is empty."""
    if not values:
        return 0.0
    return round(sum(values) / len(values), 2)
