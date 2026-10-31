"""
Gemini API client wrapper.
"""
import logging
import os

logger = logging.getLogger(__name__)


class GeminiClient:
    """Thin wrapper around google-generativeai SDK."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.available = False

        if api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
                self.model = genai.GenerativeModel(model_name)
                self.available = True
                logger.info("Gemini client initialized successfully with model: %s", model_name)
            except Exception as exc:
                logger.warning("Failed to initialise Gemini client: %s", exc)
        else:
            logger.info("GEMINI_API_KEY not set — AI features will use fallback mode.")

    def generate_content(self, prompt: str) -> str:
        """
        Send a prompt to Gemini and return the response text.
        Raises RuntimeError if the client is not available or generation fails.
        """
        if not self.available:
            raise RuntimeError("Gemini client is not available (API key missing or invalid).")

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as exc:
            # Fallback to gemini-1.5-flash if primary model encounters error
            try:
                import google.generativeai as genai
                alt_model = genai.GenerativeModel("gemini-1.5-flash")
                response = alt_model.generate_content(prompt)
                return response.text
            except Exception:
                pass
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc


# Module-level singleton
_client: GeminiClient | None = None


def get_gemini_client() -> GeminiClient:
    global _client
    if _client is None:
        _client = GeminiClient()
    return _client
