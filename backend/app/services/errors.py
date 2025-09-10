"""
Custom exceptions for the Multi-Agent AI Chat System services.
"""

class LLMServiceError(Exception):
    """Custom exception for errors occurring in LLM service interactions."""
    def __init__(self, message: str, original_exception: Exception = None):
        super().__init__(message)
        self.original_exception = original_exception
