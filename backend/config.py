"""
Configuration management for Multi-Agent AI Chat System.

This module provides comprehensive configuration management with environment-specific
settings, validation, and dependency injection support for the FastAPI application.

Example:
    from backend.config import get_settings
    
    settings = get_settings()
    print(f"Running in {settings.environment} mode")
    print(f"Database: {settings.database.url}")
"""
import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LLMProvider(str, Enum):
    """LLM provider options."""
    OLLAMA = "ollama"
    OPENROUTER = "openrouter"
    BOTH = "both"  # Try ollama first, fallback to openrouter


class DatabaseSettings(BaseModel):
    """
    Database configuration settings.
    
    Attributes:
        url: Database connection URL
        pool_size: Connection pool size
        max_overflow: Maximum overflow connections
        pool_timeout: Connection timeout in seconds
        pool_recycle: Connection recycle time in seconds
        echo: Whether to echo SQL queries (development only)
    """
    
    url: str = Field(
        default="sqlite:///./data/chatbot.db",
        description="Database connection URL"
    )
    pool_size: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Connection pool size"
    )
    max_overflow: int = Field(
        default=10,
        ge=0,
        le=100,
        description="Maximum overflow connections"
    )
    pool_timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Connection timeout in seconds"
    )
    pool_recycle: int = Field(
        default=3600,
        ge=300,
        le=86400,
        description="Connection recycle time in seconds"
    )
    echo: bool = Field(
        default=False,
        description="Echo SQL queries for debugging"
    )
    
    @validator('url')
    def validate_database_url(cls, v):
        """Validate database URL format."""
        if not v:
            raise ValueError("Database URL cannot be empty")
        if not (v.startswith('sqlite://') or v.startswith('postgresql://') or v.startswith('mysql://')):
            raise ValueError("Database URL must use sqlite://, postgresql://, or mysql:// scheme")
        return v


class SecuritySettings(BaseModel):
    """
    Security configuration settings.
    
    Attributes:
        cors_origins: Allowed CORS origins
        cors_credentials: Allow credentials in CORS
        cors_methods: Allowed HTTP methods
        cors_headers: Allowed headers
        api_keys: API keys for external services
        rate_limit_per_minute: Rate limiting threshold
        secret_key: Application secret key
    """
    
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8501",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8501"
        ],
        description="Allowed CORS origins"
    )
    cors_credentials: bool = Field(
        default=True,
        description="Allow credentials in CORS requests"
    )
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE"],
        description="Allowed HTTP methods"
    )
    cors_headers: List[str] = Field(
        default=["*"],
        description="Allowed headers"
    )
    api_keys: Dict[str, str] = Field(
        default_factory=dict,
        description="API keys for external services"
    )
    rate_limit_per_minute: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Rate limiting threshold per minute"
    )
    secret_key: Optional[str] = Field(
        default=None,
        description="Application secret key for JWT/sessions"
    )
    
    @validator('cors_origins')
    def validate_cors_origins(cls, v):
        """Validate CORS origins format."""
        for origin in v:
            if not origin.startswith(('http://', 'https://')):
                raise ValueError(f"Invalid CORS origin format: {origin}")
        return v


class OllamaSettings(BaseModel):
    """
    Ollama (local LLM) configuration.
    
    Attributes:
        base_url: Ollama server URL
        model: Default model to use
        timeout: Request timeout in seconds
        max_retries: Maximum retry attempts
        health_check_interval: Health check frequency in seconds
    """
    
    base_url: str = Field(
        default="http://localhost:11434",
        description="Ollama server base URL"
    )
    model: str = Field(
        default="llama2",
        description="Default Ollama model"
    )
    timeout: int = Field(
        default=60,
        ge=10,
        le=300,
        description="Request timeout in seconds"
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum retry attempts"
    )
    health_check_interval: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Health check frequency in seconds"
    )
    
    @validator('base_url')
    def validate_base_url(cls, v):
        """Validate Ollama base URL format."""
        if not v.startswith(('http://', 'https://')):
            raise ValueError("Ollama base URL must start with http:// or https://")
        return v.rstrip('/')


class OpenRouterSettings(BaseModel):
    """
    OpenRouter (cloud LLM) configuration.
    
    Attributes:
        api_key: OpenRouter API key
        model: Default model to use
        base_url: OpenRouter API base URL
        timeout: Request timeout in seconds
        max_retries: Maximum retry attempts
        cost_limit_usd: Monthly cost limit in USD
    """
    
    api_key: Optional[str] = Field(
        default=None,
        description="OpenRouter API key"
    )
    model: str = Field(
        default="anthropic/claude-3-haiku",
        description="Default OpenRouter model"
    )
    base_url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="OpenRouter API base URL"
    )
    timeout: int = Field(
        default=90,
        ge=10,
        le=300,
        description="Request timeout in seconds"
    )
    max_retries: int = Field(
        default=3,
        ge=0,
        le=10,
        description="Maximum retry attempts"
    )
    cost_limit_usd: float = Field(
        default=50.0,
        ge=0.0,
        le=1000.0,
        description="Monthly cost limit in USD"
    )
    
    @validator('api_key')
    def validate_api_key(cls, v):
        """Validate API key format."""
        if v and len(v) < 10:
            raise ValueError("OpenRouter API key seems too short")
        return v


class LLMSettings(BaseModel):
    """
    LLM (Language Learning Model) configuration.
    
    Attributes:
        provider: Primary LLM provider to use
        fallback_strategy: How to handle provider failures
        ollama: Ollama-specific settings
        openrouter: OpenRouter-specific settings
        max_tokens: Maximum tokens per request
        temperature: Response creativity (0.0-2.0)
        context_window: Maximum context window size
    """
    
    provider: LLMProvider = Field(
        default=LLMProvider.OLLAMA,
        description="Primary LLM provider"
    )
    fallback_strategy: Literal["none", "openrouter", "retry"] = Field(
        default="openrouter",
        description="Fallback strategy when primary provider fails"
    )
    ollama: OllamaSettings = Field(
        default_factory=OllamaSettings,
        description="Ollama configuration"
    )
    openrouter: OpenRouterSettings = Field(
        default_factory=OpenRouterSettings,
        description="OpenRouter configuration"
    )
    max_tokens: int = Field(
        default=2048,
        ge=100,
        le=8192,
        description="Maximum tokens per request"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Response creativity (0.0-2.0)"
    )
    context_window: int = Field(
        default=4096,
        ge=512,
        le=32768,
        description="Maximum context window size"
    )


class AgentSettings(BaseModel):
    """
    Agent behavior configuration.
    
    Attributes:
        response_timeout: Maximum time for agent response
        max_conversation_rounds: Maximum discussion rounds
        consensus_threshold: Agreement threshold for decisions
        retry_failed_responses: Whether to retry failed agent responses
        max_message_length: Maximum length for agent messages
        thinking_delay_seconds: Simulated thinking delay
    """
    
    response_timeout: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Maximum time for agent response in seconds"
    )
    max_conversation_rounds: int = Field(
        default=20,
        ge=3,
        le=100,
        description="Maximum discussion rounds before timeout"
    )
    consensus_threshold: float = Field(
        default=0.8,
        ge=0.5,
        le=1.0,
        description="Agreement threshold for decisions (0.5-1.0)"
    )
    retry_failed_responses: bool = Field(
        default=True,
        description="Whether to retry failed agent responses"
    )
    max_message_length: int = Field(
        default=5000,
        ge=100,
        le=50000,
        description="Maximum length for agent messages"
    )
    thinking_delay_seconds: float = Field(
        default=1.0,
        ge=0.0,
        le=10.0,
        description="Simulated thinking delay in seconds"
    )


class LoggingSettings(BaseModel):
    """
    Logging configuration.
    
    Attributes:
        level: Logging level
        file_path: Log file path
        max_file_size_mb: Maximum log file size in MB
        backup_count: Number of backup log files
        json_format: Whether to use JSON formatting
        console_output: Whether to output to console
    """
    
    level: LogLevel = Field(
        default=LogLevel.INFO,
        description="Logging level"
    )
    file_path: str = Field(
        default="./data/app.log",
        description="Log file path"
    )
    max_file_size_mb: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Maximum log file size in MB"
    )
    backup_count: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of backup log files"
    )
    json_format: bool = Field(
        default=True,
        description="Whether to use JSON log formatting"
    )
    console_output: bool = Field(
        default=True,
        description="Whether to output logs to console"
    )


class ServerSettings(BaseModel):
    """
    Server configuration.
    
    Attributes:
        host: Server host address
        port: Server port number
        workers: Number of worker processes (production)
        reload: Enable auto-reload (development)
        access_log: Enable access logging
        ssl_keyfile: SSL key file path
        ssl_certfile: SSL certificate file path
    """
    
    host: str = Field(
        default="127.0.0.1",
        description="Server host address"
    )
    port: int = Field(
        default=8000,
        ge=1000,
        le=65535,
        description="Server port number"
    )
    workers: int = Field(
        default=1,
        ge=1,
        le=32,
        description="Number of worker processes"
    )
    reload: bool = Field(
        default=True,
        description="Enable auto-reload (development only)"
    )
    access_log: bool = Field(
        default=True,
        description="Enable access logging"
    )
    ssl_keyfile: Optional[str] = Field(
        default=None,
        description="SSL key file path"
    )
    ssl_certfile: Optional[str] = Field(
        default=None,
        description="SSL certificate file path"
    )
    
    @validator('port')
    def validate_port(cls, v):
        """Validate port number."""
        if v < 1000 or v > 65535:
            raise ValueError("Port must be between 1000 and 65535")
        return v


class Settings(BaseSettings):
    """
    Main application settings.
    
    Comprehensive configuration management with environment-specific settings,
    validation, and structured organization.
    
    Attributes:
        app_name: Application name
        version: Application version
        description: Application description
        environment: Current environment (development/testing/production)
        debug: Debug mode flag
        server: Server configuration
        database: Database configuration
        security: Security configuration
        llm: LLM provider configuration
        agents: Agent behavior configuration
        logging: Logging configuration
    
    Example:
        settings = Settings()
        print(f"App: {settings.app_name} v{settings.version}")
        print(f"Environment: {settings.environment}")
        print(f"Database: {settings.database.url}")
    """
    
    # Application metadata
    app_name: str = Field(
        default="Multi-Agent AI Chat System",
        description="Application name"
    )
    version: str = Field(
        default="1.0.0",
        description="Application version"
    )
    description: str = Field(
        default="Backend API for coordinating AI agent conversations",
        description="Application description"
    )
    
    # Environment
    environment: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Current application environment"
    )
    debug: bool = Field(
        default=True,
        description="Enable debug mode"
    )
    
    # Nested configuration sections
    server: ServerSettings = Field(
        default_factory=ServerSettings,
        description="Server configuration"
    )
    database: DatabaseSettings = Field(
        default_factory=DatabaseSettings,
        description="Database configuration"
    )
    security: SecuritySettings = Field(
        default_factory=SecuritySettings,
        description="Security configuration"
    )
    llm: LLMSettings = Field(
        default_factory=LLMSettings,
        description="LLM provider configuration"
    )
    agents: AgentSettings = Field(
        default_factory=AgentSettings,
        description="Agent behavior configuration"
    )
    logging: LoggingSettings = Field(
        default_factory=LoggingSettings,
        description="Logging configuration"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_nested_delimiter = "__"
        case_sensitive = False
        
        # Allow field population from environment variables
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                env_settings,
                file_secret_settings,
            )
    
    @validator('debug')
    def validate_debug_in_production(cls, v, values):
        """Ensure debug is disabled in production."""
        environment = values.get('environment')
        if environment == Environment.PRODUCTION and v:
            raise ValueError("Debug mode must be disabled in production")
        return v
    
    @validator('logging')
    def configure_logging_for_environment(cls, v, values):
        """Configure logging based on environment."""
        environment = values.get('environment')
        debug = values.get('debug', True)
        
        if environment == Environment.DEVELOPMENT:
            v.level = LogLevel.DEBUG if debug else LogLevel.INFO
            v.console_output = True
        elif environment == Environment.TESTING:
            v.level = LogLevel.WARNING
            v.console_output = False
        elif environment == Environment.PRODUCTION:
            v.level = LogLevel.INFO
            v.json_format = True
            v.console_output = True
        
        return v
    
    @validator('server')
    def configure_server_for_environment(cls, v, values):
        """Configure server based on environment."""
        environment = values.get('environment')
        
        if environment == Environment.DEVELOPMENT:
            v.reload = True
            v.workers = 1
        elif environment == Environment.TESTING:
            v.reload = False
            v.workers = 1
            v.access_log = False
        elif environment == Environment.PRODUCTION:
            v.reload = False
            v.workers = min(4, (os.cpu_count() or 1) + 1)
            v.host = "0.0.0.0"  # Listen on all interfaces
        
        return v
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == Environment.TESTING
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION
    
    def get_database_url(self) -> str:
        """Get properly formatted database URL."""
        return self.database.url
    
    def get_cors_config(self) -> Dict[str, Union[List[str], bool]]:
        """Get CORS configuration for FastAPI."""
        return {
            "allow_origins": self.security.cors_origins,
            "allow_credentials": self.security.cors_credentials,
            "allow_methods": self.security.cors_methods,
            "allow_headers": self.security.cors_headers,
        }
    
    def validate_production_readiness(self) -> List[str]:
        """
        Validate configuration for production deployment.
        
        Returns:
            List of configuration issues (empty if valid)
        """
        issues = []
        
        if self.environment == Environment.PRODUCTION:
            if self.debug:
                issues.append("Debug mode should be disabled in production")
            
            if "localhost" in self.database.url:
                issues.append("Production should not use localhost database")
            
            if not self.llm.openrouter.api_key and self.llm.provider != LLMProvider.OLLAMA:
                issues.append("OpenRouter API key required for production LLM")
            
            if not self.security.secret_key:
                issues.append("Secret key required for production security")
            
            if self.server.host == "127.0.0.1":
                issues.append("Production server should listen on 0.0.0.0")
        
        return issues


# Configuration factory functions
def get_environment() -> Environment:
    """
    Detect current environment from environment variables.
    
    Returns:
        Current environment
    """
    env_str = os.getenv("ENVIRONMENT", "development").lower()
    
    try:
        return Environment(env_str)
    except ValueError:
        print(f"Warning: Unknown environment '{env_str}', defaulting to development")
        return Environment.DEVELOPMENT


def get_env_file_path(environment: Environment) -> str:
    """
    Get environment-specific .env file path.
    
    Args:
        environment: Target environment
        
    Returns:
        Path to environment-specific .env file
    """
    base_path = Path(__file__).parent.parent
    
    env_files = {
        Environment.DEVELOPMENT: base_path / ".env.development",
        Environment.TESTING: base_path / ".env.testing", 
        Environment.PRODUCTION: base_path / ".env.production"
    }
    
    env_file = env_files.get(environment, base_path / ".env")
    
    # Fallback to generic .env if environment-specific file doesn't exist
    if not env_file.exists():
        fallback = base_path / ".env"
        if fallback.exists():
            return str(fallback)
    
    return str(env_file)


def create_settings(environment: Optional[Environment] = None) -> Settings:
    """
    Create settings instance for specific environment.
    
    Args:
        environment: Target environment (auto-detected if None)
        
    Returns:
        Configured settings instance
    """
    if environment is None:
        environment = get_environment()
    
    env_file = get_env_file_path(environment)
    
    # Create settings with environment-specific file
    settings = Settings(
        environment=environment,
        _env_file=env_file
    )
    
    # Validate production readiness if needed
    if environment == Environment.PRODUCTION:
        issues = settings.validate_production_readiness()
        if issues:
            raise ValueError(f"Production configuration issues: {'; '.join(issues)}")
    
    return settings


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get global settings instance (singleton pattern).
    
    Returns:
        Global settings instance
        
    Example:
        from backend.config import get_settings
        
        settings = get_settings()
        print(f"Running in {settings.environment} mode")
    """
    global _settings
    
    if _settings is None:
        _settings = create_settings()
    
    return _settings


def reload_settings() -> Settings:
    """
    Reload settings from environment (useful for testing).
    
    Returns:
        Newly loaded settings instance
    """
    global _settings
    _settings = None
    return get_settings()


# Legacy compatibility
settings = get_settings()
