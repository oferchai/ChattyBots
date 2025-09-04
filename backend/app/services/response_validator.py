"""
Response Validator for the Multi-Agent AI Chat System.

This module handles validation and cleanup of LLM responses.
"""

class ResponseValidator:
    """Validates and cleans up LLM responses."""

    def validate_response(self, response: str) -> bool:
        """Performs basic validation on the LLM response."""
        return bool(response and len(response.strip()) > 0)

    def clean_response(self, response: str) -> str:
        """Cleans up the LLM response (e.g., removes leading/trailing whitespace)."""
        return response.strip()
