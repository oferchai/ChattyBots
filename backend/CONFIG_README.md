# Configuration Management System

This document describes the comprehensive configuration management system for the Multi-Agent AI Chat System.

## Overview

The configuration system uses Pydantic Settings to provide:
- **Structured configuration models** with validation
- **Environment-specific settings** (development/testing/production)
- **Nested configuration sections** for different components
- **Environment variable integration** with type validation
- **Production readiness validation** with security checks
- **FastAPI dependency injection** support

## Configuration Structure

```python
from backend.config import get_settings

settings = get_settings()

# Access nested configuration
print(f"Database: {settings.database.url}")
print(f"LLM Provider: {settings.llm.provider.value}")
print(f"Agent timeout: {settings.agents.response_timeout}")
print(f"CORS origins: {settings.security.cors_origins}")
```

### Configuration Sections

- **Application**: Basic app metadata and environment
- **Server**: Host, port, workers, SSL configuration
- **Database**: Connection settings, pool configuration
- **Security**: CORS, API keys, rate limiting, secrets
- **LLM**: Provider settings for Ollama and OpenRouter
- **Agents**: Behavior configuration, timeouts, limits
- **Logging**: Log levels, file paths, formatting

## Environment-Specific Configuration

### Development (`.env.development`)
- Debug mode enabled
- Verbose logging (DEBUG level)
- SQL query echoing
- Auto-reload enabled
- Local database file
- Higher rate limits

### Testing (`.env.testing`)
- Debug mode disabled
- Minimal logging (WARNING level)
- In-memory database
- Fast timeouts for quick tests
- Reduced conversation limits
- No console output

### Production (`.env.production.template`)
- Security hardened
- Structured JSON logging
- External database connections
- SSL configuration
- Lower rate limits
- Production-ready defaults

## Usage

### Basic Usage
```python
from backend.config import get_settings

# Get global settings instance (singleton)
settings = get_settings()
```

### Environment-Specific Settings
```python
from backend.config import create_settings, Environment

# Load specific environment
dev_settings = create_settings(Environment.DEVELOPMENT)
test_settings = create_settings(Environment.TESTING)
```

### Environment Detection
```python
from backend.config import get_environment

# Auto-detect from ENVIRONMENT variable
current_env = get_environment()
print(f"Running in: {current_env.value}")
```

### FastAPI Integration
```python
from fastapi import Depends
from backend.config import get_settings, Settings

@app.get("/config")
async def get_config(settings: Settings = Depends(get_settings)):
    return {"environment": settings.environment.value}
```

## Environment Variables

The system supports nested environment variables using double underscores (`__`):

```bash
# Application settings
APP_NAME="My Chat System"
VERSION="1.2.0"
ENVIRONMENT=development
DEBUG=true

# Database settings
DATABASE__URL="sqlite:///./data/app.db"
DATABASE__POOL_SIZE=10
DATABASE__ECHO=true

# LLM settings
LLM__PROVIDER=ollama
LLM__OLLAMA__BASE_URL="http://localhost:11434"
LLM__OLLAMA__MODEL="llama2"
LLM__OPENROUTER__API_KEY="your_key_here"

# Agent settings
AGENTS__RESPONSE_TIMEOUT=30
AGENTS__MAX_CONVERSATION_ROUNDS=20
AGENTS__CONSENSUS_THRESHOLD=0.8

# Security settings
SECURITY__SECRET_KEY="your-secret-key"
SECURITY__CORS_ORIGINS=["http://localhost:3000"]
SECURITY__RATE_LIMIT_PER_MINUTE=100
```

## Configuration Files

### Environment Files
- `.env.development` - Development configuration
- `.env.testing` - Testing configuration  
- `.env.production.template` - Production template (copy to `.env.production`)
- `.env` - Generic fallback configuration

### File Priority
1. Environment-specific file (`.env.development`)
2. Generic file (`.env`)
3. Environment variables
4. Default values in code

## Validation

The system includes comprehensive validation:

### Field Validation
- Type checking (int, float, bool, enum)
- Range validation (min/max values)
- Format validation (URLs, file paths)
- Custom validators for complex fields

### Production Validation
```python
settings = get_settings()

if settings.is_production:
    issues = settings.validate_production_readiness()
    if issues:
        raise ValueError(f"Production issues: {'; '.join(issues)}")
```

Common production validation checks:
- Debug mode disabled
- Strong secret keys configured
- External database (not localhost)
- SSL configuration present
- API keys provided

## Utility Methods

### Database Configuration
```python
# Get formatted database URL
db_url = settings.get_database_url()

# Check environment
if settings.is_development:
    print("Running in development mode")
```

### CORS Configuration
```python
# Get CORS config for FastAPI
cors_config = settings.get_cors_config()

app.add_middleware(CORSMiddleware, **cors_config)
```

## Testing

Run the configuration test suite:

```bash
# Test current environment
python test_config.py

# Test specific environment
python test_config.py development
python test_config.py testing
python test_config.py production
```

## Security Considerations

### Sensitive Data
- Never commit `.env.production` to version control
- Use strong secret keys in production
- Limit CORS origins to trusted domains
- Use environment variables for API keys

### Production Checklist
- [ ] Debug mode disabled
- [ ] Strong secret key configured
- [ ] External database configured
- [ ] SSL certificates configured
- [ ] API keys provided
- [ ] CORS origins restricted
- [ ] Rate limiting configured
- [ ] Logging configured properly

## Examples

### Development Setup
```bash
# Copy development template
cp .env.development .env

# Set any overrides
echo "DATABASE__URL=sqlite:///./data/my_dev.db" >> .env

# Run application
python -m backend.app.main
```

### Production Setup
```bash
# Copy production template
cp .env.production.template .env.production

# Edit production configuration
vim .env.production

# Set environment
export ENVIRONMENT=production

# Run with production settings
python -m backend.app.main
```

### Docker Configuration
```dockerfile
# Set environment in Dockerfile
ENV ENVIRONMENT=production

# Copy production config
COPY .env.production /app/.env.production

# Application will auto-load production settings
CMD ["python", "-m", "backend.app.main"]
```

## Troubleshooting

### Common Issues

1. **Module not found: pydantic_settings**
   ```bash
   conda install -c conda-forge pydantic-settings
   ```

2. **Configuration not loading**
   - Check file paths and environment variables
   - Verify ENVIRONMENT variable is set correctly
   - Run configuration test: `python test_config.py`

3. **Validation errors**
   - Check data types match expected types
   - Verify required fields are provided
   - Review validation error messages

4. **Environment detection issues**
   ```bash
   export ENVIRONMENT=development  # or testing, production
   python test_config.py
   ```

For more details, see the comprehensive test suite in `test_config.py`.
