"""
Configuration settings for the Multi-Agent AI Chat System
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "Multi-Agent AI Chat System"
    debug: bool = True
    host: str = "localhost"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./data/chatbot.db"
    
    # LLM Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    openrouter_api_key: Optional[str] = None
    openrouter_model: str = "anthropic/claude-3-haiku"
    
    # Agent Configuration
    max_conversation_rounds: int = 20
    consensus_threshold: float = 0.8
    agent_response_timeout: int = 30
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./data/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
