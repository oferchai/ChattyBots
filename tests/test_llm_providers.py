"""
Unit tests for LLM Providers (OllamaProvider, OpenRouterProvider).
"""
import pytest
from unittest.mock import AsyncMock, patch
import httpx

from app.services.providers.ollama_provider import OllamaProvider
from app.services.providers.openrouter_provider import OpenRouterProvider

@pytest.fixture
def mock_httpx_client():
    """Fixture to mock httpx.AsyncClient."""
    with patch('httpx.AsyncClient') as mock_client_class:
        mock_client_instance = AsyncMock()
        mock_client_class.return_value = mock_client_instance
        mock_client_instance.__aenter__.return_value = mock_client_instance
        mock_client_instance.__aexit__.return_value = False
        yield mock_client_instance

@pytest.mark.asyncio
async def test_ollama_provider_generate_response(mock_httpx_client):
    """Test OllamaProvider's generate_response method."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"response": "Ollama test response"}
    mock_response.raise_for_status.return_value = None
    mock_httpx_client.post.return_value = mock_response

    config = {"base_url": "http://localhost:11434", "model": "llama2"}
    provider = OllamaProvider(config)
    response = await provider.generate_response("Test prompt for Ollama")

    assert response == "Ollama test response"
    mock_httpx_client.post.assert_called_once_with(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": "Test prompt for Ollama",
            "stream": False,
        },
        timeout=60.0,
    )

@pytest.mark.asyncio
async def test_ollama_provider_generate_response_error(mock_httpx_client):
    """Test OllamaProvider's generate_response method with an error."""
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Bad Request", request=httpx.Request("POST", "url"), response=httpx.Response(400)
    )
    mock_httpx_client.post.return_value = mock_response

    config = {"base_url": "http://localhost:11434", "model": "llama2"}
    provider = OllamaProvider(config)

    with pytest.raises(httpx.HTTPStatusError):
        await provider.generate_response("Test prompt for Ollama")

@pytest.mark.asyncio
async def test_openrouter_provider_generate_response(mock_httpx_client):
    """Test OpenRouterProvider's generate_response method."""
    mock_response = AsyncMock()
    mock_response.json.return_value = {"choices": [{"message": {"content": "OpenRouter test response"}}]}
    mock_response.raise_for_status.return_value = None
    mock_httpx_client.post.return_value = mock_response

    config = {"api_key": "test_key", "model": "openai/gpt-3.5-turbo"}
    provider = OpenRouterProvider(config)
    response = await provider.generate_response("Test prompt for OpenRouter")

    assert response == "OpenRouter test response"
    mock_httpx_client.post.assert_called_once_with(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": "Bearer test_key",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": "Test prompt for OpenRouter"}],
        },
        timeout=60.0,
    )

@pytest.mark.asyncio
async def test_openrouter_provider_generate_response_error(mock_httpx_client):
    """Test OpenRouterProvider's generate_response method with an error."""
    mock_response = AsyncMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        message="Unauthorized", request=httpx.Request("POST", "url"), response=httpx.Response(401)
    )
    mock_httpx_client.post.return_value = mock_response

    config = {"api_key": "test_key", "model": "openai/gpt-3.5-turbo"}
    provider = OpenRouterProvider(config)

    with pytest.raises(httpx.HTTPStatusError):
        await provider.generate_response("Test prompt for OpenRouter")

def test_openrouter_provider_no_api_key():
    """Test that OpenRouterProvider raises ValueError if no API key is provided."""
    with pytest.raises(ValueError, match="OpenRouter API key is not provided in the configuration."):
        OpenRouterProvider({"model": "openai/gpt-3.5-turbo"})