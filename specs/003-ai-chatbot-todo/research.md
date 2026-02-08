# Research: AI-Powered Todo Chatbot

**Feature ID:** 003-ai-chatbot-todo
**Research Version:** 1.0
**Status:** Complete
**Last Updated:** 2026-01-26
**Researcher:** AI Development Team

---

## 1. Executive Summary

This research document covers the investigation and analysis conducted during the planning of the AI-powered conversational todo chatbot. It includes evaluations of AI frameworks, conversational UI patterns, MCP architecture, natural language processing approaches, and stateless design patterns. This research builds upon Phase 2's foundation and introduces AI-native capabilities for task management through natural language.

## 2. AI Framework Research

### 2.1 AI Agent Framework Comparison

#### OpenAI Agents SDK vs LangChain vs AutoGPT vs Custom Implementation

**OpenAI Agents SDK (Hackathon Requirement):**
- ✅ **Pros:**
  - Official OpenAI framework
  - Built-in tool calling support
  - Conversation management
  - Thread-based architecture
  - Excellent documentation
  - Meets hackathon requirements
  - Native integration with OpenAI models
- ❌ **Cons:**
  - Vendor lock-in to OpenAI
  - Requires OpenAI API key
  - Cost per API call
  - Limited to OpenAI models

**LangChain:**
- ✅ **Pros:**
  - Model-agnostic (supports multiple LLM providers)
  - Rich ecosystem of tools and integrations
  - Memory management built-in
  - Large community
  - Extensive documentation
- ❌ **Cons:**
  - More complex than needed for simple use cases
  - Steeper learning curve
  - Doesn't meet hackathon requirement
  - Potential over-engineering

**AutoGPT:**
- ✅ **Pros:**
  - Autonomous agent capabilities
  - Goal-oriented task execution
  - Self-prompting
- ❌ **Cons:**
  - Overkill for todo management
  - Less control over agent behavior
  - Higher API costs
  - Not suitable for hackathon requirements

**Custom Implementation:**
- ✅ **Pros:**
  - Full control over behavior
  - No framework dependencies
  - Learning opportunity
- ❌ **Cons:**
  - Doesn't meet hackathon requirement
  - Need to implement conversation management
  - More development time
  - Reinventing the wheel

**Decision:** OpenAI Agents SDK chosen as per hackathon requirements, providing official support and built-in features.

### 2.2 Large Language Model Selection

#### GPT-4 vs GPT-3.5-Turbo vs Claude vs Llama

**GPT-4:**
- ✅ **Pros:**
  - Superior reasoning capabilities
  - Better at following complex instructions
  - More accurate tool calling
  - Better context understanding
- ❌ **Cons:**
  - Higher cost per token
  - Slower response time
  - May be overkill for simple tasks

**GPT-3.5-Turbo:**
- ✅ **Pros:**
  - Fast response time
  - Lower cost
  - Good for simple tasks
  - Sufficient for todo management
- ❌ **Cons:**
  - Less capable than GPT-4
  - May struggle with complex instructions
  - Less accurate tool calling

**Claude (Anthropic):**
- ✅ **Pros:**
  - Strong reasoning capabilities
  - Good safety features
  - Competitive pricing
- ❌ **Cons:**
  - Different API (not OpenAI)
  - Doesn't work with OpenAI Agents SDK
  - Would require custom implementation

**Llama (Meta):**
- ✅ **Pros:**
  - Open source
  - Can be self-hosted
  - No API costs
- ❌ **Cons:**
  - Requires infrastructure
  - Less capable than GPT models
  - More complex setup

**Decision:** GPT-4 for production (better accuracy), GPT-3.5-Turbo for development (cost-effective).

## 3. MCP (Model Context Protocol) Research

### 3.1 MCP Architecture Patterns

#### Official MCP SDK vs Custom Protocol vs Function Calling

**Official MCP SDK (Hackathon Requirement):**
- ✅ **Pros:**
  - Standardized protocol
  - Built-in tool registration
  - Type safety
  - Documentation and examples
  - Meets hackathon requirements
  - Future-proof (industry standard)
- ❌ **Cons:**
  - Learning curve for new protocol
  - Additional abstraction layer
  - Newer technology (less mature)

**Custom Protocol:**
- ✅ **Pros:**
  - Full control over implementation
  - Simpler for basic use cases
  - No additional dependencies
- ❌ **Cons:**
  - Doesn't meet hackathon requirement
  - Not standardized
  - More maintenance burden
  - Less interoperable

**Direct Function Calling:**
- ✅ **Pros:**
  - Simplest approach
  - Direct integration
  - No protocol overhead
- ❌ **Cons:**
  - Doesn't meet hackathon requirement
  - Less structured
  - Harder to maintain
  - Not scalable

**Decision:** Official MCP SDK chosen for standardization and hackathon compliance.

### 3.2 MCP Tool Design Patterns

Research into MCP tool design revealed best practices:

**Stateless Tools:**
- Each tool invocation is independent
- No shared state between calls
- Database is the source of truth
- Enables horizontal scaling

**Parameter Validation:**
- Strict type checking
- Required vs optional parameters
- Range validation
- Format validation

**Error Handling:**
- Structured error responses
- User-friendly error messages
- Logging for debugging
- Graceful degradation

**Response Format:**
- Consistent structure across tools
- Include status indicators
- Provide actionable feedback
- Return relevant data

## 4. Conversational UI Research

### 4.1 Chat Interface Framework Comparison

#### OpenAI ChatKit vs Custom React Chat vs Stream Chat vs SendBird

**OpenAI ChatKit (Hackathon Requirement):**
- ✅ **Pros:**
  - Official OpenAI component
  - Designed for AI conversations
  - Built-in message handling
  - TypeScript support
  - Meets hackathon requirements
  - Easy integration with OpenAI API
- ❌ **Cons:**
  - Requires domain allowlist setup
  - Less customization than custom build
  - Vendor lock-in
  - Newer component (less mature)

**Custom React Chat:**
- ✅ **Pros:**
  - Full control over UI/UX
  - No external dependencies
  - Complete customization
  - Learning opportunity
- ❌ **Cons:**
  - Doesn't meet hackathon requirement
  - More development time
  - Need to handle edge cases
  - Reinventing the wheel

**Stream Chat:**
- ✅ **Pros:**
  - Feature-rich
  - Real-time capabilities
  - Good documentation
  - Production-ready
- ❌ **Cons:**
  - Overkill for AI chatbot
  - External service dependency
  - Cost considerations
  - Not designed for AI agents

**SendBird:**
- ✅ **Pros:**
  - Enterprise-grade
  - Scalable
  - Many features
- ❌ **Cons:**
  - Too complex for hackathon
  - Cost prohibitive
  - Not AI-focused

**Decision:** OpenAI ChatKit chosen for official support and AI-first design.

### 4.2 Conversation UX Patterns

Research into conversational interfaces revealed key patterns:

**Message Display:**
- User messages aligned right
- Assistant messages aligned left
- Timestamps for context
- Loading indicators during processing
- Error states clearly indicated

**Input Handling:**
- Enter key to send
- Shift+Enter for new line
- Character count indicators
- Disabled state during processing
- Clear button for input

**Conversation Flow:**
- Smooth scrolling to new messages
- Auto-scroll to bottom
- Scroll to top for history
- Infinite scroll for long conversations
- Message grouping by time

**Feedback Mechanisms:**
- Typing indicators
- Message delivery status
- Error notifications
- Success confirmations
- Action buttons for quick responses

## 5. Natural Language Processing Research

### 5.1 Intent Recognition Approaches

#### LLM-Based vs Rule-Based vs Hybrid

**LLM-Based (Chosen Approach):**
- ✅ **Pros:**
  - Handles natural language variations
  - No need for predefined patterns
  - Understands context
  - Adapts to user language
  - Leverages GPT's capabilities
- ❌ **Cons:**
  - API costs per request
  - Potential for misinterpretation
  - Requires good prompting
  - Less deterministic

**Rule-Based:**
- ✅ **Pros:**
  - Deterministic behavior
  - No API costs
  - Fast processing
  - Predictable results
- ❌ **Cons:**
  - Limited to predefined patterns
  - Doesn't handle variations well
  - Requires extensive rule definition
  - Brittle to edge cases

**Hybrid:**
- ✅ **Pros:**
  - Best of both worlds
  - Fallback mechanisms
  - Cost optimization
- ❌ **Cons:**
  - More complex implementation
  - Maintenance overhead
  - Potential inconsistencies

**Decision:** LLM-based approach with OpenAI Agents SDK for natural language understanding.

### 5.2 Entity Extraction Strategies

Research showed that GPT-4 excels at:
- Extracting task titles from natural language
- Identifying task IDs from context
- Understanding status filters (pending/completed)
- Parsing update instructions
- Recognizing deletion requests

**Best Practices:**
- Clear system prompts
- Examples in prompts (few-shot learning)
- Structured output formats
- Validation of extracted entities
- Fallback to clarification questions

## 6. Stateless Architecture Research

### 6.1 Stateless vs Stateful Server Design

#### Stateless (Chosen) vs Stateful vs Hybrid

**Stateless Architecture:**
- ✅ **Pros:**
  - Horizontal scalability
  - No server-side session storage
  - Resilient to server restarts
  - Load balancer friendly
  - Simpler deployment
- ❌ **Cons:**
  - Database queries for every request
  - Potential performance overhead
  - More complex state management

**Stateful Architecture:**
- ✅ **Pros:**
  - Faster access to session data
  - Less database load
  - Simpler conversation context
- ❌ **Cons:**
  - Sticky sessions required
  - Not horizontally scalable
  - State lost on restart
  - More complex deployment

**Hybrid:**
- ✅ **Pros:**
  - Balance of performance and scalability
  - Caching for frequently accessed data
- ❌ **Cons:**
  - More complex implementation
  - Cache invalidation challenges
  - Consistency concerns

**Decision:** Stateless architecture chosen for scalability and resilience.

### 6.2 Conversation State Management

Research into conversation persistence patterns:

**Database-Backed State:**
- All conversation history in database
- Messages stored with timestamps
- Conversation metadata tracked
- User isolation enforced
- Enables conversation resume

**State Loading Strategies:**
- Load last N messages (e.g., 50)
- Pagination for long conversations
- Lazy loading for performance
- Caching for frequently accessed conversations

**State Synchronization:**
- Optimistic UI updates
- Server as source of truth
- Conflict resolution strategies
- Real-time sync (future enhancement)

## 7. Security Research

### 7.1 AI-Specific Security Concerns

#### Prompt Injection vs Data Leakage vs API Abuse

**Prompt Injection:**
- **Risk:** Users manipulating AI behavior through crafted inputs
- **Mitigation:**
  - System prompts with clear boundaries
  - Input validation and sanitization
  - Context isolation per user
  - Monitoring for suspicious patterns

**Data Leakage:**
- **Risk:** AI revealing other users' data
- **Mitigation:**
  - User ID validation on every request
  - Database-level isolation
  - No cross-user data in prompts
  - Audit logging

**API Abuse:**
- **Risk:** Excessive API calls, cost overruns
- **Mitigation:**
  - Rate limiting (10 requests/minute per user)
  - Request size limits
  - Timeout configurations
  - Cost monitoring and alerts

### 7.2 Authentication Integration

Research confirmed:
- JWT tokens must be validated on every request
- User ID in URL must match authenticated user
- Conversation ownership must be verified
- Message access must be restricted to owner

### 7.3 Input Validation

**Message Content:**
- Length limits (1-2000 characters)
- Content sanitization
- XSS prevention
- SQL injection prevention (via ORM)

**Tool Parameters:**
- Type validation
- Range checking
- Format validation
- Required field enforcement

## 8. Performance Research

### 8.1 OpenAI API Performance

**Latency Considerations:**
- GPT-4: 2-5 seconds typical response time
- GPT-3.5-Turbo: 1-2 seconds typical response time
- Network latency: 100-300ms
- Total user-facing latency: 2-6 seconds

**Optimization Strategies:**
- Use GPT-3.5-Turbo for simple tasks
- Implement request timeouts (30 seconds)
- Show loading indicators immediately
- Stream responses (future enhancement)
- Cache common responses (future enhancement)

### 8.2 Database Performance

**Query Optimization:**
- Indexes on frequently queried columns
  - `conversations.user_id`
  - `messages.conversation_id`
  - `messages.created_at`
- Connection pooling
- Async database operations
- Pagination for large result sets

**Conversation History Loading:**
- Load last 50 messages by default
- Implement cursor-based pagination
- Optimize with proper indexes
- Consider caching for active conversations

### 8.3 Frontend Performance

**Rendering Optimization:**
- Virtual scrolling for long conversations
- Lazy loading of message history
- Optimistic UI updates
- Debounced input handling
- Memoization of expensive computations

**Bundle Optimization:**
- Code splitting by route
- Lazy load ChatKit component
- Tree shaking unused code
- Image optimization

## 9. Testing Research

### 9.1 AI Agent Testing Strategies

#### Mocking vs Live API vs Recorded Responses

**Mocking OpenAI API:**
- ✅ **Pros:**
  - Fast test execution
  - No API costs
  - Deterministic results
  - Offline testing
- ❌ **Cons:**
  - Doesn't test real AI behavior
  - Mock responses may not match reality
  - Maintenance of mock data

**Live API Testing:**
- ✅ **Pros:**
  - Tests real AI behavior
  - Catches actual issues
  - Validates prompts
- ❌ **Cons:**
  - Slow test execution
  - API costs
  - Non-deterministic results
  - Requires API key

**Recorded Responses:**
- ✅ **Pros:**
  - Balance of realism and speed
  - Deterministic results
  - No API costs after recording
- ❌ **Cons:**
  - Initial recording required
  - Responses may become outdated
  - Maintenance overhead

**Decision:** Mock for unit tests, live API for integration tests (limited), recorded for E2E tests.

### 9.2 Conversation Flow Testing

**Test Scenarios:**
- Single-turn conversations
- Multi-turn conversations with context
- Error handling and recovery
- Ambiguous user inputs
- Edge cases (empty messages, very long messages)
- Concurrent requests
- Conversation persistence across sessions

### 9.3 MCP Tool Testing

**Unit Tests:**
- Test each tool in isolation
- Mock database operations
- Test parameter validation
- Test error handling
- Test response formatting

**Integration Tests:**
- Test tools with real database
- Test user isolation
- Test transaction handling
- Test concurrent operations

## 10. Deployment Research

### 10.1 OpenAI ChatKit Domain Allowlist

**Setup Process:**
1. Deploy frontend to get production URL
2. Navigate to OpenAI platform settings
3. Add domain to security allowlist
4. Obtain domain key
5. Configure in environment variables

**Considerations:**
- Allowlist required for production
- localhost works without allowlist (development)
- Multiple domains can be added
- Domain key is environment-specific

### 10.2 Environment Configuration

**Required Environment Variables:**
```
# OpenAI Configuration
OPENAI_API_KEY=sk-...
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...

# Existing from Phase II
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
FRONTEND_URL=https://...
```

### 10.3 Monitoring and Observability

**Metrics to Track:**
- OpenAI API latency
- OpenAI API error rates
- Token usage and costs
- Conversation creation rate
- Message volume per user
- Tool invocation frequency
- Database query performance

**Logging Strategy:**
- Structured logging (JSON format)
- Log all API requests/responses (excluding message content for privacy)
- Log tool invocations
- Log errors with stack traces
- Redact sensitive data (API keys, user data)

**Alerting:**
- High OpenAI API error rate (>5%)
- Slow response time (>10 seconds)
- High API costs (budget threshold)
- Database connection issues
- Rate limit violations

## 11. User Experience Research

### 11.1 Conversational AI UX Best Practices

Research into conversational AI interfaces revealed:

**Conversation Starters:**
- Provide example commands
- Show capabilities upfront
- Suggest common actions
- Guide new users

**Error Handling:**
- Clear, actionable error messages
- Suggest corrections
- Provide examples
- Maintain conversation context

**Confirmation Patterns:**
- Confirm destructive actions
- Summarize completed actions
- Provide undo options (future enhancement)
- Show task details after creation

**Context Management:**
- Remember conversation history
- Reference previous messages
- Maintain task context
- Clear context when needed

### 11.2 Natural Language Command Design

**Command Patterns:**
- Imperative: "Add a task to buy groceries"
- Interrogative: "What are my pending tasks?"
- Declarative: "I need to call mom"
- Conversational: "Can you show me what I need to do today?"

**Ambiguity Resolution:**
- Ask clarifying questions
- Provide options to choose from
- Use context to infer intent
- Default to safe actions

### 11.3 Feedback and Confirmation

**Action Feedback:**
- Immediate acknowledgment
- Progress indicators
- Success confirmations
- Error notifications
- Helpful suggestions

**Visual Feedback:**
- Typing indicators
- Message delivery status
- Tool execution indicators
- Loading states
- Error states

## 12. Accessibility Research

### 12.1 Conversational Interface Accessibility

**Screen Reader Support:**
- ARIA live regions for new messages
- Proper labeling of input fields
- Keyboard navigation support
- Focus management
- Alternative text for icons

**Keyboard Accessibility:**
- Enter to send message
- Escape to cancel
- Arrow keys for history navigation
- Tab for focus management
- Shortcuts for common actions

### 12.2 WCAG Compliance for Chat Interfaces

**Color Contrast:**
- Message bubbles meet contrast ratios
- Error states clearly visible
- Loading indicators accessible
- Focus indicators prominent

**Text Alternatives:**
- Alt text for images
- ARIA labels for buttons
- Descriptive link text
- Status announcements

## 13. Cost Analysis Research

### 13.1 OpenAI API Pricing

**GPT-4 Pricing (as of 2026):**
- Input: $0.03 per 1K tokens
- Output: $0.06 per 1K tokens
- Average conversation: 500-1000 tokens
- Estimated cost per conversation: $0.03-$0.10

**GPT-3.5-Turbo Pricing:**
- Input: $0.0015 per 1K tokens
- Output: $0.002 per 1K tokens
- Average conversation: 500-1000 tokens
- Estimated cost per conversation: $0.002-$0.004

**Cost Optimization Strategies:**
- Use GPT-3.5-Turbo for simple tasks
- Implement response caching
- Limit conversation history length
- Optimize system prompts
- Monitor and set budget alerts

### 13.2 Infrastructure Costs

**Estimated Monthly Costs (100 active users):**
- OpenAI API: $50-$200 (depending on usage)
- Neon Database: $0 (free tier)
- Vercel Frontend: $0 (free tier)
- Backend Hosting: $0-$20 (Railway/Render free tier)
- **Total: $50-$220/month**

## 14. Scalability Research

### 14.1 Horizontal Scaling Patterns

**Stateless Server Benefits:**
- Multiple server instances
- Load balancer distribution
- No session affinity required
- Easy auto-scaling
- Resilient to failures

**Database Scaling:**
- Connection pooling
- Read replicas (future)
- Query optimization
- Caching layer (future)

### 14.2 Rate Limiting Strategies

**User-Level Rate Limiting:**
- 10 requests per minute per user
- Prevents abuse
- Protects API costs
- Ensures fair usage

**Global Rate Limiting:**
- Total requests per second
- Protects infrastructure
- Prevents cascading failures
- Budget protection

## 15. Alternative Approaches Considered

### 15.1 Approaches Not Chosen

**Streaming Responses:**
- **Why Not:** Added complexity, not required for hackathon
- **Future Enhancement:** Would improve perceived performance

**WebSocket for Real-Time:**
- **Why Not:** HTTP polling sufficient for single-user conversations
- **Future Enhancement:** Needed for collaborative features

**Voice Input/Output:**
- **Why Not:** Out of scope for Phase III
- **Future Enhancement:** Phase V bonus feature

**Multi-Language Support:**
- **Why Not:** Out of scope for Phase III
- **Future Enhancement:** Phase V bonus feature

**Advanced NLP Features:**
- **Why Not:** GPT-4 handles most cases well
- **Future Enhancement:** Custom entity extraction, sentiment analysis

## 16. Integration Patterns

### 16.1 Phase II Integration

**Reusing Existing Components:**
- Authentication system (Better Auth)
- Task CRUD operations
- Database models and migrations
- User management
- API patterns

**New Components:**
- Chat API endpoint
- MCP server and tools
- OpenAI Agents SDK integration
- Conversation and message models
- ChatKit frontend

### 16.2 Phase IV/V Preparation

**Kubernetes Readiness:**
- Stateless design enables easy containerization
- No local file storage
- Environment-based configuration
- Health check endpoints
- Graceful shutdown handling

**Event-Driven Architecture:**
- MCP tools can publish events
- Conversation events for analytics
- Task events for notifications
- Audit trail for compliance

## 17. Lessons Learned from Research

1. **AI Framework Selection:** Using official SDKs (OpenAI Agents SDK, MCP SDK) provides better support and future-proofing than custom implementations.

2. **Stateless Architecture:** Essential for scalability and resilience, especially important for cloud-native deployments in later phases.

3. **Cost Management:** OpenAI API costs can add up quickly; monitoring and optimization strategies are crucial.

4. **User Experience:** Conversational interfaces require different UX patterns than traditional forms; clear feedback and error handling are critical.

5. **Testing Challenges:** Testing AI-powered features requires different strategies than traditional software; mocking and recorded responses are essential.

6. **Security Considerations:** AI-specific security concerns (prompt injection, data leakage) require additional safeguards beyond traditional web security.

7. **Performance Trade-offs:** LLM response times (2-6 seconds) require careful UX design to maintain perceived performance.

8. **Integration Complexity:** Integrating multiple new technologies (Agents SDK, MCP, ChatKit) requires careful planning and incremental implementation.

## 18. Future Research Areas

### 18.1 For Phase IV (Kubernetes Deployment)

- Container optimization for AI workloads
- Kubernetes resource allocation for LLM applications
- Service mesh integration
- Distributed tracing for AI requests
- Cost optimization in cloud environments

### 18.2 For Phase V (Advanced Features)

- Event-driven architecture with Kafka
- Real-time collaboration features
- Advanced NLP with custom models
- Voice interface integration
- Multi-language support
- Analytics and insights dashboard

### 18.3 Emerging Technologies

- GPT-5 and future model improvements
- Edge AI for reduced latency
- Federated learning for privacy
- Multimodal AI (text + images)
- Agent-to-agent communication

## 19. References

### 19.1 Official Documentation

- OpenAI Agents SDK: https://platform.openai.com/docs/agents
- OpenAI ChatKit: https://platform.openai.com/docs/guides/chatkit
- Official MCP SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP Specification: https://modelcontextprotocol.io/
- OpenAI API Reference: https://platform.openai.com/docs/api-reference

### 19.2 Best Practices and Guides

- Conversational AI Design: https://www.nngroup.com/articles/chatbot-design/
- Prompt Engineering Guide: https://platform.openai.com/docs/guides/prompt-engineering
- AI Security Best Practices: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- Stateless Architecture Patterns: https://12factor.net/

### 19.3 Research Papers

- "Attention Is All You Need" (Transformer Architecture)
- "Language Models are Few-Shot Learners" (GPT-3 Paper)
- "Constitutional AI" (AI Safety)
- "Retrieval-Augmented Generation" (RAG Patterns)

### 19.4 Community Resources

- OpenAI Community Forum: https://community.openai.com/
- MCP Community: https://github.com/modelcontextprotocol/
- FastAPI + AI Integration Examples
- Next.js + ChatKit Examples

---

**Research Completed:** 2026-01-26
**Next Review:** Phase IV Planning
**Researcher:** AI Development Team
**Approval:** Ready for Implementation

---

## Appendix A: Technology Decision Matrix

| Technology | Score | Rationale |
|------------|-------|-----------|
| OpenAI Agents SDK | 9/10 | Official support, meets requirements, excellent documentation |
| GPT-4 | 8/10 | Best accuracy, higher cost justified for quality |
| Official MCP SDK | 8/10 | Standardized, future-proof, meets requirements |
| OpenAI ChatKit | 7/10 | Official component, some limitations, meets requirements |
| Stateless Architecture | 9/10 | Scalability, resilience, cloud-native ready |
| PostgreSQL (Neon) | 9/10 | Proven reliability, serverless benefits |

## Appendix B: Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| OpenAI API Rate Limits | Medium | High | Implement rate limiting, caching, monitoring |
| High API Costs | Medium | Medium | Use GPT-3.5-Turbo, optimize prompts, set budgets |
| Prompt Injection | Low | High | Input validation, system prompt boundaries |
| Poor AI Responses | Low | Medium | Prompt engineering, testing, fallback messages |
| ChatKit Integration Issues | Low | Medium | Early testing, follow documentation |
| Performance Issues | Medium | Medium | Optimize queries, implement caching |

## Appendix C: Glossary

- **MCP:** Model Context Protocol - standardized protocol for AI-to-application communication
- **Agent:** AI system that can use tools to accomplish tasks
- **Tool:** Function that an AI agent can call to perform actions
- **Prompt:** Instructions given to an LLM to guide its behavior
- **Token:** Unit of text processed by LLMs (roughly 4 characters)
- **Stateless:** Server architecture where no session state is stored in memory
- **Few-Shot Learning:** Providing examples in prompts to guide AI behavior
- **Intent Recognition:** Determining what action a user wants to perform
- **Entity Extraction:** Identifying specific data points from natural language
