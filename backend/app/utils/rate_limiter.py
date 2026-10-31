"""
Production Rate Limiting Middleware for LearnSphere AI.
Implements in-memory sliding window rate limiting per client IP.
Zero external dependencies, O(1) memory cleanup, thread-safe.
"""
import os
import time
from collections import defaultdict
from threading import Lock
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.enabled = os.getenv("RATE_LIMIT_ENABLED", "true").lower() in ("true", "1", "yes")
        self.general_limit = int(os.getenv("RATE_LIMIT_PER_MINUTE", "180"))
        self.auth_limit = int(os.getenv("AUTH_RATE_LIMIT_PER_MINUTE", "45"))
        self.window_seconds = 60
        self.requests = defaultdict(list)
        self.lock = Lock()
        self.last_cleanup = time.time()

    def _cleanup_old_entries(self, now: float):
        """Purge records older than window to prevent unbounded memory growth."""
        if now - self.last_cleanup > 120:
            threshold = now - self.window_seconds
            for ip in list(self.requests.keys()):
                self.requests[ip] = [ts for ts in self.requests[ip] if ts > threshold]
                if not self.requests[ip]:
                    del self.requests[ip]
            self.last_cleanup = now

    async def dispatch(self, request, call_next):
        if not self.enabled:
            return await call_next(request)

        # Allow CORS preflight requests without rate limiting
        if request.method == "OPTIONS":
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        path = request.url.path

        # Determine limit according to endpoint sensitivity
        is_auth = path.startswith("/api/auth/")
        limit = self.auth_limit if is_auth else self.general_limit

        now = time.time()
        threshold = now - self.window_seconds

        with self.lock:
            self._cleanup_old_entries(now)
            timestamps = self.requests[client_ip]
            # Retain only timestamps within the current sliding window
            valid_timestamps = [ts for ts in timestamps if ts > threshold]
            self.requests[client_ip] = valid_timestamps

            if len(valid_timestamps) >= limit:
                return JSONResponse(
                    status_code=429,
                    content={
                        "detail": "Rate limit exceeded. Too many requests. Please wait a moment before retrying."
                    },
                    headers={
                        "Retry-After": "60",
                        "X-RateLimit-Limit": str(limit),
                        "X-RateLimit-Remaining": "0",
                    },
                )

            valid_timestamps.append(now)
            remaining = max(0, limit - len(valid_timestamps))

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response
