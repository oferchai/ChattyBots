"""
LLM Service Factory for the Multi-Agent AI Chat System.

This module provides a factory for creating LLM service instances.
"""
from typing import Dict, Type

from app.services.base_llm_service import LLMService
from app.services.prompt_manager import PromptManager
from app.services.response_validator import ResponseValidator
from app.services.providers.ollama_provider import OllamaProvider
from app.services.providers.openrouter_provider import OpenRouterProvider

class LLMServiceFactory:
    """Factory for creating LLMService instances based on configuration."""

    _providers: Dict[str, Type[LLMService]] = {
        "ollama": OllamaProvider,
        "openrouter": OpenRouterProvider,
    }

    @classmethod
    def create_llm_service(cls, provider_name: str, config: dict) -> LLMService:
        """Creates an LLMService instance for the specified provider."""
        provider_class = cls._providers.get(provider_name)
        if not provider_class:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        return provider_class(config)

    def __init__(self, config: dict, prompt_manager: PromptManager = None, response_validator: ResponseValidator = None):
        self.config = config
        self.provider = self.create_llm_service(
            provider_name=config.get("provider", "ollama"),
            config=config.get(config.get("provider", "ollama"), {})
        )
        self.prompt_manager = prompt_manager or PromptManager()
        self.response_validator = response_validator or ResponseValidator()

    async def generate_response(self, prompt: str) -> str:
        """Generates a response using the configured LLM provider."""
        response = await self.provider.generate_response(prompt)
        if not self.response_validator.validate_response(response):
            raise ValueError("LLM response failed validation.")
        return self.response_validator.clean_response(response)

    def get_prompt_manager(self) -> PromptManager:
        """Returns the prompt manager instance."""
        return self.prompt_manager
