# Phase III: AI-Powered Todo Chatbot - Specification

## 1. Overview

### 1.1 Purpose
Transform the existing web-based todo application into an AI-powered conversational interface that allows users to manage their tasks through natural language using OpenAI Agents SDK and Model Context Protocol (MCP).

### 1.2 Objectives
- Implement a conversational AI interface using OpenAI ChatKit
- Build an MCP server that exposes task operations as standardized tools
- Enable natural language task management (add, update, delete, complete, list tasks)
- Maintain stateless server architecture with database-persisted conversation state
- Integrate with existing Phase II authentication and task management system

### 1.3 Scope
**In Scope:**
- OpenAI ChatKit frontend integration
- Chat API endpoint for conversational interactions
- OpenAI Agents SDK integration
- MCP server with 5 task management tools
- Conversation and message persistence
- Natural language understanding for task commands
- Stateless request/response architecture

**Out of Scope:**
- Voice input/output
- Multi-language support (Phase V bonus)
- Advanced NLP features beyond basic task management
- Real-time collaborative features
- Mobile app interface

### 1.4 Success Criteria
- Users can manage all 5 basic task operations through natural language
- Conversation history persists across sessions
- Server remains stateless (horizontally scalable)
- AI agent correctly interprets and executes task commands
- Graceful error handling and user feedback
- Response time < 3 seconds for typical interactions

---

## 2. User Stories

### 2.1 Core User Stories

**US-1: Natural Language Task Creation**
- **As a** user
- **I want to** create tasks by describing them in natural language
- **So that** I can quickly add tasks without filling forms

**Acceptance Criteria:**
- User can say "Add a task to buy groceries" and task is created
- User can include descriptions: "Remind me to call mom tomorrow about dinner plans"
- System confirms task creation with task ID and title
- Task is associated with authenticated user

---

**US-2: Conversational Task Listing**
- **As a** user
- **I want to** ask about my tasks in natural language
- **So that** I can quickly see what needs to be done

**Acceptance Criteria:**
- User can ask "What are my tasks?" or "Show me all tasks"
- User can filter: "What's pending?" or "What have I completed?"
- System returns formatted list of tasks
- Empty lists return friendly messages

---

**US-3: Natural Language Task Completion**
- **As a** user
- **I want to** mark tasks complete through conversation
- **So that** I can update status without clicking buttons

**Acceptance Criteria:**
- User can say "Mark task 3 as complete" or "I finished task 5"
- System confirms completion with task title
- Task status updates in database
- Handles invalid task IDs gracefully

---

**US-4: Conversational Task Updates**
- **As a** user
- **I want to** modify task details through natural language
- **So that** I can make changes quickly

**Acceptance Criteria:**
- User can say "Change task 1 to 'Call mom tonight'"
- User can update descriptions: "Update task 2 description to include meeting notes"
- System confirms update with new details
- Validates task ownership before updating

---

**US-5: Natural Language Task Deletion**
- **As a** user
- **I want to** delete tasks by describing them
- **So that** I can remove unwanted tasks easily

**Acceptance Criteria:**
- User can say "Delete task 4" or "Remove the grocery task"
- System confirms deletion with task title
- Task is permanently removed from database
- Handles non-existent tasks gracefully

---

**US-6: Conversation Context Persistence**
- **As a** user
- **I want to** continue previous conversations
- **So that** I can maintain context across sessions

**Acceptance Criteria:**
- Conversation history persists in database
- User can resume conversations after logout/login
- Server restart doesn't lose conversation state
- Each conversation has unique ID

---

**US-7: Multi-Turn Conversations**
- **As a** user
- **I want to** have natural back-and-forth conversations
- **So that** I can clarify or refine my requests

**Acceptance Criteria:**
- Agent remembers context within conversation
- User can reference previous messages
- Agent can ask clarifying questions
- Conversation flows naturally

---

## 3. Functional Requirements

### 3.1 Frontend Requirements

**FR-1: ChatKit Integration**
- Implement OpenAI ChatKit UI component
- Configure domain allowlist for production deployment
- Handle authentication token passing
- Display conversation history
- Show typing indicators during AI processing
- Support message input with Enter key submission

**FR-2: Chat Interface**
- Clean, modern chat UI with message bubbles
- User messages aligned right, assistant messages left
- Timestamp display for each message
- Loading states during API calls
- Error message display
- Conversation list/history view

**FR-3: Authentication Integration**
- Integrate with existing Better Auth system
- Pass JWT token with chat requests
- Handle token expiration gracefully
- Redirect to login if unauthenticated

---

### 3.2 Backend Requirements

**FR-4: Chat API Endpoint**
- **Endpoint:** `POST /api/{user_id}/chat`
- Accept conversation_id (optional) and message (required)
- Validate user authentication via JWT
- Fetch conversation history from database
- Process message through OpenAI Agents SDK
- Store user message and assistant response
- Return conversation_id, response, and tool_calls

**FR-5: OpenAI Agents SDK Integration**
- Initialize OpenAI Agent with system prompt
- Configure agent with MCP tools
- Build message array from conversation history
- Execute agent with user message
- Handle agent responses and tool calls
- Manage API errors and retries

**FR-6: MCP Server Implementation**
- Build MCP server using Official MCP SDK
- Expose 5 task management tools
- Implement stateless tool handlers
- Validate tool parameters
- Return structured responses
- Handle database operations within tools

---

### 3.3 Database Requirements

**FR-7: Conversation Model**
```
Table: conversations
- id: SERIAL PRIMARY KEY
- user_id: UUID NOT NULL (FK -> users.id)
- created_at: TIMESTAMP DEFAULT NOW()
- updated_at: TIMESTAMP DEFAULT NOW()
- INDEX: user_id
```

**FR-8: Message Model**
```
Table: messages
- id: SERIAL PRIMARY KEY
- conversation_id: INTEGER NOT NULL (FK -> conversations.id)
- user_id: UUID NOT NULL (FK -> users.id)
- role: VARCHAR(20) NOT NULL ('user' or 'assistant')
- content: TEXT NOT NULL
- created_at: TIMESTAMP DEFAULT NOW()
- INDEX: conversation_id
- INDEX: user_id
```

**FR-9: Database Migrations**
- Create migration scripts for new tables
- Add foreign key constraints
- Create indexes for performance
- Handle rollback scenarios

---

### 3.4 MCP Tools Specifications

**FR-10: Tool - add_task**
```json
{
  "name": "add_task",
  "description": "Create a new task for the user",
  "parameters": {
    "user_id": {
      "type": "string",
      "required": true,
      "description": "User ID from authentication"
    },
    "title": {
      "type": "string",
      "required": true,
      "description": "Task title (1-200 characters)"
    },
    "description": {
      "type": "string",
      "required": false,
      "description": "Task description (max 1000 characters)"
    }
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

**FR-11: Tool - list_tasks**
```json
{
  "name": "list_tasks",
  "description": "Retrieve user's tasks with optional filtering",
  "parameters": {
    "user_id": {
      "type": "string",
      "required": true,
      "description": "User ID from authentication"
    },
    "status": {
      "type": "string",
      "required": false,
      "enum": ["all", "pending", "completed"],
      "default": "all",
      "description": "Filter tasks by completion status"
    }
  },
  "returns": {
    "tasks": "array of task objects"
  }
}
```

**FR-12: Tool - complete_task**
```json
{
  "name": "complete_task",
  "description": "Mark a task as complete",
  "parameters": {
    "user_id": {
      "type": "string",
      "required": true,
      "description": "User ID from authentication"
    },
    "task_id": {
      "type": "integer",
      "required": true,
      "description": "ID of task to complete"
    }
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

**FR-13: Tool - delete_task**
```json
{
  "name": "delete_task",
  "description": "Remove a task from the list",
  "parameters": {
    "user_id": {
      "type": "string",
      "required": true,
      "description": "User ID from authentication"
    },
    "task_id": {
      "type": "integer",
      "required": true,
      "description": "ID of task to delete"
    }
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

**FR-14: Tool - update_task**
```json
{
  "name": "update_task",
  "description": "Modify task title or description",
  "parameters": {
    "user_id": {
      "type": "string",
      "required": true,
      "description": "User ID from authentication"
    },
    "task_id": {
      "type": "integer",
      "required": true,
      "description": "ID of task to update"
    },
    "title": {
      "type": "string",
      "required": false,
      "description": "New task title"
    },
    "description": {
      "type": "string",
      "required": false,
      "description": "New task description"
    }
  },
  "returns": {
    "task_id": "integer",
    "status": "string",
    "title": "string"
  }
}
```

---

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-1:** Chat response time < 3 seconds for 95% of requests
- **NFR-2:** Support 100 concurrent users
- **NFR-3:** Database queries optimized with proper indexes
- **NFR-4:** OpenAI API calls with timeout and retry logic

### 4.2 Scalability
- **NFR-5:** Stateless server architecture (no in-memory session state)
- **NFR-6:** Horizontal scaling capability
- **NFR-7:** Database connection pooling
- **NFR-8:** Conversation history pagination for large datasets

### 4.3 Security
- **NFR-9:** All chat endpoints require JWT authentication
- **NFR-10:** User isolation - users only access their own conversations
- **NFR-11:** Input validation on all user messages
- **NFR-12:** SQL injection prevention via ORM
- **NFR-13:** Rate limiting on chat endpoint (10 requests/minute per user)

### 4.4 Reliability
- **NFR-14:** Graceful handling of OpenAI API failures
- **NFR-15:** Database transaction management for consistency
- **NFR-16:** Error logging for debugging
- **NFR-17:** Conversation state recovery after server restart

### 4.5 Usability
- **NFR-18:** Natural, conversational AI responses
- **NFR-19:** Clear error messages for users
- **NFR-20:** Confirmation messages for all actions
- **NFR-21:** Helpful suggestions when commands are unclear

---

## 5. Natural Language Command Examples

### 5.1 Task Creation Commands
| User Input | Expected Behavior |
|------------|-------------------|
| "Add a task to buy groceries" | Create task with title "Buy groceries" |
| "Remind me to call mom" | Create task with title "Call mom" |
| "I need to finish the report by Friday" | Create task with title "Finish the report by Friday" |
| "Create a task: Review pull requests" | Create task with title "Review pull requests" |

### 5.2 Task Listing Commands
| User Input | Expected Behavior |
|------------|-------------------|
| "Show me all my tasks" | List all tasks (pending + completed) |
| "What's pending?" | List only pending tasks |
| "What have I completed?" | List only completed tasks |
| "List my tasks" | List all tasks |

### 5.3 Task Completion Commands
| User Input | Expected Behavior |
|------------|-------------------|
| "Mark task 3 as complete" | Complete task with ID 3 |
| "I finished task 5" | Complete task with ID 5 |
| "Task 2 is done" | Complete task with ID 2 |
| "Complete the grocery task" | List tasks, identify grocery task, complete it |

### 5.4 Task Update Commands
| User Input | Expected Behavior |
|------------|-------------------|
| "Change task 1 to 'Call mom tonight'" | Update task 1 title |
| "Update task 2 description to include meeting notes" | Update task 2 description |
| "Rename task 4 to 'Urgent: Submit report'" | Update task 4 title |

### 5.5 Task Deletion Commands
| User Input | Expected Behavior |
|------------|-------------------|
| "Delete task 4" | Delete task with ID 4 |
| "Remove the meeting task" | List tasks, identify meeting task, delete it |
| "Cancel task 7" | Delete task with ID 7 |

---

## 6. Agent Behavior Specification

### 6.1 System Prompt
The AI agent should be configured with a system prompt that:
- Identifies itself as a helpful task management assistant
- Explains its capabilities (add, list, update, delete, complete tasks)
- Uses friendly, conversational tone
- Confirms actions before executing
- Asks for clarification when commands are ambiguous
- Provides helpful error messages

### 6.2 Tool Selection Logic
| User Intent | Tool to Call | Additional Logic |
|-------------|--------------|------------------|
| Create/Add/Remember | `add_task` | Extract title and optional description |
| Show/List/Display | `list_tasks` | Determine status filter from context |
| Complete/Done/Finish | `complete_task` | Extract task ID or search by title |
| Delete/Remove/Cancel | `delete_task` | Extract task ID or search by title |
| Change/Update/Modify | `update_task` | Extract task ID and new values |

### 6.3 Error Handling
- **Task Not Found:** "I couldn't find task #X. Would you like to see your current tasks?"
- **Invalid Task ID:** "Please provide a valid task number."
- **Ambiguous Command:** "I'm not sure what you'd like to do. Could you rephrase that?"
- **API Error:** "I'm having trouble processing that right now. Please try again."

---

## 7. API Specifications

### 7.1 Chat Endpoint

**POST /api/{user_id}/chat**

**Request Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "conversation_id": 123,  // Optional - creates new if omitted
  "message": "Add a task to buy groceries"
}
```

**Response (Success - 200):**
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list. Task ID: 42",
  "tool_calls": ["add_task"],
  "timestamp": "2026-01-25T18:30:00Z"
}
```

**Response (Error - 400):**
```json
{
  "error": "Message is required",
  "code": "INVALID_REQUEST"
}
```

**Response (Error - 401):**
```json
{
  "error": "Unauthorized",
  "code": "AUTH_REQUIRED"
}
```

**Response (Error - 500):**
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```

---

## 8. Data Flow

### 8.1 Stateless Request Cycle
```
1. Client sends message → POST /api/{user_id}/chat
2. Server validates JWT token
3. Server fetches conversation history from DB
4. Server builds message array (history + new message)
5. Server stores user message in DB
6. Server calls OpenAI Agents SDK with message array
7. Agent analyzes message and selects appropriate MCP tool(s)
8. MCP tool executes (e.g., add_task, list_tasks)
9. Tool returns result to agent
10. Agent generates natural language response
11. Server stores assistant response in DB
12. Server returns response to client
13. Server discards all in-memory state
```

### 8.2 Conversation State Management
- All conversation state stored in database
- No server-side session storage
- Each request is independent
- Conversation history loaded on-demand
- Enables horizontal scaling

---

## 9. Acceptance Criteria

### 9.1 Functional Acceptance
- [ ] User can create tasks through natural language
- [ ] User can list tasks with status filtering
- [ ] User can mark tasks as complete
- [ ] User can update task details
- [ ] User can delete tasks
- [ ] Conversation history persists across sessions
- [ ] Server remains stateless (no in-memory state)
- [ ] All 5 MCP tools function correctly
- [ ] Agent correctly interprets natural language commands

### 9.2 Technical Acceptance
- [ ] OpenAI ChatKit integrated in frontend
- [ ] Chat API endpoint implemented
- [ ] OpenAI Agents SDK configured
- [ ] MCP server built with Official SDK
- [ ] Database models created (Conversation, Message)
- [ ] Database migrations executed
- [ ] JWT authentication enforced
- [ ] User isolation implemented

### 9.3 Quality Acceptance
- [ ] Response time < 3 seconds for 95% of requests
- [ ] Error handling for all failure scenarios
- [ ] Input validation on all endpoints
- [ ] Comprehensive error messages
- [ ] Code follows existing project patterns
- [ ] No security vulnerabilities

### 9.4 Documentation Acceptance
- [ ] README updated with Phase III setup
- [ ] API documentation for chat endpoint
- [ ] MCP tools documentation
- [ ] Environment variables documented
- [ ] Deployment instructions included

---

## 10. Dependencies

### 10.1 External Dependencies
- OpenAI API account and API key
- OpenAI ChatKit domain allowlist configuration
- OpenAI Agents SDK (Python)
- Official MCP SDK (Python)
- Existing Phase II infrastructure

### 10.2 Internal Dependencies
- Phase II authentication system (Better Auth)
- Phase II task CRUD operations
- Phase II database schema
- Neon PostgreSQL database

---

## 11. Risks and Mitigations

### 11.1 Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| OpenAI API rate limits | High | Medium | Implement rate limiting, caching, retry logic |
| ChatKit domain allowlist issues | High | Low | Test early, document setup process |
| MCP SDK learning curve | Medium | High | Study documentation, start with simple tools |
| Conversation history performance | Medium | Medium | Implement pagination, optimize queries |

### 11.2 Integration Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Better Auth not implemented | High | High | Implement Better Auth before Phase III |
| Database schema conflicts | Medium | Low | Review existing schema, plan migrations |
| Frontend-backend integration | Medium | Medium | Define clear API contracts |

---

## 12. Testing Strategy

### 12.1 Unit Tests
- MCP tool functions
- Database models
- Message parsing logic
- Authentication validation

### 12.2 Integration Tests
- Chat endpoint with OpenAI Agents SDK
- MCP server with tools
- Database operations
- Authentication flow

### 12.3 End-to-End Tests
- Complete conversation flows
- Multi-turn conversations
- Error scenarios
- Conversation persistence

### 12.4 Manual Testing
- Natural language command variations
- Edge cases and ambiguous inputs
- UI/UX flow
- Performance under load

---

## 13. Deployment Considerations

### 13.1 Environment Variables
```
# OpenAI Configuration
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...

# Existing from Phase II
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
FRONTEND_URL=http://localhost:3000
```

### 13.2 Domain Allowlist Setup
1. Deploy frontend to production (Vercel)
2. Get production URL
3. Add to OpenAI domain allowlist
4. Obtain domain key
5. Configure in environment variables

### 13.3 Database Migrations
- Run migrations before deployment
- Test rollback procedures
- Backup database before migration

---

## 14. Future Enhancements (Out of Scope for Phase III)

- Voice input/output
- Multi-language support
- Advanced NLP (sentiment analysis, intent classification)
- Task scheduling and reminders
- Collaborative task management
- Mobile app integration
- Analytics and insights

---

## 15. References

- [OpenAI ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-sdk)
- [Official MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Hackathon Phase III Requirements](../Hackathon%20II%20-%20Todo%20Spec-Driven%20Development.md)
- [Phase II Specification](../002-fullstack-web-app/spec.md)

---

**Document Version:** 1.0
**Last Updated:** January 25, 2026
**Author:** Spec-Driven Development Team
**Status:** Draft - Ready for Review
