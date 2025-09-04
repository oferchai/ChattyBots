"""
Unit tests for the Configuration Management System.
"""
import os
import pytest
from pathlib import Path

from backend.config import (
    get_settings, create_settings, get_environment, 
    Environment, Settings, reload_settings, LogLevel
)

@pytest.fixture(autouse=True)
def reset_settings_for_tests():
    """Fixture to ensure settings are reloaded for each test."""
    reload_settings()
    yield
    reload_settings() # Reset after test

def test_environment_detection(monkeypatch):
    """Test automatic environment detection."""
    # Test default detection
    if 'ENVIRONMENT' in os.environ:
        del os.environ['ENVIRONMENT']
    current_env = get_environment()
    assert current_env == Environment.DEVELOPMENT
    
    # Test environment override
    monkeypatch.setenv('ENVIRONMENT', 'testing')
    test_env = get_environment()
    assert test_env == Environment.TESTING
    
    # Reset environment
    monkeypatch.delenv('ENVIRONMENT')

def test_configuration_validation(monkeypatch):
    """Test configuration validation logic."""
    # Test development settings
    monkeypatch.setenv('ENVIRONMENT', 'development')
    monkeypatch.setenv('APP_NAME', 'Multi-Agent AI Chat System')
    monkeypatch.setenv('DEBUG', 'true')
    monkeypatch.setenv('DATABASE__URL', 'sqlite:///./data/chatbot.db')
    monkeypatch.setenv('LLM__PROVIDER', 'ollama')
    reload_settings()
    dev_settings = create_settings(Environment.DEVELOPMENT)
    assert dev_settings.app_name == "Multi-Agent AI Chat System"
    assert dev_settings.debug is True
    assert dev_settings.database.url == "sqlite:///./data/chatbot.db"
    assert dev_settings.llm.provider == "ollama"
    
    # Test testing settings
    monkeypatch.setenv('ENVIRONMENT', 'testing')
    monkeypatch.setenv('APP_NAME', 'Multi-Agent AI Chat System')
    monkeypatch.setenv('DEBUG', 'false')
    monkeypatch.setenv('DATABASE__URL', 'sqlite:///./data/chatbot.db')
    monkeypatch.setenv('LOGGING__CONSOLE_OUTPUT', 'false')
    reload_settings()
    test_settings = create_settings(Environment.TESTING)
    assert test_settings.app_name == "Multi-Agent AI Chat System"
    assert test_settings.debug is False
    assert test_settings.database.url == "sqlite:///./data/chatbot.db"
    assert test_settings.logging.console_output is False

def test_nested_settings(monkeypatch):
    """Test nested configuration settings access."""
    monkeypatch.setenv('ENVIRONMENT', 'development')
    monkeypatch.setenv('DATABASE__URL', 'sqlite:///./data/chatbot.db')
    monkeypatch.setenv('DATABASE__POOL_SIZE', '5')
    monkeypatch.setenv('DATABASE__ECHO', 'false')
    monkeypatch.setenv('LLM__PROVIDER', 'ollama')
    monkeypatch.setenv('LLM__OLLAMA__BASE_URL', 'http://localhost:11434')
    monkeypatch.setenv('LLM__OLLAMA__MODEL', 'llama2')
    monkeypatch.setenv('LLM__OPENROUTER__MODEL', 'anthropic/claude-3-haiku')
    monkeypatch.setenv('LLM__MAX_TOKENS', '2048')
    monkeypatch.setenv('LLM__TEMPERATURE', '0.7')
    monkeypatch.setenv('AGENTS__RESPONSE_TIMEOUT', '30')
    monkeypatch.setenv('AGENTS__MAX_CONVERSATION_ROUNDS', '20')
    monkeypatch.setenv('AGENTS__CONSENSUS_THRESHOLD', '0.8')
    monkeypatch.setenv('SERVER__HOST', '127.0.0.1')
    monkeypatch.setenv('SERVER__PORT', '8000')
    monkeypatch.setenv('SERVER__WORKERS', '1')
    monkeypatch.setenv('SERVER__RELOAD', 'true')
    reload_settings()
    settings = get_settings()
    
    # Test database settings
    assert settings.database.url == "sqlite:///./data/chatbot.db"
    assert settings.database.pool_size == 5
    assert settings.database.echo is False
    
    # Test LLM settings
    assert settings.llm.provider == "ollama"
    assert settings.llm.ollama.base_url == "http://localhost:11434"
    assert settings.llm.ollama.model == "llama2"
    assert settings.llm.openrouter.model == "anthropic/claude-3-haiku"
    assert settings.llm.max_tokens == 2048
    assert settings.llm.temperature == 0.7
    
    # Test agent settings
    assert settings.agents.response_timeout == 30
    assert settings.agents.max_conversation_rounds == 20
    assert settings.agents.consensus_threshold == 0.8
    
    # Test server settings
    assert settings.server.host == "127.0.0.1"
    assert settings.server.port == 8000
    assert settings.server.workers == 1
    assert settings.server.reload is True

def test_utility_methods(monkeypatch):
    """Test configuration utility methods."""
    monkeypatch.setenv('ENVIRONMENT', 'development')
    monkeypatch.setenv('DATABASE__URL', 'sqlite:///./data/chatbot.db')
    monkeypatch.setenv('SECURITY__CORS_ORIGINS', '["http://localhost:3000", "http://localhost:8501", "http://127.0.0.1:3000", "http://127.0.0.1:8501"]')
    monkeypatch.setenv('SECURITY__CORS_CREDENTIALS', 'true')
    reload_settings()
    settings = get_settings()
    
    # Test environment checks
    assert settings.is_development is True
    assert settings.is_testing is False
    assert settings.is_production is False
    
    # Test database URL formatting
    db_url = settings.get_database_url()
    assert db_url == "sqlite:///./data/chatbot.db"
    
    # Test CORS configuration
    cors_config = settings.get_cors_config()
    assert len(cors_config['allow_origins']) == 4
    assert cors_config['allow_credentials'] is True

def test_production_validation(monkeypatch):
    """Test production readiness validation."""
    # Test with current settings (development)
    monkeypatch.setenv('ENVIRONMENT', 'development')
    reload_settings()
    settings = get_settings()
    issues = settings.validate_production_readiness()
    assert not issues # No issues in development
    
    # Test production settings with issues
    monkeypatch.setenv('ENVIRONMENT', 'production')
    monkeypatch.setenv('DEBUG', 'true') # Force debug on
    monkeypatch.setenv('DATABASE__URL', 'sqlite:///./data/chatbot.db') # Localhost DB
    monkeypatch.setenv('SECURITY__SECRET_KEY', '' ) # Missing secret key
    monkeypatch.setenv('LLM__OPENROUTER__API_KEY', '' ) # Missing API key
    monkeypatch.setenv('SERVER__HOST', '127.0.0.1') # Localhost server
    
    with pytest.raises(ValueError, match="Debug mode must be disabled in production"):
        reload_settings()
    
    # Test valid production settings
    monkeypatch.setenv('ENVIRONMENT', 'production')
    monkeypatch.setenv('DEBUG', 'false')
    monkeypatch.setenv('DATABASE__URL', 'postgresql://user:pass@host:port/db')
    monkeypatch.setenv('SECURITY__SECRET_KEY', 'super-secret-key')
    monkeypatch.setenv('LLM__OPENROUTER__API_KEY', 'pk-test-key')
    monkeypatch.setenv('SERVER__HOST', '0.0.0.0')
    
    reload_settings()
    prod_settings_valid = get_settings()
    issues_valid = prod_settings_valid.validate_production_readiness()
    assert not issues_valid

def test_environment_specific_config(monkeypatch):
    """Test environment-specific configuration loading."""
    from backend.config import LogLevel # Import LogLevel here
    environments = [Environment.DEVELOPMENT, Environment.TESTING]
    
    for env in environments:
        monkeypatch.setenv('ENVIRONMENT', env.value)
        if env == Environment.DEVELOPMENT:
            monkeypatch.setenv('DEBUG', 'true')
            monkeypatch.setenv('LOGGING__LEVEL', 'INFO')
            monkeypatch.setenv('SERVER__RELOAD', 'true')
            monkeypatch.setenv('SERVER__WORKERS', '1')
            monkeypatch.setenv('DATABASE__ECHO', 'false')
        elif env == Environment.TESTING:
            monkeypatch.setenv('DEBUG', 'false')
            monkeypatch.setenv('LOGGING__LEVEL', 'WARNING')
            monkeypatch.setenv('SERVER__RELOAD', 'false')
            monkeypatch.setenv('SERVER__WORKERS', '1')
            monkeypatch.setenv('SERVER__ACCESS_LOG', 'false')
            monkeypatch.setenv('DATABASE__ECHO', 'false')
        reload_settings()
        settings = create_settings(env)
        if env == Environment.DEVELOPMENT:
            assert settings.debug is True
            assert settings.logging.level == LogLevel.DEBUG
            assert settings.server.reload is True
            assert settings.server.workers == 1
            assert settings.database.echo is False
        elif env == Environment.TESTING:
            assert settings.debug is False
            assert settings.logging.level == LogLevel.WARNING
            assert settings.server.reload is False
            assert settings.server.workers == 1
            assert settings.server.access_log is False
            assert settings.database.echo is False

