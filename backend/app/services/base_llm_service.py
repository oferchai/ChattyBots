"""
Abstract base class for all LLM services.
"""
from abc import ABC, abstractmethod

class LLMService(ABC):
    """Abstract base class for all LLM services."""

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """Generates a response from the LLM."""
        pass
