# Phase 3: OpenAI Agents SDK + MCP Integration - Implementation Summary

## Overview

This implementation integrates the **OpenAI Agents SDK** with **Model Context Protocol (MCP)** to create an AI-powered task management chatbot.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js + ChatKit)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP + JWT
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Chat API (chat_new.py)                                  │   │
│  │  - JWT validation                                        │   │
│  │  - Conversation management                               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Agent Service (agent_service_new.py)                    │   │
│  │  - Agent initialization                                  │   │
│  │  - Runner.run_async()                                    │   │
│  │  - MCP client connection                                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  MCP Server (mcp_server.py)                              │   │
│  │  - FastMCP with @mcp.tool() decorators                   │   │
│  │  - 5 task operation tools                                │   │
│  │  - Direct database access                                │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database (Neon)                    │
└────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. MCP Server (`src/mcp_server.py`)
- **Framework**: FastMCP
- **Transport**: stdio
- **Tools**:
  - `add_task(user_id, title, description)` - Create new task
  - `list_tasks(user_id, completed)` - List tasks with optional filter
  - `complete_task(user_id, task_id)` - Mark task as complete
  - `update_task(user_id, task_id, title, description)` - Update task
  - `delete_task(user_id, task_id)` - Delete task

### 2. Agent Service (`src/core/agent_service_new.py`)
- **SDK**: OpenAI Agents SDK
- **Components**:
  - `Agent` - Initialized with name, instructions, model
  - `Runner` - Executes agent with `run_async()`
  - `MCPClient` - Connects to MCP server via stdio
- **Features**:
  - Automatic MCP server startup
  - Context management with user_id
  - Result extraction from Agent execution

### 3. Chat API (`src/api/chat_new.py`)
- **Endpoints**:
  - `POST /api/{user_id}/chat` - Send message, get AI response
  - `GET /api/{user_id}/conversations` - List conversations
  - `GET /api/{user_id}/conversations/{id}` - Get conversation details
  - `DELETE /api/{user_id}/conversations/{id}` - Delete conversation
- **Integration**:
  - Uses `agent_service_mcp.run_agent()`
  - Extracts tool operations from Result
  - Persists messages to database

## Dependencies

### Required Packages
```toml
dependencies = [
    "openai-agents>=0.1.0",  # OpenAI Agents SDK
    "mcp[cli]>=1.2.0",       # Model Context Protocol with FastMCP
    "httpx>=0.27.0",         # HTTP client for MCP
    # ... existing dependencies
]
```

## Installation Steps

### 1. Install Dependencies
```bash
cd phase-3/backend
uv add "openai-agents>=0.1.0" "mcp[cli]>=1.2.0"
```

### 2. Update Environment Variables
Add to `.env`:
```env
# OpenRouter Configuration (already exists)
OPENROUTER_API_KEY=your-key-here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet

# Agent Configuration (already exists)
AGENT_NAME=TodoAssistant
AGENT_INSTRUCTIONS=You are a helpful AI assistant for managing todo tasks...
```

### 3. Replace Old Files
```bash
# Backup old files
mv src/core/agent_service.py src/core/agent_service_old.py
mv src/api/chat.py src/api/chat_old.py

# Use new files
mv src/core/agent_service_new.py src/core/agent_service.py
mv src/api/chat_new.py src/api/chat.py
```

### 4. Update Imports in Main App
In `src/main.py`, ensure the chat router is imported:
```python
from src.api.chat import router as chat_router
app.include_router(chat_router)
```

## Testing

### 1. Test MCP Server Standalone
```bash
cd phase-3/backend
python src/mcp_server.py
```

Expected: Server starts and listens on stdio

### 2. Test Backend API
```bash
cd phase-3/backend
uvicorn src.main:app --reload --port 8001
```

### 3. Test Frontend
```bash
cd phase-3/frontend
npm run dev
```

Navigate to `http://localhost:3000/chat` and test:
- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task 1 as complete"

## Key Differences from Previous Implementation

| Aspect | Old (Standard OpenAI) | New (Agents SDK + MCP) |
|--------|----------------------|------------------------|
| **Client** | `OpenAI()` client | `Agent` + `Runner` |
| **API Call** | `chat.completions.create()` | `Runner.run_async()` |
| **Tools** | Inline function calling | MCP server with `@mcp.tool()` |
| **Tool Execution** | Manual in chat.py | Automatic via MCP protocol |
| **Context** | Manual message array | Session-based context |
| **Result** | Raw API response | Structured `Result` object |

## Compliance with Hackathon Requirements

✅ **OpenAI Agents SDK**: Using `Agent`, `Runner`, and proper SDK patterns
✅ **MCP Protocol**: Separate MCP server with FastMCP
✅ **5 Task Tools**: All tools implemented with proper schemas
✅ **Stateless Architecture**: Database-persisted conversations
✅ **Natural Language**: AI interprets user intent and calls tools

## Next Steps

1. **Install dependencies** with `uv add`
2. **Replace old files** with new implementations
3. **Test MCP server** standalone
4. **Test full integration** with frontend
5. **Verify tool execution** in chat interface

## Troubleshooting

### Issue: "Module 'agents' not found"
**Solution**: Verify package name - might be `openai-agents` or check PyPI

### Issue: "MCP server not starting"
**Solution**: Check database connection in mcp_server.py

### Issue: "Agent not connecting to MCP"
**Solution**: Verify stdio transport and subprocess communication

### Issue: "Tools not executing"
**Solution**: Check user_id is passed correctly in context

## Files Created

1. `src/mcp_server.py` - MCP server with 5 task tools
2. `src/core/agent_service_new.py` - Agent SDK service layer
3. `src/api/chat_new.py` - Updated chat API
4. `pyproject.toml` - Updated dependencies

## Files to Replace

1. `src/core/agent_service.py` ← Replace with agent_service_new.py
2. `src/api/chat.py` ← Replace with chat_new.py
