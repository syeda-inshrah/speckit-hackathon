# Phase III: AI-Powered Todo Chatbot

## 📋 Overview

This directory contains the complete specification, implementation plan, and task breakdown for Phase III of the Todo Application hackathon project. Phase III transforms the existing web-based todo application into an AI-powered conversational chatbot using OpenAI Agents SDK and Model Context Protocol (MCP).

**Status:** 📝 Specification Complete - Ready for Implementation

---

## 📁 Document Structure

### Core Documents

| Document | Purpose | Status |
|----------|---------|--------|
| [spec.md](./spec.md) | Complete feature specification with user stories, requirements, and acceptance criteria | ✅ Complete |
| [plan.md](./plan.md) | Technical implementation plan with architecture, design decisions, and code examples | ✅ Complete |
| [tasks.md](./tasks.md) | Detailed task breakdown with 37 implementation tasks organized into 5 phases | ✅ Complete |
| [README.md](./README.md) | This file - overview and navigation guide | ✅ Complete |

---

## 🎯 Phase III Objectives

Transform the Phase II web application into an AI-powered chatbot that allows users to manage their tasks through natural language conversations.

### Key Features
- ✅ Natural language task management (add, list, update, delete, complete)
- ✅ OpenAI ChatKit conversational interface
- ✅ OpenAI Agents SDK for intent understanding
- ✅ MCP server with 5 standardized task operation tools
- ✅ Stateless server architecture with database-persisted conversations
- ✅ Multi-turn conversation support with context persistence

---

## 🏗️ Architecture Overview

```
┌─────────────────┐
│  ChatKit UI     │  ← User interacts via natural language
│  (Next.js)      │
└────────┬────────┘
         │ HTTPS + JWT
         ▼
┌─────────────────┐
│  Chat API       │  ← POST /api/{user_id}/chat
│  (FastAPI)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenAI Agents  │  ← Natural language understanding
│  SDK            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP Server     │  ← 5 task operation tools
│  (Official SDK) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Neon Database  │  ← Tasks, Conversations, Messages
│  (PostgreSQL)   │
└─────────────────┘
```

---

## 📚 Technology Stack

### Frontend
- **Next.js 16+** - React framework
- **OpenAI ChatKit** - Chat UI component
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling

### Backend
- **Python 3.13+** - Runtime
- **FastAPI** - Web framework
- **OpenAI Agents SDK** - AI agent framework
- **Official MCP SDK** - Tool protocol
- **SQLModel** - ORM
- **Better Auth** - Authentication (required)

### Infrastructure
- **Neon PostgreSQL** - Database
- **OpenAI API** - LLM inference
- **Vercel** - Frontend hosting

---

## 🚀 Getting Started

### Prerequisites

Before starting Phase III implementation, ensure:

1. ✅ **Phase II is complete** - Web application with authentication and task CRUD
2. ⚠️ **Better Auth is implemented** - This is a CRITICAL blocker (see Task 1.1)
3. ✅ **OpenAI API account** - Get API key from platform.openai.com
4. ✅ **Development environment** - Node.js, Python 3.13+, PostgreSQL

### Implementation Order

Follow this sequence for successful implementation:

1. **Read the Specification** ([spec.md](./spec.md))
   - Understand user stories and requirements
   - Review acceptance criteria
   - Familiarize yourself with natural language commands

2. **Study the Implementation Plan** ([plan.md](./plan.md))
   - Review architecture decisions
   - Understand component responsibilities
   - Study code examples and patterns

3. **Follow the Task Breakdown** ([tasks.md](./tasks.md))
   - Start with Phase 1 (Foundation) - especially Task 1.1 (Better Auth)
   - Complete tasks in order
   - Check off completed tasks
   - Run tests after each phase

---

## ⚠️ Critical Blockers

### 🔴 BLOCKER: Better Auth Not Implemented

**Current Status:** Phase II uses custom JWT authentication instead of Better Auth as specified.

**Impact:** Phase III requires Better Auth for proper authentication integration.

**Action Required:**
- Complete Task 1.1 in [tasks.md](./tasks.md)
- Implement Better Auth in frontend
- Update backend to validate Better Auth JWT tokens
- Test all existing Phase II endpoints

**Estimated Effort:** 8-12 hours

**Priority:** CRITICAL - Must be completed before starting other Phase III tasks

---

## 📊 Implementation Progress

### Phase 1: Foundation (4 tasks)
- [ ] Task 1.1: Implement Better Auth (CRITICAL BLOCKER)
- [ ] Task 1.2: Create Database Models
- [ ] Task 1.3: Create Database Migrations
- [ ] Task 1.4: Set Up OpenAI API Integration

### Phase 2: Backend Core (9 tasks)
- [ ] Task 2.1: Implement MCP Server Structure
- [ ] Task 2.2: Implement add_task MCP Tool
- [ ] Task 2.3: Implement list_tasks MCP Tool
- [ ] Task 2.4: Implement complete_task MCP Tool
- [ ] Task 2.5: Implement update_task MCP Tool
- [ ] Task 2.6: Implement delete_task MCP Tool
- [ ] Task 2.7: Implement OpenAI Agents SDK Integration
- [ ] Task 2.8: Implement Chat API Endpoint
- [ ] Task 2.9: Implement Conversation History Loading

### Phase 3: Frontend Integration (5 tasks)
- [ ] Task 3.1: Install and Configure OpenAI ChatKit
- [ ] Task 3.2: Create Chat Page Component
- [ ] Task 3.3: Implement Chat API Client
- [ ] Task 3.4: Implement Conversation State Management
- [ ] Task 3.5: Add Navigation to Chat Page

### Phase 4: Testing & Quality (5 tasks)
- [ ] Task 4.1: Write Unit Tests for MCP Tools
- [ ] Task 4.2: Write Integration Tests for Chat API
- [ ] Task 4.3: Write End-to-End Tests
- [ ] Task 4.4: Performance Testing
- [ ] Task 4.5: Security Testing

### Phase 5: Deployment (7 tasks)
- [ ] Task 5.1: Prepare Production Environment
- [ ] Task 5.2: Run Database Migrations
- [ ] Task 5.3: Deploy Backend
- [ ] Task 5.4: Deploy Frontend
- [ ] Task 5.5: End-to-End Production Testing
- [ ] Task 5.6: Create Demo Video
- [ ] Task 5.7: Prepare Submission

**Total Progress:** 0/37 tasks completed (0%)

---

## 🔑 Key Concepts

### Stateless Architecture
- Server holds no in-memory session state
- All conversation state persisted in database
- Enables horizontal scaling
- Conversation history loaded on-demand

### MCP (Model Context Protocol)
- Standardized interface for AI-to-application communication
- Tools expose task operations to AI agent
- Stateless tool handlers
- Structured request/response format

### OpenAI Agents SDK
- Natural language understanding
- Intent recognition and tool selection
- Multi-turn conversation support
- Context management

### Conversation Persistence
- Conversations stored in database
- Messages linked to conversations
- History loaded for context
- Survives server restarts

---

## 📖 Natural Language Examples

### Task Creation
```
User: "Add a task to buy groceries"
Agent: "I've added 'Buy groceries' to your task list. Task ID: 42"
```

### Task Listing
```
User: "What are my pending tasks?"
Agent: "You have 3 pending tasks:
1. Buy groceries
2. Call mom
3. Finish report"
```

### Task Completion
```
User: "Mark task 42 as complete"
Agent: "Great! I've marked 'Buy groceries' as complete."
```

### Task Update
```
User: "Change task 1 to 'Call mom tonight'"
Agent: "I've updated task 1 to 'Call mom tonight'."
```

### Task Deletion
```
User: "Delete task 3"
Agent: "I've deleted 'Finish report' from your task list."
```

---

## 🧪 Testing Strategy

### Unit Tests
- MCP tool functions
- Database models
- Message parsing
- Authentication validation

### Integration Tests
- Chat endpoint with mocked OpenAI
- MCP server with tools
- Database operations
- Authentication flow

### End-to-End Tests
- Complete conversation flows
- Multi-turn conversations
- Error scenarios
- Conversation persistence

### Performance Tests
- Response time < 3 seconds
- Concurrent user handling
- Database query optimization
- Load testing

---

## 🔒 Security Considerations

### Authentication & Authorization
- All endpoints require JWT authentication
- User ID validation
- Conversation ownership verification
- Message access control

### Input Validation
- Message length limits (1-2000 characters)
- SQL injection prevention (SQLModel ORM)
- XSS prevention
- Rate limiting (10 requests/minute per user)

### Data Privacy
- User isolation at database level
- No cross-user data leakage
- Secure token storage
- Conversation history encryption

---

## 📈 Success Metrics

### Functional Metrics
- ✅ All 5 basic task operations work via natural language
- ✅ Conversation history persists across sessions
- ✅ Server remains stateless
- ✅ Multi-turn conversations supported

### Technical Metrics
- ⏱️ Response time < 3 seconds (95th percentile)
- 📊 Error rate < 1%
- 🔄 Uptime > 99%
- 💾 Database query time < 100ms

### User Experience Metrics
- 💬 Natural, conversational AI responses
- ✅ Clear error messages
- 🎯 Helpful action confirmations
- ⚡ Fast and responsive interface

---

## 🎓 Learning Resources

### OpenAI Documentation
- [ChatKit Documentation](https://platform.openai.com/docs/guides/chatkit)
- [Agents SDK](https://github.com/openai/openai-agents-sdk)
- [API Reference](https://platform.openai.com/docs/api-reference)

### MCP Documentation
- [Official MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Specification](https://modelcontextprotocol.io/)

### Related Documentation
- [Phase II Specification](../002-fullstack-web-app/spec.md)
- [Hackathon Requirements](../../Hackathon%20II%20-%20Todo%20Spec-Driven%20Development.md)

---

## 🐛 Troubleshooting

### Common Issues

**Issue:** ChatKit not loading
- **Solution:** Verify domain allowlist configuration and domain key

**Issue:** OpenAI API errors
- **Solution:** Check API key, rate limits, and error messages

**Issue:** Conversation not persisting
- **Solution:** Verify database migrations and conversation ID handling

**Issue:** Agent not calling tools
- **Solution:** Check tool registration and system prompt

**Issue:** Authentication failures
- **Solution:** Verify Better Auth configuration and JWT validation

---

## 📝 Submission Requirements

### Required Deliverables
1. ✅ Public GitHub repository
2. ✅ Deployed frontend URL (Vercel)
3. ✅ Demo video (under 90 seconds)
4. ✅ WhatsApp number for presentation invitation

### Submission Form
[https://forms.gle/KMKEKaFUD6ZX4UtY8](https://forms.gle/KMKEKaFUD6ZX4UtY8)

### Due Date
**December 21, 2025** (200 points)

---

## 🎯 Next Steps

1. **Resolve Better Auth Blocker**
   - Read Task 1.1 in [tasks.md](./tasks.md)
   - Implement Better Auth in frontend and backend
   - Test all existing Phase II functionality

2. **Set Up Development Environment**
   - Install OpenAI SDK
   - Get OpenAI API key
   - Configure environment variables

3. **Start Implementation**
   - Follow task order in [tasks.md](./tasks.md)
   - Check off completed tasks
   - Run tests after each phase

4. **Deploy and Test**
   - Deploy to production
   - Configure domain allowlist
   - Create demo video
   - Submit to hackathon

---

## 📞 Support

For questions or issues:
- Review the [specification](./spec.md) for requirements
- Check the [implementation plan](./plan.md) for technical details
- Follow the [task breakdown](./tasks.md) for step-by-step guidance
- Refer to the [hackathon document](../../Hackathon%20II%20-%20Todo%20Spec-Driven%20Development.md) for official requirements

---

**Document Version:** 1.0
**Last Updated:** January 25, 2026
**Status:** Ready for Implementation
**Estimated Effort:** 91-94 hours (2-3 weeks full-time)

---

## 🎉 Good Luck!

Phase III is an exciting challenge that will teach you:
- AI agent development
- Natural language processing
- Conversational UI design
- Stateless architecture patterns
- MCP protocol implementation

Follow the specifications carefully, test thoroughly, and create an amazing AI-powered todo chatbot! 🚀
