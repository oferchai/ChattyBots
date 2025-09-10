"""
OpenRouter LLM Provider for the Multi-Agent AI Chat System.
"""
import httpx

from app.services.base_llm_service import LLMService
from app.services.errors import LLMServiceError

class OpenRouterProvider(LLMService):
    """OpenRouter LLM service implementation."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.api_key = config.get("api_key")
        self.model = config.get("model", "openai/gpt-3.5-turbo")
        self.base_url = "https://openrouter.ai/api/v1"

        if not self.api_key:
            raise ValueError("OpenRouter API key is not provided in the configuration.")

    async def generate_response(self, prompt: str) -> str:
        """Generates a response from the OpenRouter LLM."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            data = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
            }

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60.0,
                )
                await response.raise_for_status()
                return (await response.json())["choices"][0]["message"]["content"]
        except httpx.RequestError as e:
            raise LLMServiceError(f"Network or request error communicating with OpenRouter: {e}", original_exception=e)
        except httpx.HTTPStatusError as e:
            raise LLMServiceError(f"OpenRouter API returned an error: {e.response.status_code} - {e.response.text}", original_exception=e)
        except Exception as e:
            raise LLMServiceError(f"An unexpected error occurred during OpenRouter response generation: {e}", original_exception=e)