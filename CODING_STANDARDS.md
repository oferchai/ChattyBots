# Coding Standards - Multi-Agent AI Chat System

## 🎯 Purpose

This document establishes coding standards for the Multi-Agent AI Chat System to ensure:
- **Consistency** across all code contributions
- **Readability** for both humans and AI agents
- **Maintainability** for long-term development
- **Quality** through best practices enforcement

---

## 🐍 Python Style Guide

### Base Standards
- Follow **PEP 8** - Python Style Guide
- Follow **PEP 257** - Docstring Conventions
- Use **Type Hints** (PEP 484) for all functions and methods
- Target **Python 3.11+** compatibility

### Code Formatting
- Use **Black** for automatic code formatting
- Maximum line length: **88 characters** (Black default)
- Use **4 spaces** for indentation (no tabs)
- UTF-8 encoding for all Python files

---

## 📁 Project Structure Standards

### Directory Organization
```
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── dependencies.py      # Dependency injection
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   ├── base.py         # Base model class
│   │   └── *.py            # Individual model files
│   ├── agents/              # Agent implementations
│   │   ├── __init__.py
│   │   ├── base.py         # Base agent class
│   │   └── *.py            # Individual agent files
│   ├── services/            # Business logic services
│   │   ├── __init__.py
│   │   └── *.py            # Service implementations
│   ├── api/                 # API route handlers
│   │   ├── __init__.py
│   │   └── *.py            # API endpoint files
│   └── db/                  # Database operations
│       ├── __init__.py
│       └── repositories/    # Data access layer
```

### File Naming Conventions
- Use **snake_case** for all file and directory names
- Use descriptive names: `conversation_manager.py` not `conv_mgr.py`
- Test files: `test_*.py` or `*_test.py`
- Configuration files: `config.py`, `settings.py`

---

## 🔤 Naming Conventions

### Variables and Functions
```python
# ✅ Good - snake_case
user_name = "john_doe"
conversation_id = "conv_123"

def process_user_message(message_content: str) -> str:
    return processed_content

async def fetch_conversation_history(conversation_id: str) -> List[Message]:
    return messages
```

### Classes
```python
# ✅ Good - PascalCase
class ConversationManager:
    pass

class ProjectManagerAgent:
    pass

class LLMServiceProvider:
    pass
```

### Constants
```python
# ✅ Good - SCREAMING_SNAKE_CASE
MAX_CONVERSATION_ROUNDS = 20
DEFAULT_TIMEOUT_SECONDS = 30
OLLAMA_BASE_URL = "http://localhost:11434"
```

### Private Variables/Methods
```python
# ✅ Good - Leading underscore for private
class Agent:
    def __init__(self):
        self._internal_state = {}
        self.__private_data = None  # Name mangling for truly private
    
    def _internal_method(self) -> None:
        pass
    
    def public_method(self) -> str:
        return self._internal_method()
```

---

## 📚 Documentation Standards

### Module Docstrings
```python
"""
Multi-Agent AI Chat System - Conversation Manager

This module provides conversation orchestration and management functionality
for coordinating multiple AI agents in collaborative problem-solving sessions.

Classes:
    ConversationManager: Main orchestration class
    ConversationState: State management for conversations

Functions:
    create_conversation: Initialize new conversation
    process_agent_response: Handle individual agent responses

Example:
    manager = ConversationManager()
    conversation = await manager.create_conversation(goal="Design a mobile app")
"""
```

### Class Docstrings
```python
class ConversationManager:
    """
    Manages multi-agent conversations and orchestrates discussion flow.
    
    The ConversationManager coordinates between multiple AI agents, manages
    conversation state, handles consensus building, and ensures productive
    discussion flow toward goal achievement.
    
    Attributes:
        conversation_id (str): Unique identifier for the conversation
        agents (List[BaseAgent]): List of participating agents
        current_phase (ConversationPhase): Current discussion phase
        consensus_threshold (float): Required agreement level for decisions
    
    Example:
        manager = ConversationManager(
            agents=[pm_agent, tech_agent, creative_agent],
            consensus_threshold=0.8
        )
        result = await manager.start_conversation("Build a chatbot")
    """
```

### Function Docstrings
```python
async def process_agent_response(
    agent_id: str, 
    message: str, 
    conversation_context: ConversationContext
) -> ProcessedResponse:
    """
    Process and validate an agent's response within conversation context.
    
    Takes an agent's raw response, validates it against conversation rules,
    formats it appropriately, and prepares it for distribution to other agents.
    
    Args:
        agent_id (str): Unique identifier of the responding agent
        message (str): Raw message content from the agent
        conversation_context (ConversationContext): Current conversation state
    
    Returns:
        ProcessedResponse: Validated and formatted response ready for distribution
    
    Raises:
        InvalidResponseError: When agent response fails validation
        ConversationTimeoutError: When processing exceeds timeout limits
    
    Example:
        response = await process_agent_response(
            agent_id="project_manager",
            message="I suggest we start with user research",
            conversation_context=current_context
        )
    """
```

---

## 🏗️ Code Structure Standards

### Import Organization
```python
# 1. Standard library imports
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Union
from uuid import UUID

# 2. Third-party imports
import fastapi
import sqlalchemy
from pydantic import BaseModel, Field
from langchain.llms import Ollama

# 3. Local application imports
from app.config import settings
from app.models.base import BaseModel
from app.services.llm_service import LLMService
```

### Class Structure Template
```python
class ExampleClass:
    """Class docstring here."""
    
    # Class variables first
    CLASS_CONSTANT = "value"
    
    def __init__(self, param1: str, param2: Optional[int] = None):
        """Initialize the class."""
        # Public attributes
        self.param1 = param1
        self.param2 = param2 or 0
        
        # Private attributes
        self._internal_state = {}
        self.__private_data = None
    
    # Properties next
    @property
    def state(self) -> Dict:
        """Get current internal state."""
        return self._internal_state.copy()
    
    # Public methods
    async def public_async_method(self, data: str) -> str:
        """Public async method."""
        result = await self._process_data(data)
        return result
    
    def public_sync_method(self, value: int) -> bool:
        """Public synchronous method."""
        return self._validate_value(value)
    
    # Private methods last
    async def _process_data(self, data: str) -> str:
        """Private async method."""
        return data.upper()
    
    def _validate_value(self, value: int) -> bool:
        """Private validation method."""
        return value > 0
```

---

## 🎯 Type Hints Standards

### Basic Type Hints
```python
# ✅ Good - Clear type hints
def calculate_score(votes: List[int], weights: Dict[str, float]) -> float:
    return sum(vote * weights.get(str(i), 1.0) for i, vote in enumerate(votes))

async def fetch_conversation(conversation_id: UUID) -> Optional[Conversation]:
    return await db.get_conversation(conversation_id)
```

### Complex Type Hints
```python
from typing import Dict, List, Optional, Union, Callable, TypeVar, Generic

# Type aliases for complex types
ConversationID = str
AgentID = str
MessageContent = str
ResponseCallback = Callable[[str], None]

# Generic types
T = TypeVar('T')

class Repository(Generic[T]):
    async def get(self, id: str) -> Optional[T]:
        pass
    
    async def list(self) -> List[T]:
        pass
```

### Pydantic Models
```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class MessageType(str, Enum):
    PROPOSAL = "proposal"
    QUESTION = "question"
    RESPONSE = "response"
    VOTE = "vote"
    CONSENSUS = "consensus"

class Message(BaseModel):
    """Message model with validation."""
    id: str = Field(..., description="Unique message identifier")
    conversation_id: str = Field(..., description="Parent conversation ID")
    agent_id: str = Field(..., description="ID of sending agent")
    content: str = Field(..., min_length=1, max_length=10000)
    message_type: MessageType
    created_at: datetime = Field(default_factory=datetime.utcnow)
    parent_message_id: Optional[str] = None
    
    @validator('content')
    def content_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

---

## 🔒 Error Handling Standards

### Exception Hierarchy
```python
# Base exceptions
class ChatbotError(Exception):
    """Base exception for all chatbot errors."""
    pass

class ValidationError(ChatbotError):
    """Raised when data validation fails."""
    pass

class AgentError(ChatbotError):
    """Raised when agent operations fail."""
    pass

class ConversationError(ChatbotError):
    """Raised when conversation operations fail."""
    pass

# Specific exceptions
class AgentTimeoutError(AgentError):
    """Raised when agent response times out."""
    pass

class ConversationNotFoundError(ConversationError):
    """Raised when conversation cannot be found."""
    pass
```

### Error Handling Patterns
```python
import logging
from typing import Optional

logger = logging.getLogger(__name__)

async def safe_agent_call(agent: BaseAgent, message: str) -> Optional[str]:
    """
    Safely call agent with proper error handling.
    
    Returns None if the call fails, logs the error for debugging.
    """
    try:
        response = await agent.process_message(message)
        return response
    except AgentTimeoutError:
        logger.warning(f"Agent {agent.id} timed out processing message")
        return None
    except AgentError as e:
        logger.error(f"Agent {agent.id} failed: {e}", exc_info=True)
        return None
    except Exception as e:
        logger.critical(f"Unexpected error calling agent {agent.id}: {e}", exc_info=True)
        return None

# FastAPI error handling
from fastapi import HTTPException, status

async def get_conversation(conversation_id: str) -> Conversation:
    """Get conversation with proper HTTP error handling."""
    try:
        conversation = await conversation_repository.get(conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found"
            )
        return conversation
    except ConversationError as e:
        logger.error(f"Failed to get conversation {conversation_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
```

---

## 📊 Logging Standards

### Logger Configuration
```python
import logging
import json
from datetime import datetime

# Configure structured logging
class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging."""
    
    def format(self, record):
        log_obj = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if hasattr(record, 'conversation_id'):
            log_obj['conversation_id'] = record.conversation_id
            
        if hasattr(record, 'agent_id'):
            log_obj['agent_id'] = record.agent_id
            
        return json.dumps(log_obj)

# Logger setup
def get_logger(name: str) -> logging.Logger:
    """Get configured logger for module."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
```

### Logging Best Practices
```python
logger = get_logger(__name__)

class ConversationManager:
    """Example of proper logging usage."""
    
    async def start_conversation(self, goal: str) -> str:
        """Start new conversation with structured logging."""
        conversation_id = generate_conversation_id()
        
        # Log conversation start
        logger.info(
            "Starting new conversation",
            extra={
                'conversation_id': conversation_id,
                'goal': goal,
                'agent_count': len(self.agents)
            }
        )
        
        try:
            result = await self._orchestrate_conversation(conversation_id, goal)
            
            # Log success
            logger.info(
                "Conversation completed successfully",
                extra={'conversation_id': conversation_id}
            )
            return result
            
        except Exception as e:
            # Log error with context
            logger.error(
                "Conversation failed",
                extra={
                    'conversation_id': conversation_id,
                    'error': str(e),
                    'goal': goal
                },
                exc_info=True
            )
            raise
```

---

## 🧪 Testing Standards

### Test File Structure
```python
"""
tests/test_conversation_manager.py

Test file naming: test_*.py
Test class naming: Test*
Test method naming: test_*
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from typing import List

from app.services.conversation_manager import ConversationManager
from app.models.message import Message, MessageType
from app.agents.base import BaseAgent

class TestConversationManager:
    """Test suite for ConversationManager."""
    
    @pytest.fixture
    def mock_agents(self) -> List[Mock]:
        """Create mock agents for testing."""
        agents = []
        for i in range(3):
            agent = Mock(spec=BaseAgent)
            agent.id = f"agent_{i}"
            agent.process_message = AsyncMock(return_value=f"Response from agent {i}")
            agents.append(agent)
        return agents
    
    @pytest.fixture
    def conversation_manager(self, mock_agents) -> ConversationManager:
        """Create ConversationManager instance for testing."""
        return ConversationManager(agents=mock_agents)
    
    @pytest.mark.asyncio
    async def test_start_conversation_success(self, conversation_manager):
        """Test successful conversation start."""
        # Arrange
        goal = "Design a mobile app"
        
        # Act
        result = await conversation_manager.start_conversation(goal)
        
        # Assert
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_agent_timeout_handling(self, conversation_manager, mock_agents):
        """Test proper handling of agent timeouts."""
        # Arrange
        mock_agents[0].process_message.side_effect = AgentTimeoutError("Timeout")
        goal = "Test timeout handling"
        
        # Act & Assert
        with pytest.raises(ConversationError):
            await conversation_manager.start_conversation(goal)
    
    @pytest.mark.parametrize("agent_count,expected_result", [
        (1, "single_agent_result"),
        (3, "multi_agent_result"),
        (5, "full_team_result")
    ])
    def test_different_agent_counts(self, agent_count, expected_result):
        """Test conversation with different numbers of agents."""
        # Parameterized test implementation
        pass
```

### Mock Usage Standards
```python
# ✅ Good - Proper mocking
@patch('app.services.llm_service.ollama_client')
async def test_llm_service_call(mock_ollama):
    """Test LLM service with mocked client."""
    # Arrange
    mock_ollama.generate.return_value = {"response": "Test response"}
    service = LLMService()
    
    # Act
    result = await service.generate_response("Test prompt")
    
    # Assert
    assert result == "Test response"
    mock_ollama.generate.assert_called_once_with("Test prompt")

# ✅ Good - Using pytest fixtures
@pytest.fixture
async def db_session():
    """Create test database session."""
    async with AsyncSession() as session:
        yield session
        await session.rollback()
```

---

## 🚀 Performance Standards

### Async/Await Best Practices
```python
# ✅ Good - Proper async usage
async def process_multiple_agents(agents: List[BaseAgent], message: str) -> List[str]:
    """Process message with multiple agents concurrently."""
    tasks = [agent.process_message(message) for agent in agents]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle exceptions in results
    responses = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.warning(f"Agent {agents[i].id} failed: {result}")
        else:
            responses.append(result)
    
    return responses

# ✅ Good - Context managers for resources
from contextlib import asynccontextmanager

@asynccontextmanager
async def database_transaction():
    """Manage database transaction with proper cleanup."""
    session = AsyncSession()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
```

### Memory Management
```python
from typing import Generator
import gc

def process_large_dataset(data: List[Dict]) -> Generator[Dict, None, None]:
    """Process large dataset with memory efficiency."""
    batch_size = 100
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        
        for item in batch:
            processed_item = process_item(item)
            yield processed_item
        
        # Explicit garbage collection for large datasets
        if i % 1000 == 0:
            gc.collect()
```

---

## ✅ Code Quality Checklist

### Before Committing Code
- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have type hints
- [ ] All classes and functions have docstrings
- [ ] Error handling is implemented properly
- [ ] Logging is added for important operations
- [ ] Tests are written and passing
- [ ] No hardcoded values (use configuration)
- [ ] Code is formatted with Black
- [ ] Imports are organized properly
- [ ] No unused imports or variables

### Code Review Checklist
- [ ] Code is readable and self-documenting
- [ ] Business logic is separated from infrastructure
- [ ] Error messages are user-friendly
- [ ] Performance considerations are addressed
- [ ] Security implications are considered
- [ ] Database queries are optimized
- [ ] Async operations are handled correctly
- [ ] Resource cleanup is implemented

---

## 🔧 Development Tools Configuration

### Black Configuration (pyproject.toml)
```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### Flake8 Configuration (.flake8)
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = .git,__pycache__,docs/source/conf.py,old,build,dist
```

### MyPy Configuration (mypy.ini)
```ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True
```

---

## 🎯 Enforcement

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
```

### CI/CD Pipeline
```yaml
# GitHub Actions example
name: Code Quality
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install black flake8 mypy pytest
        pip install -r requirements.txt
    
    - name: Run Black
      run: black --check .
    
    - name: Run Flake8
      run: flake8 .
    
    - name: Run MyPy
      run: mypy .
    
    - name: Run Tests
      run: pytest
```

---

## 📈 Continuous Improvement

### Code Metrics to Track
- Test coverage percentage (target: >90%)
- Cyclomatic complexity (target: <10 per function)
- Code duplication (target: <5%)
- Documentation coverage (target: 100% for public APIs)

### Regular Reviews
- Weekly code quality reviews
- Monthly architecture reviews
- Quarterly standards updates
- Annual tooling evaluations

---

**Remember:** These standards exist to improve code quality and team collaboration. When in doubt, prioritize readability and maintainability over cleverness.
