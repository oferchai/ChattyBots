"""
Unit tests for the LLMServiceFactory.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.llm_service import LLMServiceFactory, LLMService
from app.services.prompt_manager import PromptManager
from app.services.response_validator import ResponseValidator
from app.services.providers.ollama_provider import OllamaProvider
from app.services.providers.openrouter_provider import OpenRouterProvider

@pytest.fixture
def mock_ollama_provider():
    mock = MagicMock(spec=OllamaProvider)
    mock.generate_response = AsyncMock(return_value="Ollama response")
    return mock

@pytest.fixture
def mock_openrouter_provider():
    mock = MagicMock(spec=OpenRouterProvider)
    mock.generate_response = AsyncMock(return_value="OpenRouter response")
    return mock

@pytest.fixture
def mock_response_validator():
    mock = MagicMock(spec=ResponseValidator)
    mock.validate_response.return_value = True
    mock.clean_response.side_effect = lambda x: x # Return as is for cleaning
    return mock

@pytest.fixture
def mock_prompt_manager():
    mock = MagicMock(spec=PromptManager)
    return mock

@pytest.fixture(autouse=True)
def mock_response_validator_and_prompt_manager(mock_response_validator, mock_prompt_manager):
    with patch('app.services.response_validator.ResponseValidator', return_value=mock_response_validator), \
         patch('app.services.prompt_manager.PromptManager', return_value=mock_prompt_manager):
        yield

@pytest.fixture(autouse=True)
def mock_llm_providers(mock_ollama_provider, mock_openrouter_provider):
    """Mock the actual provider classes in the factory."""
    with patch.object(LLMServiceFactory, 'create_llm_service') as mock_create_llm_service:
        def side_effect(provider_name, config):
            if provider_name == "ollama":
                return mock_ollama_provider
            elif provider_name == "openrouter":
                return mock_openrouter_provider
            else:
                raise ValueError("Unknown LLM provider: unknown")
        mock_create_llm_service.side_effect = side_effect
        yield


def test_create_llm_service_ollama(mock_ollama_provider, mock_response_validator, mock_prompt_manager):
    """Test that LLMServiceFactory creates OllamaProvider correctly."""
    config = {"provider": "ollama", "ollama": {"model": "llama2"}}
    factory = LLMServiceFactory(config, prompt_manager=mock_prompt_manager, response_validator=mock_response_validator)
    
    assert isinstance(factory.provider, MagicMock) # It's a mock of OllamaProvider
    assert factory.provider == mock_ollama_provider
    assert isinstance(factory.prompt_manager, PromptManager)
    assert isinstance(factory.response_validator, ResponseValidator)

def test_create_llm_service_openrouter(mock_openrouter_provider, mock_response_validator, mock_prompt_manager):
    """Test that LLMServiceFactory creates OpenRouterProvider correctly."""
    config = {"provider": "openrouter", "openrouter": {"api_key": "test_key"}}
    factory = LLMServiceFactory(config, prompt_manager=mock_prompt_manager, response_validator=mock_response_validator)
    
    assert isinstance(factory.provider, MagicMock) # It's a mock of OpenRouterProvider
    assert factory.provider == mock_openrouter_provider
    assert isinstance(factory.prompt_manager, PromptManager)
    assert isinstance(factory.response_validator, ResponseValidator)

def test_create_llm_service_unknown_provider():
    """Test that LLMServiceFactory raises ValueError for unknown provider."""
    config = {"provider": "unknown"}
    with pytest.raises(ValueError, match="Unknown LLM provider: unknown"):
        LLMServiceFactory(config)

@pytest.mark.asyncio
async def test_llm_service_factory_generate_response_ollama(mock_ollama_provider, mock_response_validator):
    """Test generate_response through LLMServiceFactory with Ollama."""
    config = {"provider": "ollama", "ollama": {"model": "llama2"}}
    factory = LLMServiceFactory(config, prompt_manager=mock_prompt_manager, response_validator=mock_response_validator)
    
    response = await factory.generate_response("Test prompt")
    
    mock_ollama_provider.generate_response.assert_called_once_with("Test prompt")
    mock_response_validator.validate_response.assert_called_once_with("Ollama response")
    mock_response_validator.clean_response.assert_called_once_with("Ollama response")
    assert response == "Ollama response"

@pytest.mark.asyncio
async def test_llm_service_factory_generate_response_openrouter(mock_openrouter_provider, mock_response_validator):
    """Test generate_response through LLMServiceFactory with OpenRouter."""
    config = {"provider": "openrouter", "openrouter": {"api_key": "test_key"}}
    factory = LLMServiceFactory(config, prompt_manager=mock_prompt_manager, response_validator=mock_response_validator)
    
    response = await factory.generate_response("Test prompt")
    
    mock_openrouter_provider.generate_response.assert_called_once_with("Test prompt")
    mock_response_validator.validate_response.assert_called_once_with("OpenRouter response")
    mock_response_validator.clean_response.assert_called_once_with("OpenRouter response")
    assert response == "OpenRouter response"

@pytest.mark.asyncio
async def test_llm_service_factory_validation_failure(mock_ollama_provider, mock_response_validator):
    """Test LLMServiceFactory handles response validation failure."""
    mock_response_validator.validate_response.return_value = False
    config = {"provider": "ollama", "ollama": {"model": "llama2"}}
    factory = LLMServiceFactory(config, prompt_manager=mock_prompt_manager, response_validator=mock_response_validator)
    
    with pytest.raises(ValueError, match="LLM response failed validation."):
        await factory.generate_response("Test prompt")
    
    mock_ollama_provider.generate_response.assert_called_once_with("Test prompt")
    mock_response_validator.validate_response.assert_called_once_with("Ollama response")
    mock_response_validator.clean_response.assert_not_called()
