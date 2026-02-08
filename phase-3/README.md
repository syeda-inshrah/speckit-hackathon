# Phase 3: AI-Powered Todo Chatbot (OpenRouter + OpenAI Agents SDK + ChatKit)

## Overview

Phase 3 adds AI-powered conversational task management using:
- **OpenRouter** - OpenAI-compatible API for accessing multiple LLM models
- **OpenAI Agents SDK** - Official SDK for building AI agents with tools
- **ChatKit** - Official OpenAI chat UI component
- **MCP (Model Context Protocol)** - Standardized tool protocol

## Architecture

### Backend Stack
- **FastAPI** - REST API framework
- **OpenRouter** - LLM API gateway (supports Claude, GPT-4, Llama, etc.)
- **OpenAI SDK** - For agent orchestration and function calling
- **PostgreSQL** - Database for conversations and messages
- **SQLModel** - ORM for database operations

### Frontend Stack
- **Next.js 16** - React framework
- **ChatKit** - Official OpenAI chat UI component
- **Tailwind CSS** - Styling
- **TypeScript** - Type safety

### Key Components

#### 1. Agent Service (`src/core/agent_service.py`)
- Manages OpenAI Agents SDK with OpenRouter
- Defines MCP tools using Pydantic schemas
- Handles agent execution and tool calling
- Supports multiple LLM models via OpenRouter

#### 2. MCP Tools
Five task operation tools:
- `add_task` - Create new tasks
- `list_tasks` - List tasks (with optional completion filter)
- `complete_task` - Mark tasks as completed
- `update_task` - Update task title/description
- `delete_task` - Delete tasks

#### 3. Chat API (`src/api/chat.py`)
- POST `/api/{user_id}/chat` - Send chat message
- GET `/api/{user_id}/conversations` - List conversations
- GET `/api/{user_id}/conversations/{id}` - Get conversation details
- DELETE `/api/{user_id}/conversations/{id}` - Delete conversation

#### 4. ChatKit Integration (`app/chat/page.tsx`)
- Official OpenAI chat UI component
- Connects to backend chat endpoint
- Displays AI responses and task operations
- Supports conversation history

## Setup Instructions

### Prerequisites
- Phase 2 must be fully implemented and working
- OpenRouter API key (get from https://openrouter.ai/keys)
- Node.js 18+ and Python 3.13+

### Backend Setup

1. **Navigate to Phase 3 backend**
   ```bash
   cd phase-3/backend
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**

   Edit `.env` file:
   ```env
   # OpenRouter Configuration
   OPENROUTER_API_KEY=your-openrouter-api-key-here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

   # OpenAI Agents SDK Configuration
   AGENT_NAME=TodoAssistant
   AGENT_INSTRUCTIONS=You are a helpful AI assistant for managing todo tasks.
   MAX_TOKENS=2000
   TEMPERATURE=0.7
   ```

   **Available Models:**
   - `anthropic/claude-3.5-sonnet` (Recommended)
   - `openai/gpt-4-turbo`
   - `anthropic/claude-3-opus`
   - `meta-llama/llama-3.1-70b-instruct`
   - `google/gemini-pro-1.5`

4. **Run database migrations**
   ```bash
   uv run alembic upgrade head
   ```

5. **Start backend server**
   ```bash
   .venv/Scripts/python.exe -m uvicorn src.main:app --reload --port 8001
   ```

   Backend will be available at: http://localhost:8001

### Frontend Setup

1. **Navigate to Phase 3 frontend**
   ```bash
   cd phase-3/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start frontend server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: http://localhost:3000

## Usage Guide

### Natural Language Commands

The AI assistant understands various natural language commands:

**Creating Tasks:**
- "Add a task to buy groceries"
- "Create a new task: finish the report"
- "I need to schedule a dentist appointment"
- "Remind me to call mom tomorrow"

**Listing Tasks:**
- "Show me all my tasks"
- "What tasks do I have?"
- "List my pending tasks"
- "Show completed tasks"
- "What's on my todo list?"

**Completing Tasks:**
- "Mark task 1 as complete"
- "Complete the grocery shopping task"
- "I finished task 3"
- "Done with task 5"

**Updating Tasks:**
- "Update task 2 title to 'Finish quarterly report'"
- "Change the description of task 1"
- "Edit task 5"
- "Rename task 3 to 'Buy milk'"

**Deleting Tasks:**
- "Delete task 3"
- "Remove the dentist appointment task"
- "Cancel task 7"
- "Get rid of task 2"

### ChatKit Features

1. **Starting a Conversation**
   - Click "AI Chat" button in dashboard navigation
   - Type your message in the input field
   - Press Enter or click Send

2. **Conversation Management**
   - Conversations are automatically saved
   - Navigate back to dashboard using "← Back to Dashboard"
   - View conversation history in the chat interface

3. **Task Operations**
   - AI will execute task operations automatically
   - You'll see confirmation messages for each action
   - Task changes are reflected immediately in the dashboard

## API Endpoints

### Chat Endpoints

#### Send Chat Message
```http
POST /api/{user_id}/chat
Authorization: Bearer {token}
Content-Type: application/json

{
  "message": "Add a task to buy groceries",
  "conversation_id": 1  // optional, omit for new conversation
}
```

**Response:**
```json
{
  "conversation_id": 1,
  "message": {
    "id": 2,
    "conversation_id": 1,
    "role": "assistant",
    "content": "I've created a new task for you: 'Buy groceries'",
    "created_at": "2026-01-27T10:30:00Z"
  },
  "task_operations": [
    {
      "operation": "add_task",
      "task_id": 5,
      "title": "Buy groceries",
      "description": null,
      "details": "Created task: Buy groceries"
    }
  ]
}
```

## OpenRouter Configuration

### Why OpenRouter?

OpenRouter provides:
- **Multiple Models**: Access to Claude, GPT-4, Llama, Gemini, and more
- **Cost Optimization**: Choose models based on cost/performance tradeoffs
- **Reliability**: Automatic fallback to alternative models
- **Unified API**: OpenAI-compatible API for all models
- **Transparent Pricing**: Pay-as-you-go with clear pricing

### Model Selection

**Recommended Models:**

1. **anthropic/claude-3.5-sonnet** (Default)
   - Best balance of quality and cost
   - Excellent at following instructions
   - Cost: ~$3 per million input tokens

2. **openai/gpt-4-turbo**
   - High quality responses
   - Good at complex reasoning
   - Cost: ~$10 per million input tokens

3. **meta-llama/llama-3.1-70b-instruct**
   - Open source model
   - Good performance
   - Cost: ~$0.50 per million input tokens

4. **anthropic/claude-3-opus**
   - Highest quality
   - Best for complex tasks
   - Cost: ~$15 per million input tokens

### Cost Estimation

**With Claude 3.5 Sonnet:**
- Average conversation: 500-1000 tokens
- Cost per conversation: $0.001-$0.003
- Monthly (100 users, 10 conversations each): $1-$3

**With GPT-4 Turbo:**
- Average conversation: 500-1000 tokens
- Cost per conversation: $0.005-$0.010
- Monthly (100 users, 10 conversations each): $5-$10

**With Llama 3.1 70B:**
- Average conversation: 500-1000 tokens
- Cost per conversation: $0.0002-$0.0005
- Monthly (100 users, 10 conversations each): $0.20-$0.50

## OpenAI Agents SDK

### Agent Architecture

The agent service uses the OpenAI SDK with:
- **Agent Instructions**: System prompt defining agent behavior
- **Tools**: MCP tools for task operations
- **Runner**: Executes agent with automatic tool calling
- **Session**: Maintains conversation context

### Tool Execution Flow

1. User sends message via ChatKit
2. Backend receives message and conversation history
3. Agent service runs agent with tools
4. Agent decides which tools to call (if any)
5. Tools are executed (task operations)
6. Agent generates final response
7. Response sent back to ChatKit

### Pydantic Tool Schemas

All tools use Pydantic schemas for validation:
```python
class AddTaskInput(BaseModel):
    title: str = Field(..., description="The title of the task")
    description: Optional[str] = Field(None, description="Optional description")
```

This ensures:
- Type safety
- Input validation
- Clear documentation
- JSON schema generation

## ChatKit Integration

### Features

- **Official Component**: Built by OpenAI team
- **Responsive Design**: Works on all screen sizes
- **Customizable Theme**: Match your brand colors
- **Streaming Support**: Real-time response streaming
- **Message History**: Automatic conversation persistence
- **Error Handling**: Built-in error states

### Configuration

```typescript
<ChatKit
  apiUrl={`http://localhost:8001/api/${userId}/chat`}
  headers={{
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  }}
  placeholder="Type your message..."
  welcomeMessage="👋 Hi! I'm your AI assistant..."
  theme={{
    primaryColor: '#2563eb',
    backgroundColor: '#ffffff',
    userMessageColor: '#2563eb',
    assistantMessageColor: '#f3f4f6',
  }}
/>
```

## Security

### API Key Protection
- OpenRouter API key stored in `.env` (not committed to git)
- Never expose API key in frontend code
- Use environment variables for all secrets

### Authentication
- JWT authentication required for all endpoints
- User-scoped conversations and tasks
- Token validation on every request

### Input Validation
- All user inputs validated on backend
- SQL injection protection via SQLModel
- XSS protection via React's built-in escaping
- Tool input validation via Pydantic schemas

### Prompt Injection Protection
- System prompt isolated from user input
- Function calling limits AI actions to defined tools
- All task operations require user authentication
- Rate limiting prevents abuse

## Performance

### Response Times
- **OpenRouter API**: 1-4 seconds typical (varies by model)
- **Database operations**: <100ms
- **Total chat response**: 1-4 seconds

### Optimization Tips
1. Use faster models for development (Llama 3.1)
2. Implement response caching for common queries
3. Add request debouncing to prevent duplicate calls
4. Monitor API usage and costs

## Troubleshooting

### Common Issues

**1. "Agent execution error: Invalid API key"**
- Check that OPENROUTER_API_KEY is set correctly in `.env`
- Verify API key is active at https://openrouter.ai/keys
- Ensure no extra spaces or quotes in the key

**2. "Failed to send message"**
- Check backend server is running on port 8001
- Verify database connection is working
- Check browser console for detailed error messages

**3. "Conversation not found"**
- Ensure conversation_id exists in database
- Check user authentication is working
- Verify user owns the conversation

**4. ChatKit not rendering**
- Check that @openai/chatkit is installed
- Verify ChatKit styles are imported
- Check browser console for errors

**5. Backend import errors**
- Ensure using Phase 3's virtual environment
- Run: `.venv/Scripts/python.exe -m uvicorn src.main:app --reload --port 8001`
- Verify openai package is installed in Phase 3's venv

## Testing

### Manual Testing Checklist

1. **Chat Interface**
   - [ ] Chat page loads successfully
   - [ ] Can send messages
   - [ ] Messages appear in chat history
   - [ ] Loading indicator shows while waiting for response
   - [ ] Error handling works for failed requests

2. **Task Operations**
   - [ ] Can create tasks via chat
   - [ ] Can list tasks via chat
   - [ ] Can complete tasks via chat
   - [ ] Can update tasks via chat
   - [ ] Can delete tasks via chat

3. **Conversation Management**
   - [ ] New conversations are created automatically
   - [ ] Conversation history persists across page refreshes
   - [ ] Can navigate back to dashboard

4. **Integration**
   - [ ] Task changes in chat reflect in dashboard
   - [ ] Dashboard tasks are accessible via chat
   - [ ] Authentication works correctly
   - [ ] Navigation between pages works

## Future Enhancements

### Phase 4 Potential Features
- Streaming responses for better UX
- Voice input/output support
- Multi-language support
- Conversation search functionality
- Message editing and deletion
- File attachment support
- Advanced analytics
- Mobile app integration
- Custom agent personalities
- Integration with calendar apps

## Support

For issues or questions:
1. Check this README for common solutions
2. Review the Phase 3 specification in `specs/003-ai-chatbot-todo/`
3. Check OpenRouter status at https://openrouter.ai/status
4. Review backend logs for detailed error messages

## License

This project is part of the Hackathon II - Todo Spec-Driven Development challenge.
