# Multi-Agent AI Chat System - Backend API

A FastAPI backend for coordinating multiple AI agents in collaborative problem-solving conversations.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Conda environment (recommended)

### Setup
1. **Activate the conda environment:**
   ```bash
   conda activate chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Start the server:**
   ```bash
   # From the root directory
   python run_server.py
   ```

4. **Access the API:**
   - Server: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📡 API Endpoints

### System Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/status` - System status with database and agent info

### Agent Endpoints
- `GET /api/agents` - List all available AI agents
- `GET /api/agents/{agent_id}` - Get specific agent details

### Conversation Endpoints
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations` - List conversations (with pagination)
- `GET /api/conversations/{id}` - Get conversation details
- `PUT /api/conversations/{id}` - Update conversation status
- `DELETE /api/conversations/{id}` - Delete conversation

### Message Endpoints
- `POST /api/conversations/{id}/messages` - Send message
- `GET /api/conversations/{id}/messages` - Get conversation messages
- `GET /api/conversations/{id}/messages/pending` - Get messages requiring user response

### WebSocket Endpoints
- `WebSocket /ws/conversations/{id}` - Real-time conversation updates

## 🤖 Available AI Agents

The system includes 5 specialized AI agents:

1. **Alex PM** (Project Manager)
   - Role: Facilitates discussion, manages flow
   - Personality: Diplomatic, organized, goal-oriented

2. **Sam Tech** (Technical Architect)
   - Role: Evaluates technical feasibility
   - Personality: Analytical, detail-oriented, innovative

3. **Jordan Creative** (Creative Strategist)
   - Role: Generates innovative ideas
   - Personality: Imaginative, optimistic, unconventional

4. **Casey QA** (Quality Assurance)
   - Role: Identifies risks and validates quality
   - Personality: Cautious, thorough, detail-focused

5. **Riley Resource** (Resource Coordinator)
   - Role: Manages constraints and practical implementation
   - Personality: Practical, realistic, efficient

## 💾 Database

- **Engine**: SQLite (development) / PostgreSQL (production)
- **ORM**: SQLAlchemy with async support
- **Models**: Conversation, Message
- **Features**: UUID primary keys, timestamps, foreign key constraints

### Database Schema
```sql
conversations:
  - id (UUID, Primary Key)
  - goal_description (Text)
  - status (Enum: active, paused, completed)
  - created_at, updated_at (DateTime)
  - final_summary (Text, nullable)

messages:
  - id (UUID, Primary Key)
  - conversation_id (UUID, Foreign Key)
  - sender_type (Enum: agent, user)
  - sender_id (String)
  - content (Text)
  - message_type (Enum: discussion, question_to_user, user_response)
  - parent_message_id (UUID, nullable)
  - requires_user_response (Boolean)
  - created_at (DateTime)
```

## 🔄 Conversation Flow

1. **Create Conversation**: User defines a goal/problem
2. **Agent Discussion**: Agents collaborate to understand and solve
3. **User Interaction**: Agents can ask users for clarification
4. **Status Management**: Conversations can be active, paused, or completed

## 🌐 Real-time Features

### WebSocket Communication
- Real-time message updates
- Conversation status changes
- Agent activity indicators
- Connection management per conversation

### Example WebSocket Messages
```javascript
// Connection established
{"type": "connection_established", "conversation_id": "...", "message": "Connected"}

// New message
{"type": "new_message", "conversation_id": "...", "data": {...}}

// Status change
{"type": "status_change", "conversation_id": "...", "new_status": "paused"}

// Agent activity
{"type": "agent_activity", "conversation_id": "...", "agent_id": "...", "activity": "typing"}
```

## 🧪 Testing

### Manual Testing
```bash
# Start the server
python run_server.py

# In another terminal, test the API
python test_api_manual.py
```

### Model Testing
```bash
# Test database models and agent configuration
python test_models.py
```

## 🏗️ Architecture

```
app/
├── main.py              # FastAPI application
├── schemas.py           # Pydantic request/response schemas
├── models/              # SQLAlchemy database models
│   ├── base.py         # Base model with common fields
│   ├── conversation.py # Conversation model
│   └── message.py      # Message model
├── agents/              # Static agent configurations
│   ├── config.py       # Agent definitions and prompts
│   └── __init__.py     # Agent utilities
├── db/                  # Database configuration
│   ├── database.py     # SQLAlchemy setup and session management
│   └── __init__.py     # Database utilities
├── api/                 # FastAPI route handlers
│   ├── conversations.py # Conversation endpoints
│   ├── agents.py       # Agent endpoints
│   ├── websockets.py   # WebSocket handlers
│   └── __init__.py     # API package
└── middleware/          # Custom middleware
    ├── logging.py      # Request logging
    ├── error_handler.py # Error handling
    └── __init__.py     # Middleware package
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=sqlite:///./data/chatbot.db

# Logging
DEBUG=true
LOG_LEVEL=INFO

# Server
HOST=localhost
PORT=8000
```

### Agent Configuration
Agents are configured statically in `app/agents/config.py` with:
- Name and role
- System prompts for LLM interaction
- Personality traits
- Expertise areas

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls

#### Create Conversation
```bash
curl -X POST "http://localhost:8000/api/conversations" \
  -H "Content-Type: application/json" \
  -d '{"goal_description": "Design a mobile banking app"}'
```

#### Send Message
```bash
curl -X POST "http://localhost:8000/api/conversations/{id}/messages" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_type": "user",
    "sender_id": "user",
    "content": "What features should it have?",
    "message_type": "user_response"
  }'
```

#### List Agents
```bash
curl "http://localhost:8000/api/agents"
```

## 🚧 Development

### Adding New Endpoints
1. Create route handler in appropriate `api/` module
2. Define Pydantic schemas in `schemas.py`
3. Add any new database models in `models/`
4. Update API documentation

### Database Migrations
```python
# Initialize database
from app.db import init_database
init_database()

# Reset database (development only)
from app.db import reset_database
reset_database()
```

### Logging
The application uses structured JSON logging:
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Message", extra={
    "conversation_id": "...",
    "agent_id": "...",
    "custom_field": "value"
})
```

## 🔐 Security Considerations

- Input validation via Pydantic schemas
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend integration
- Request ID tracking for security auditing
- Structured error responses (no sensitive data leakage)

## 🚀 Production Deployment

### Docker Support (Future)
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Setup
- Use PostgreSQL for production database
- Configure proper logging aggregation
- Set up monitoring and health checks
- Use environment-based configuration
