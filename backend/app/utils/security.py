"""
Security and authentication utilities for LearnSphere AI.
Implements PBKDF2-HMAC-SHA256 password hashing and RFC 7519 compliant HS256 JWT tokens.
"""
import base64
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.database.db import get_db

# Secret key from environment or fallback secure default
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "learnsphere-btech-cse-jwt-secret-key-2026-secure")
TOKEN_EXPIRE_HOURS = int(os.getenv("TOKEN_EXPIRE_HOURS", "72"))

security_scheme = HTTPBearer(auto_error=False)


def _b64url_encode(data: bytes) -> str:
    """Base64 URL-safe encode without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def _b64url_decode(data: str) -> bytes:
    """Base64 URL-safe decode with padding restoration."""
    padding = 4 - (len(data) % 4)
    if padding and padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def hash_password(password: str) -> str:
    """
    Hash a password using PBKDF2-HMAC-SHA256 with 100,000 iterations and 16-byte salt.
    """
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    salt_b64 = base64.b64encode(salt).decode("ascii")
    dk_b64 = base64.b64encode(dk).decode("ascii")
    return f"pbkdf2:sha256:100000${salt_b64}${dk_b64}"


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a stored PBKDF2 hash.
    """
    try:
        parts = hashed_password.split("$")
        if len(parts) != 3:
            return False
        _, salt_b64, hash_b64 = parts
        salt = base64.b64decode(salt_b64.encode("ascii"))
        expected_dk = base64.b64decode(hash_b64.encode("ascii"))
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return hmac.compare_digest(dk, expected_dk)
    except Exception:
        return False


def create_access_token(payload: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate an HS256 JWT token with an expiration timestamp.
    """
    header = {"alg": "HS256", "typ": "JWT"}
    header_b64 = _b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))

    to_encode = payload.copy()
    now = int(time.time())
    if expires_delta:
        exp = now + int(expires_delta.total_seconds())
    else:
        exp = now + (TOKEN_EXPIRE_HOURS * 3600)

    to_encode["iat"] = now
    to_encode["exp"] = exp

    payload_b64 = _b64url_encode(json.dumps(to_encode, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    signature = hmac.new(AUTH_SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = _b64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{sig_b64}"


def decode_access_token(token: str) -> Optional[dict]:
    """
    Validate and decode an HS256 JWT token. Returns payload dict or None.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts

        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        expected_sig = hmac.new(AUTH_SECRET_KEY.encode("utf-8"), signing_input, hashlib.sha256).digest()
        actual_sig = _b64url_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            return None

        payload_bytes = _b64url_decode(payload_b64)
        payload = json.loads(payload_bytes.decode("utf-8"))

        # Verify expiration
        if "exp" in payload and int(time.time()) > payload["exp"]:
            return None

        return payload
    except Exception:
        return None


def get_current_student(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db),
):
    """
    FastAPI dependency that extracts and validates the Bearer token,
    returning the authenticated Student instance.
    """
    if not auth or not auth.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required. Please log in.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = decode_access_token(auth.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    student_id = int(payload["sub"])
    from app.models.models import Student

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student account not found.",
        )

    return student


def get_current_teacher(
    current_student = Depends(get_current_student),
):
    """
    Enforces RBAC: Strictly verifies that the authenticated user possesses the
    'teacher' or 'admin' role in the verified database record.
    Never trusts client-supplied headers or roles. Returns 403 Forbidden otherwise.
    """
    role = getattr(current_student, "role", "student")
    if role not in ("teacher", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: Teacher or faculty role authorization required.",
        )
    return current_student


def get_optional_student(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
    db: Session = Depends(get_db),
):
    """
    Optional student extraction dependency. Does not raise 401 if missing.
    """
    if not auth or not auth.credentials:
        return None
    payload = decode_access_token(auth.credentials)
    if not payload or "sub" not in payload:
        return None
    try:
        student_id = int(payload["sub"])
        from app.models.models import Student

        return db.query(Student).filter(Student.id == student_id).first()
    except Exception:
        return None
