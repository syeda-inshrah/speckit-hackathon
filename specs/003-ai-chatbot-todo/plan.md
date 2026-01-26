# Phase III: AI-Powered Todo Chatbot - Implementation Plan

## 1. Executive Summary

This document outlines the technical implementation plan for Phase III of the Todo application, transforming the existing web interface into an AI-powered conversational chatbot using OpenAI Agents SDK and Model Context Protocol (MCP).

**Key Architectural Decisions:**
- Stateless server architecture with database-persisted conversation state
- MCP server pattern for standardized AI-to-application communication
- OpenAI Agents SDK for natural language understanding
- Existing Phase II infrastructure reuse (auth, database, task operations)

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                 │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  OpenAI ChatKit UI (Next.js Frontend)                        │   │
│  │  - Chat interface component                                  │   │
│  │  - Message history display                                   │   │
│  │  - Authentication integration                                │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS + JWT
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      FASTAPI SERVER LAYER                            │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Chat API Endpoint                                           │   │
│  │  POST /api/{user_id}/chat                                    │   │
│  │  - JWT validation                                            │   │
│  │  - Conversation history loading                              │   │
│  │  - Message persistence                                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                    │                                 │
│                                    ▼                                 │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  OpenAI Agents SDK Integration                               │   │
│  │  - Agent initialization                                      │   │
│  │  - Message array construction                                │   │
│  │  - Tool registration                                         │   │
│  │  - Response generation                                       │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                    │                                 │
│                                    ▼                                 │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  MCP Server (Model Context Protocol)                         │   │
│  │  - add_task tool                                             │   │
│  │  - list_tasks tool                                           │   │
│  │  - complete_task tool                                        │   │
│  │  - update_task tool                                          │   │
│  │  - delete_task tool                                          │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │  Neon PostgreSQL (Existing + New Tables)                     │   │
│  │  - users (existing)                                          │   │
│  │  - tasks (existing)                                          │   │
│  │  - conversations (new)                                       │   │
│  │  - messages (new)                                            │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Responsibilities

| Component | Responsibility | Stateful? |
|-----------|---------------|-----------|
| **ChatKit UI** | User interface, message display, input handling | No (React state only) |
| **Chat API** | Request routing, auth validation, orchestration | No (stateless) |
| **Agents SDK** | NLP, intent recognition, tool selection | No (per-request) |
| **MCP Server** | Task operations, business logic execution | No (stateless) |
| **Database** | Persistent storage for all state | Yes (source of truth) |

---

## 3. Technology Stack

### 3.1 Frontend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 16+ | React framework |
| OpenAI ChatKit | Latest | Chat UI component |
| TypeScript | 5+ | Type safety |
| Tailwind CSS | 3+ | Styling |
| Axios | Latest | HTTP client |

### 3.2 Backend Stack
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.13+ | Runtime |
| FastAPI | Latest | Web framework |
| OpenAI Agents SDK | Latest | AI agent framework |
| Official MCP SDK | Latest | Tool protocol |
| SQLModel | Latest | ORM |
| Pydantic | Latest | Data validation |
| python-jose | Latest | JWT handling |

### 3.3 Infrastructure
| Service | Purpose |
|---------|---------|
| Neon PostgreSQL | Database |
| OpenAI API | LLM inference |
| Vercel | Frontend hosting |
| Railway/Render | Backend hosting (optional) |

---

## 4. Database Design

### 4.1 New Tables

**conversations**
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

**messages**
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_user_id ON messages(user_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

### 4.2 SQLModel Models

**Conversation Model**
```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID
from typing import Optional, List

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    messages: List["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")
```

**Message Model**
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True, nullable=False)
    user_id: UUID = Field(foreign_key="users.id", index=True, nullable=False)
    role: str = Field(max_length=20, nullable=False)  # 'user' or 'assistant'
    content: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=False)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    user: "User" = Relationship()
```

### 4.3 Migration Strategy
1. Create migration script using Alembic
2. Test migration on development database
3. Backup production database
4. Run migration on production
5. Verify data integrity

---

## 5. API Design

### 5.1 Chat Endpoint Specification

**Endpoint:** `POST /api/{user_id}/chat`

**Request Schema (Pydantic)**
```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    conversation_id: Optional[int] = Field(None, description="Existing conversation ID")
    message: str = Field(..., min_length=1, max_length=2000, description="User message")

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 123,
                "message": "Add a task to buy groceries"
            }
        }
```

**Response Schema**
```python
class ChatResponse(BaseModel):
    conversation_id: int = Field(..., description="Conversation ID")
    response: str = Field(..., description="AI assistant response")
    tool_calls: List[str] = Field(default=[], description="Tools invoked")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 123,
                "response": "I've added 'Buy groceries' to your task list.",
                "tool_calls": ["add_task"],
                "timestamp": "2026-01-25T18:30:00Z"
            }
        }
```

### 5.2 Request Flow

```python
@router.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # 1. Validate user_id matches authenticated user
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    # 2. Get or create conversation
    conversation = await get_or_create_conversation(
        session, request.conversation_id, current_user.id
    )

    # 3. Load conversation history
    history = await load_conversation_history(session, conversation.id)

    # 4. Store user message
    await store_message(session, conversation.id, current_user.id, "user", request.message)

    # 5. Build message array for agent
    messages = build_message_array(history, request.message)

    # 6. Call OpenAI Agents SDK
    agent_response = await run_agent(messages, current_user.id)

    # 7. Store assistant response
    await store_message(
        session, conversation.id, current_user.id, "assistant", agent_response.content
    )

    # 8. Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=agent_response.content,
        tool_calls=agent_response.tool_calls,
        timestamp=datetime.utcnow()
    )
```

---

## 6. OpenAI Agents SDK Integration

### 6.1 Agent Configuration

```python
from openai import OpenAI
from openai.agents import Agent

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Define system prompt
SYSTEM_PROMPT = """
You are a helpful task management assistant. You help users manage their todo list through natural conversation.

Your capabilities:
- Create new tasks (add_task)
- List tasks with filtering (list_tasks)
- Mark tasks as complete (complete_task)
- Update task details (update_task)
- Delete tasks (delete_task)

Guidelines:
- Be friendly and conversational
- Confirm actions before executing
- Ask for clarification when commands are ambiguous
- Provide helpful error messages
- Use the user's language and tone

When a user asks to do something with their tasks, use the appropriate tool and provide a natural language confirmation.
"""

# Create agent
agent = Agent(
    name="todo_assistant",
    instructions=SYSTEM_PROMPT,
    model="gpt-4",
    tools=[
        add_task_tool,
        list_tasks_tool,
        complete_task_tool,
        update_task_tool,
        delete_task_tool
    ]
)
```

### 6.2 Message Array Construction

```python
def build_message_array(history: List[Message], new_message: str) -> List[dict]:
    """
    Build message array for OpenAI Agents SDK.

    Args:
        history: Previous messages from database
        new_message: Current user message

    Returns:
        List of message dicts in OpenAI format
    """
    messages = []

    # Add conversation history
    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    # Add new user message
    messages.append({
        "role": "user",
        "content": new_message
    })

    return messages
```

### 6.3 Agent Execution

```python
async def run_agent(messages: List[dict], user_id: str) -> AgentResponse:
    """
    Execute agent with message history.

    Args:
        messages: Message array
        user_id: Current user ID (passed to tools)

    Returns:
        Agent response with content and tool calls
    """
    try:
        # Create thread
        thread = client.beta.threads.create()

        # Add messages to thread
        for msg in messages:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role=msg["role"],
                content=msg["content"]
            )

        # Run agent
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=agent.id,
            additional_instructions=f"User ID: {user_id}"
        )

        # Wait for completion
        while run.status in ["queued", "in_progress"]:
            await asyncio.sleep(0.5)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Get response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        latest_message = messages.data[0]

        return AgentResponse(
            content=latest_message.content[0].text.value,
            tool_calls=[step.tool_calls for step in run.steps if step.tool_calls]
        )

    except Exception as e:
        logger.error(f"Agent execution failed: {e}")
        raise HTTPException(status_code=500, detail="AI processing failed")
```

---

## 7. MCP Server Implementation

### 7.1 MCP Server Structure

```python
from mcp import Server, Tool
from mcp.server.stdio import stdio_server

# Initialize MCP server
mcp_server = Server("todo-mcp-server")

# Tool definitions
@mcp_server.tool()
async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Create a new task for the user."""
    # Implementation
    pass

@mcp_server.tool()
async def list_tasks(user_id: str, status: str = "all") -> dict:
    """List user's tasks with optional filtering."""
    # Implementation
    pass

@mcp_server.tool()
async def complete_task(user_id: str, task_id: int) -> dict:
    """Mark a task as complete."""
    # Implementation
    pass

@mcp_server.tool()
async def update_task(
    user_id: str,
    task_id: int,
    title: str = None,
    description: str = None
) -> dict:
    """Update task details."""
    # Implementation
    pass

@mcp_server.tool()
async def delete_task(user_id: str, task_id: int) -> dict:
    """Delete a task."""
    # Implementation
    pass
```

### 7.2 Tool Implementation Pattern

```python
@mcp_server.tool()
async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """
    Create a new task for the user.

    Args:
        user_id: User ID from authentication
        title: Task title (1-200 characters)
        description: Optional task description (max 1000 characters)

    Returns:
        {
            "task_id": int,
            "status": "created",
            "title": str
        }
    """
    # Validate inputs
    if not title or len(title) > 200:
        return {
            "error": "Title must be 1-200 characters",
            "status": "error"
        }

    if description and len(description) > 1000:
        return {
            "error": "Description must be max 1000 characters",
            "status": "error"
        }

    # Get database session
    async with get_async_session() as session:
        try:
            # Create task
            new_task = Task(
                user_id=UUID(user_id),
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False
            )

            session.add(new_task)
            await session.commit()
            await session.refresh(new_task)

            return {
                "task_id": new_task.id,
                "status": "created",
                "title": new_task.title
            }

        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            await session.rollback()
            return {
                "error": "Failed to create task",
                "status": "error"
            }
```

### 7.3 Tool Registration with Agent

```python
# Convert MCP tools to OpenAI function format
def mcp_tool_to_openai_function(tool: Tool) -> dict:
    """Convert MCP tool to OpenAI function definition."""
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": tool.parameters,
                "required": tool.required_parameters
            }
        }
    }

# Register tools with agent
tools = [
    mcp_tool_to_openai_function(add_task),
    mcp_tool_to_openai_function(list_tasks),
    mcp_tool_to_openai_function(complete_task),
    mcp_tool_to_openai_function(update_task),
    mcp_tool_to_openai_function(delete_task)
]
```

---

## 8. Frontend Implementation

### 8.1 ChatKit Integration

```typescript
// app/chat/page.tsx
'use client';

import { ChatKit } from '@openai/chatkit';
import { useState, useEffect } from 'react';
import { useAuth } from '@/lib/auth';
import { chatApi } from '@/lib/api-client';

export default function ChatPage() {
  const { user, token } = useAuth();
  const [conversationId, setConversationId] = useState<number | null>(null);

  const handleSendMessage = async (message: string) => {
    try {
      const response = await chatApi.sendMessage({
        conversation_id: conversationId,
        message: message,
        token: token
      });

      setConversationId(response.conversation_id);
      return response.response;
    } catch (error) {
      console.error('Failed to send message:', error);
      throw error;
    }
  };

  return (
    <div className="h-screen">
      <ChatKit
        apiKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY}
        onSendMessage={handleSendMessage}
        placeholder="Ask me to manage your tasks..."
        theme="light"
      />
    </div>
  );
}
```

### 8.2 API Client

```typescript
// lib/api-client.ts
import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

export const chatApi = {
  sendMessage: async (data: {
    conversation_id: number | null;
    message: string;
    token: string;
  }) => {
    const response = await axios.post(
      `${API_BASE_URL}/api/${getUserId()}/chat`,
      {
        conversation_id: data.conversation_id,
        message: data.message
      },
      {
        headers: {
          'Authorization': `Bearer ${data.token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return response.data;
  },

  getConversationHistory: async (conversationId: number, token: string) => {
    const response = await axios.get(
      `${API_BASE_URL}/api/${getUserId()}/conversations/${conversationId}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );
    return response.data;
  }
};
```

---

## 9. Security Considerations

### 9.1 Authentication & Authorization
- All chat endpoints require valid JWT token
- User ID in URL must match authenticated user
- Conversation access restricted to owner
- Message access restricted to conversation participants

### 9.2 Input Validation
- Message length limits (1-2000 characters)
- SQL injection prevention via SQLModel ORM
- XSS prevention via content sanitization
- Rate limiting (10 requests/minute per user)

### 9.3 Data Privacy
- User isolation at database level
- No cross-user data leakage
- Conversation history encrypted at rest
- Secure token storage

---

## 10. Performance Optimization

### 10.1 Database Optimization
- Indexes on frequently queried columns
- Connection pooling
- Query optimization
- Pagination for large conversation histories

### 10.2 API Optimization
- Response caching where appropriate
- Async/await for non-blocking operations
- Timeout handling for OpenAI API calls
- Retry logic with exponential backoff

### 10.3 Frontend Optimization
- Lazy loading of conversation history
- Optimistic UI updates
- Message streaming (future enhancement)
- Client-side caching

---

## 11. Error Handling Strategy

### 11.1 Error Categories

| Error Type | HTTP Code | User Message | Action |
|------------|-----------|--------------|--------|
| Invalid input | 400 | "Please provide a valid message" | Show error in UI |
| Unauthorized | 401 | "Please sign in to continue" | Redirect to login |
| Forbidden | 403 | "You don't have access to this conversation" | Show error |
| Not found | 404 | "Conversation not found" | Create new conversation |
| Rate limit | 429 | "Too many requests. Please wait." | Show cooldown timer |
| OpenAI API error | 500 | "AI service temporarily unavailable" | Retry button |
| Database error | 500 | "Something went wrong. Please try again." | Log error, retry |

### 11.2 Error Response Format

```python
class ErrorResponse(BaseModel):
    error: str
    code: str
    details: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

## 12. Testing Strategy

### 12.1 Unit Tests
- MCP tool functions
- Database models and operations
- Message parsing and validation
- Authentication helpers

### 12.2 Integration Tests
- Chat endpoint with mocked OpenAI API
- MCP server tool execution
- Database transactions
- Authentication flow

### 12.3 End-to-End Tests
- Complete conversation flows
- Multi-turn conversations
- Error scenarios
- Conversation persistence across sessions

---

## 13. Deployment Plan

### 13.1 Pre-Deployment Checklist
- [ ] Better Auth implemented and tested
- [ ] Database migrations created and tested
- [ ] Environment variables configured
- [ ] OpenAI API key obtained
- [ ] ChatKit domain allowlist configured
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed (optional)
- [ ] SSL certificates configured
- [ ] Monitoring and logging set up

### 13.2 Deployment Steps
1. Run database migrations
2. Deploy backend (if hosting separately)
3. Deploy frontend to Vercel
4. Configure domain allowlist with production URL
5. Update environment variables
6. Test end-to-end flow
7. Monitor for errors

### 13.3 Rollback Plan
- Keep previous deployment active
- Database migration rollback script ready
- Quick switch to previous version if issues arise

---

## 14. Monitoring & Observability

### 14.1 Metrics to Track
- Chat endpoint response time
- OpenAI API latency
- Error rates by type
- Conversation creation rate
- Message volume per user
- Tool invocation frequency

### 14.2 Logging Strategy
- Structured logging (JSON format)
- Log levels: DEBUG, INFO, WARNING, ERROR
- Sensitive data redaction
- Request/response logging (excluding message content)

### 14.3 Alerting
- High error rate (>5% of requests)
- Slow response time (>5 seconds)
- OpenAI API failures
- Database connection issues

---

## 15. Implementation Timeline

### Phase 1: Foundation (Week 1)
- [ ] Implement Better Auth (if not done)
- [ ] Create database models (Conversation, Message)
- [ ] Write and test database migrations
- [ ] Set up OpenAI API integration

### Phase 2: Backend Core (Week 2)
- [ ] Implement chat API endpoint
- [ ] Build MCP server with 5 tools
- [ ] Integrate OpenAI Agents SDK
- [ ] Implement conversation state management

### Phase 3: Frontend Integration (Week 3)
- [ ] Integrate OpenAI ChatKit
- [ ] Build chat UI components
- [ ] Implement API client
- [ ] Add authentication flow

### Phase 4: Testing & Polish (Week 4)
- [ ] Write unit and integration tests
- [ ] Perform end-to-end testing
- [ ] Fix bugs and edge cases
- [ ] Optimize performance

### Phase 5: Deployment (Week 5)
- [ ] Deploy to production
- [ ] Configure domain allowlist
- [ ] Monitor and fix issues
- [ ] Create demo video

---

## 16. Success Metrics

### 16.1 Technical Metrics
- Response time < 3 seconds (95th percentile)
- Error rate < 1%
- Uptime > 99%
- Database query time < 100ms

### 16.2 Functional Metrics
- All 5 MCP tools working correctly
- Natural language commands understood (>90% accuracy)
- Conversation persistence working
- Multi-turn conversations supported

### 16.3 User Experience Metrics
- Clear and helpful AI responses
- Smooth conversation flow
- Intuitive UI
- Fast and responsive interface

---

## 17. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| OpenAI API rate limits | High | Medium | Implement caching, rate limiting, fallback messages |
| Better Auth not implemented | High | High | Prioritize implementation before Phase III |
| MCP SDK learning curve | Medium | High | Study docs, start with simple tools, iterate |
| ChatKit integration issues | Medium | Medium | Test early, follow documentation closely |
| Performance issues | Medium | Low | Optimize queries, implement caching, load testing |

---

## 18. Future Enhancements

### 18.1 Phase IV Considerations
- Kubernetes deployment preparation
- Containerization strategy
- Scalability improvements
- Monitoring and observability

### 18.2 Potential Features
- Voice input/output
- Multi-language support
- Advanced NLP capabilities
- Task scheduling and reminders
- Collaborative features
- Analytics dashboard

---

**Document Version:** 1.0
**Last Updated:** January 25, 2026
**Author:** Technical Architecture Team
**Status:** Ready for Implementation
