"""
Ollama LLM Provider for the Multi-Agent AI Chat System.
"""
import httpx

from app.services.base_llm_service import LLMService
from app.services.errors import LLMServiceError

class OllamaProvider(LLMService):
    """Ollama LLM service implementation."""

    def __init__(self, config: dict):
        super().__init__(config)
        self.base_url = config.get("base_url", "http://localhost:11434")
        self.model = config.get("model", "llama2")

    async def generate_response(self, prompt: str) -> str:
        """Generates a response from the Ollama LLM."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                    },
                    timeout=60.0,
                )
                await response.raise_for_status()
                return (await response.json())["response"]
        except httpx.RequestError as e:
            raise LLMServiceError(f"Network or request error communicating with Ollama: {e}", original_exception=e)
        except httpx.HTTPStatusError as e:
            raise LLMServiceError(f"Ollama API returned an error: {e.response.status_code} - {e.response.text}", original_exception=e)
        except Exception as e:
            raise LLMServiceError(f"An unexpected error occurred during Ollama response generation: {e}", original_exception=e)