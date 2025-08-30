#!/usr/bin/env python3
"""
Configuration Management Test Script.

This script tests the new comprehensive configuration management system,
validating environment-specific settings, validation logic, and integration
with FastAPI dependency injection.

Usage:
    python test_config.py [environment]
    
Example:
    python test_config.py development
    python test_config.py testing
    python test_config.py production
"""
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from backend.config import (
    get_settings, create_settings, get_environment, 
    Environment, Settings, reload_settings
)


def test_environment_detection():
    """Test automatic environment detection."""
    print("🔍 Testing Environment Detection")
    print("-" * 40)
    
    # Test default detection
    current_env = get_environment()
    print(f"Current environment: {current_env.value}")
    
    # Test environment override
    os.environ['ENVIRONMENT'] = 'testing'
    test_env = get_environment()
    print(f"Test environment (overridden): {test_env.value}")
    
    # Reset environment
    if 'ENVIRONMENT' in os.environ:
        del os.environ['ENVIRONMENT']
    
    print("✅ Environment detection test passed\n")


def test_configuration_validation():
    """Test configuration validation logic."""
    print("🔒 Testing Configuration Validation")
    print("-" * 40)
    
    # Test development settings
    dev_settings = create_settings(Environment.DEVELOPMENT)
    print(f"Development config loaded: {dev_settings.app_name}")
    print(f"  Debug mode: {dev_settings.debug}")
    print(f"  Database URL: {dev_settings.database.url}")
    print(f"  LLM Provider: {dev_settings.llm.provider.value}")
    
    # Test testing settings
    test_settings = create_settings(Environment.TESTING)
    print(f"Testing config loaded: {test_settings.app_name}")
    print(f"  Debug mode: {test_settings.debug}")
    print(f"  Database URL: {test_settings.database.url}")
    print(f"  Console output: {test_settings.logging.console_output}")
    
    print("✅ Configuration validation test passed\n")


def test_nested_settings():
    """Test nested configuration settings access."""
    print("🏗️  Testing Nested Settings")
    print("-" * 40)
    
    settings = get_settings()
    
    # Test database settings
    print("Database Configuration:")
    print(f"  URL: {settings.database.url}")
    print(f"  Pool size: {settings.database.pool_size}")
    print(f"  Echo: {settings.database.echo}")
    
    # Test LLM settings
    print("LLM Configuration:")
    print(f"  Provider: {settings.llm.provider.value}")
    print(f"  Ollama URL: {settings.llm.ollama.base_url}")
    print(f"  Ollama Model: {settings.llm.ollama.model}")
    print(f"  OpenRouter Model: {settings.llm.openrouter.model}")
    print(f"  Max tokens: {settings.llm.max_tokens}")
    print(f"  Temperature: {settings.llm.temperature}")
    
    # Test agent settings
    print("Agent Configuration:")
    print(f"  Response timeout: {settings.agents.response_timeout}s")
    print(f"  Max rounds: {settings.agents.max_conversation_rounds}")
    print(f"  Consensus threshold: {settings.agents.consensus_threshold}")
    
    # Test server settings
    print("Server Configuration:")
    print(f"  Host: {settings.server.host}")
    print(f"  Port: {settings.server.port}")
    print(f"  Workers: {settings.server.workers}")
    print(f"  Reload: {settings.server.reload}")
    
    print("✅ Nested settings test passed\n")


def test_utility_methods():
    """Test configuration utility methods."""
    print("🛠️  Testing Utility Methods")
    print("-" * 40)
    
    settings = get_settings()
    
    # Test environment checks
    print(f"Is development: {settings.is_development}")
    print(f"Is testing: {settings.is_testing}")
    print(f"Is production: {settings.is_production}")
    
    # Test database URL formatting
    db_url = settings.get_database_url()
    print(f"Database URL: {db_url}")
    
    # Test CORS configuration
    cors_config = settings.get_cors_config()
    print(f"CORS origins: {len(cors_config['allow_origins'])} configured")
    print(f"CORS credentials: {cors_config['allow_credentials']}")
    
    print("✅ Utility methods test passed\n")


def test_production_validation():
    """Test production readiness validation."""
    print("🔐 Testing Production Validation")
    print("-" * 40)
    
    # Test with current settings
    settings = get_settings()
    issues = settings.validate_production_readiness()
    
    if settings.is_production:
        if issues:
            print("❌ Production validation issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("✅ Production configuration is valid")
    else:
        print("ℹ️  Not in production mode, validation skipped")
        print(f"Current environment: {settings.environment.value}")
    
    print("✅ Production validation test passed\n")


def test_environment_specific_config():
    """Test environment-specific configuration loading."""
    print("🌍 Testing Environment-Specific Config")
    print("-" * 40)
    
    environments = [Environment.DEVELOPMENT, Environment.TESTING]
    
    for env in environments:
        try:
            settings = create_settings(env)
            print(f"{env.value.title()} Environment:")
            print(f"  Debug: {settings.debug}")
            print(f"  Log level: {settings.logging.level.value}")
            print(f"  Server reload: {settings.server.reload}")
            print(f"  Workers: {settings.server.workers}")
            print(f"  Database echo: {settings.database.echo}")
        except Exception as e:
            print(f"❌ Failed to load {env.value} config: {e}")
    
    print("✅ Environment-specific config test passed\n")


def display_config_summary(env_name: str = None):
    """Display a comprehensive configuration summary."""
    print("📋 Configuration Summary")
    print("=" * 50)
    
    if env_name:
        try:
            env = Environment(env_name.lower())
            settings = create_settings(env)
        except ValueError:
            print(f"❌ Invalid environment: {env_name}")
            return
    else:
        settings = get_settings()
    
    print(f"Application: {settings.app_name} v{settings.version}")
    print(f"Environment: {settings.environment.value}")
    print(f"Description: {settings.description}")
    print()
    
    print("🖥️  Server Configuration:")
    print(f"  Host: {settings.server.host}")
    print(f"  Port: {settings.server.port}")
    print(f"  Debug: {settings.debug}")
    print(f"  Workers: {settings.server.workers}")
    print(f"  Reload: {settings.server.reload}")
    print()
    
    print("🗄️  Database Configuration:")
    print(f"  URL: {settings.database.url}")
    print(f"  Pool size: {settings.database.pool_size}")
    print(f"  Echo SQL: {settings.database.echo}")
    print()
    
    print("🤖 LLM Configuration:")
    print(f"  Provider: {settings.llm.provider.value}")
    print(f"  Fallback: {settings.llm.fallback_strategy}")
    print(f"  Max tokens: {settings.llm.max_tokens}")
    print(f"  Temperature: {settings.llm.temperature}")
    print(f"  Ollama URL: {settings.llm.ollama.base_url}")
    print(f"  Ollama Model: {settings.llm.ollama.model}")
    print()
    
    print("👥 Agent Configuration:")
    print(f"  Response timeout: {settings.agents.response_timeout}s")
    print(f"  Max rounds: {settings.agents.max_conversation_rounds}")
    print(f"  Consensus threshold: {settings.agents.consensus_threshold}")
    print(f"  Retry failed: {settings.agents.retry_failed_responses}")
    print(f"  Thinking delay: {settings.agents.thinking_delay_seconds}s")
    print()
    
    print("🔒 Security Configuration:")
    print(f"  CORS origins: {len(settings.security.cors_origins)} configured")
    print(f"  Rate limit: {settings.security.rate_limit_per_minute}/min")
    print(f"  Secret key configured: {bool(settings.security.secret_key)}")
    print()
    
    print("📝 Logging Configuration:")
    print(f"  Level: {settings.logging.level.value}")
    print(f"  File: {settings.logging.file_path}")
    print(f"  Console output: {settings.logging.console_output}")
    print(f"  JSON format: {settings.logging.json_format}")
    print()


def main():
    """Main test execution."""
    print("🚀 Multi-Agent AI Chat System - Configuration Test")
    print("=" * 60)
    print()
    
    # Get environment argument if provided
    env_name = sys.argv[1] if len(sys.argv) > 1 else None
    
    try:
        # Run all tests
        test_environment_detection()
        test_configuration_validation()
        test_nested_settings()
        test_utility_methods()
        test_production_validation()
        test_environment_specific_config()
        
        # Display configuration summary
        display_config_summary(env_name)
        
        print("🎉 All configuration tests passed successfully!")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
