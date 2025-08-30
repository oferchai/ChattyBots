# ChattyBots 🤖💬

**Multi-Agent AI Conversation System**

ChattyBots is a sophisticated multi-agent AI chat system where teams of 3-5 AI agents with specialized roles collaborate to solve problems through structured conversations. The system enables intelligent discussions, user interactions, and consensus-building among AI agents.

## ✨ Features

### 🧠 **Multi-Agent Intelligence**
- **Specialized AI Agents**: Each agent has unique roles and personalities
- **Collaborative Problem Solving**: Agents work together to find optimal solutions  
- **Consensus Building**: Intelligent agreement mechanisms for decision making
- **Dynamic Conversations**: Real-time multi-agent discussions with threading

### 🔗 **Flexible LLM Integration**
- **Local LLMs**: Ollama integration for privacy-focused deployments
- **Cloud LLMs**: OpenRouter API support for advanced models
- **Hybrid Strategy**: Automatic fallback between local and cloud providers
- **Model Flexibility**: Easy switching between different LLM providers

### 👥 **Interactive User Experience**
- **Agent-User Interaction**: Agents can ask users questions during discussions
- **Real-time Updates**: WebSocket support for live conversation monitoring
- **Message Threading**: Organized conversation flows with reply chains
- **Conversation History**: Complete discussion archives and analysis

### 🏗️ **Production-Ready Architecture**
- **FastAPI Backend**: High-performance async API with automatic documentation
- **Database Support**: SQLite for development, PostgreSQL/MySQL for production
- **Environment Management**: Comprehensive configuration system with validation
- **Security Features**: CORS, rate limiting, production safety checks

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Conda or virtualenv
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd chatbot
   ```

2. **Set up Python environment**
   ```bash
   # Using conda (recommended)
   conda create -n chatbot python=3.11 -y
   conda activate chatbot
   
   # Install dependencies
   conda install -c conda-forge fastapi uvicorn sqlalchemy pydantic-settings -y
   ```

3. **Configure the application**
   ```bash
   # Copy development configuration
   cp .env.development .env
   
   # Edit configuration as needed
   vim .env
   ```

4. **Initialize the database**
   ```bash
   python -c "from backend.database import init_database; init_database()"
   ```

5. **Run the application**
   ```bash
   # Development server
   python -m backend.app.main
   
   # Or using uvicorn directly
   uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
   ```

6. **Access the application**
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health

## 🏛️ Architecture

### System Components

```
ChattyBots System Architecture

┌─────────────────────────────────────────────────────────────┐
│                    Frontend Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web UI    │  │  Mobile App │  │  API Integrations   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     API Layer                               │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │            FastAPI Application                          │ │
│  │  • REST API Endpoints     • WebSocket Handlers         │ │
│  │  • Authentication         • Real-time Updates          │ │
│  │  • Rate Limiting          • Error Handling             │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Business Logic Layer                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Agents    │  │Conversation │  │   Decision Engine   │  │
│  │  Manager    │  │   Engine    │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     LLM Integration Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Ollama    │  │ OpenRouter  │  │   Future LLMs       │  │
│  │   (Local)   │  │  (Cloud)    │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   SQLite    │  │ PostgreSQL  │  │      Caching        │  │
│  │    (Dev)    │  │   (Prod)    │  │                     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Agent System

**Built-in AI Agents:**
- **🎯 Project Manager**: Coordination and planning specialist
- **💡 Creative Thinker**: Innovation and brainstorming expert  
- **📊 Analyst**: Data analysis and logical reasoning
- **🔧 Technical Expert**: Implementation and technical solutions
- **👥 User Advocate**: User experience and accessibility focus

## 🛠️ Development

### Project Structure

```
chatbot/
├── backend/                    # Backend application
│   ├── app/                   # FastAPI application
│   │   ├── main.py           # Application entry point
│   │   ├── api/              # API routes
│   │   └── middleware/       # Custom middleware
│   ├── database/             # Database models and setup
│   │   ├── models/           # SQLAlchemy models
│   │   └── __init__.py       # Database initialization
│   ├── agents/               # Agent configuration
│   │   └── config.py         # Agent definitions
│   └── config.py             # Configuration management
├── tests/                     # Test suites
│   ├── test_config.py        # Configuration tests
│   └── test_config_suite.sh  # Automated test suite
├── docs/                     # Documentation
│   ├── CONFIG_README.md      # Configuration guide
│   └── CONFIG_TEST_SUITE.md  # Test suite documentation
├── .env.development          # Development configuration
├── .env.testing              # Testing configuration
├── .env.production.template  # Production template
└── README.md                 # This file
```

### Configuration Management

ChattyBots features a comprehensive configuration system:

```python
from backend.config import get_settings

settings = get_settings()

# Access nested configuration
print(f"Environment: {settings.environment.value}")
print(f"Database: {settings.database.url}")
print(f"LLM Provider: {settings.llm.provider.value}")
```

**Environment-Specific Configs:**
- **Development**: Debug mode, verbose logging, auto-reload
- **Testing**: Fast settings, in-memory database, minimal output
- **Production**: Security hardened, external database, SSL support

### Testing

**Run Configuration Tests:**
```bash
# Manual testing
python test_config.py

# Comprehensive automated test suite
./test_config_suite.sh

# Test specific environment
python test_config.py testing
```

**Test Results:**
- ✅ **18 comprehensive tests** with 100% pass rate
- 🧪 **Core functionality**, validation, environment, and utility tests
- 📊 **Detailed reporting** with statistics and error detection

### Database Models

**Core Data Models:**
```python
# Conversation management
class Conversation(Base):
    id: UUID
    title: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime

# Message threading
class Message(Base):
    id: UUID
    conversation_id: UUID
    content: str
    sender_type: SenderType
    sender_id: str
    parent_message_id: Optional[UUID]
```

**Agent Configuration:**
```python
# Static agent definitions
AGENTS = {
    "project_manager": {
        "name": "Alex",
        "role": "Project Manager", 
        "personality": "Organized and strategic leader...",
        "capabilities": ["planning", "coordination", "risk_assessment"]
    },
    # ... more agents
}
```

## 🔧 Configuration

### Environment Variables

Configure ChattyBots using environment variables with nested structure:

```bash
# Application
ENVIRONMENT=development
DEBUG=true
APP_NAME="ChattyBots"

# Database  
DATABASE__URL="sqlite:///./data/chatbot.db"
DATABASE__POOL_SIZE=5

# LLM Configuration
LLM__PROVIDER=ollama
LLM__OLLAMA__BASE_URL="http://localhost:11434"
LLM__OPENROUTER__API_KEY="your_api_key_here"

# Agent Behavior
AGENTS__MAX_CONVERSATION_ROUNDS=20
AGENTS__CONSENSUS_THRESHOLD=0.8
AGENTS__RESPONSE_TIMEOUT=30

# Security
SECURITY__SECRET_KEY="your-secret-key"
SECURITY__RATE_LIMIT_PER_MINUTE=100
```

### LLM Setup

**Ollama (Local):**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama

# Configure in .env
LLM__OLLAMA__MODEL=llama2
```

**OpenRouter (Cloud):**
```bash
# Get API key from https://openrouter.ai
# Configure in .env
LLM__OPENROUTER__API_KEY=your_api_key_here
LLM__OPENROUTER__MODEL=anthropic/claude-3-haiku
```

## 📚 API Documentation

### Core Endpoints

**Conversations:**
- `POST /api/v1/conversations` - Create new conversation
- `GET /api/v1/conversations` - List conversations  
- `GET /api/v1/conversations/{id}` - Get conversation details
- `PUT /api/v1/conversations/{id}` - Update conversation

**Messages:**
- `POST /api/v1/conversations/{id}/messages` - Send message
- `GET /api/v1/conversations/{id}/messages` - Get messages
- `GET /api/v1/messages/pending` - Get pending agent responses

**Agents:**
- `GET /api/v1/agents` - List available agents
- `GET /api/v1/agents/{id}` - Get agent details

**System:**
- `GET /health` - Health check
- `GET /api/v1/status` - Detailed system status
- `GET /api/v1/config` - Public configuration

### WebSocket Support

```javascript
// Real-time conversation updates
const ws = new WebSocket('ws://localhost:8000/ws/conversations/{id}');

ws.onmessage = function(event) {
    const update = JSON.parse(event.data);
    console.log('New message:', update);
};
```

## 🚀 Deployment

### Development
```bash
# Local development server
python -m backend.app.main

# With auto-reload
uvicorn backend.app.main:app --reload
```

### Production

**Docker Deployment:**
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "-m", "backend.app.main"]
```

**Environment Setup:**
```bash
# Copy and configure production settings
cp .env.production.template .env.production
vim .env.production

# Set environment
export ENVIRONMENT=production

# Run with production settings
python -m backend.app.main
```

## 🤝 Contributing

We welcome contributions to ChattyBots! Please see our contributing guidelines:

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `./test_config_suite.sh`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include comprehensive docstrings
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** for local LLM integration
- **OpenRouter** for cloud LLM access
- **FastAPI** for the excellent web framework
- **Pydantic** for data validation and configuration
- **SQLAlchemy** for database ORM

## 📞 Support

- **Documentation**: [Full documentation](docs/)
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)

---

**ChattyBots** - Where AI agents collaborate to solve problems! 🤖✨

*Built with ❤️ using Python, FastAPI, and modern AI technologies*
