# Hackathon II: The Evolution of Todo - Constitution

## Core Principles

### I. Spec-Driven Development (SDD) - NON-NEGOTIABLE
All development MUST follow the Spec-Kit lifecycle: **Specify → Plan → Tasks → Implement**
- NO agent is allowed to write code until specification is complete and approved
- Every code change must trace back to an explicit Task ID from speckit.tasks
- Specs are the single source of truth; agents must not infer missing requirements
- If specification is missing or underspecified, agents MUST stop and request clarification
- This prevents "vibe coding" and ensures alignment across all AI agents

### II. Agentic Dev Stack Integration
We use AGENTS.md + Spec-Kit Plus + Claude Code as our development pipeline
- AGENTS.md defines how agents should behave and what tools to use
- Spec-Kit Plus manages spec artifacts (speckit.specify, speckit.plan, speckit.tasks)
- Claude Code executes Spec-Kit tools via MCP server for implementation
- MCP server exposes Spec-Kit commands as prompts for all AI agents
- Constitution > Specify > Plan > Tasks hierarchy applies for conflict resolution

### III. Technology Stack Constraints
The following technology choices are NON-NEGOTIABLE:

**Phase I - Console App:**
- Python 3.13+
- UV package manager
- Claude Code for implementation (manual coding NOT allowed)
- Spec-Kit Plus for spec management

**Phase II - Full-Stack Web:**
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT tokens
- Monorepo structure with /frontend and /backend directories

**Phase III - AI Chatbot:**
- Frontend: OpenAI ChatKit
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK for tool exposure
- Backend: Python FastAPI (extended from Phase II)
- Architecture: Stateless chat endpoint with database-persisted conversation state

**Phase IV - Local Kubernetes:**
- Containerization: Docker (Docker Desktop)
- Docker AI: Gordon (for Docker operations)
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AIOps: kubectl-ai, kagent

**Phase V - Cloud Deployment:**
- Kubernetes Cloud: Azure (AKS), Google Cloud (GKE), or DigitalOcean DOKS
- Event Streaming: Kafka (Redpanda Cloud or Confluent)
- Distributed Runtime: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- CI/CD: GitHub Actions

### IV. Evolutionary Development
The project evolves progressively through phases; each phase builds on the previous
- No skipping phases allowed; must complete I → II → III → IV → V in order
- Phase I: In-memory Python console (Basic Level features)
- Phase II: Full-stack web with persistent storage and authentication (Basic Level features)
- Phase III: AI-powered chatbot interface (Basic Level features)
- Phase IV: Local Kubernetes deployment (Basic Level functionality)
- Phase V: Advanced features on cloud (Intermediate + Advanced Level features)

**Feature Levels:**
- **Basic Level (Phases I-III):** Add, Delete, Update, View, Mark Complete
- **Intermediate Level (Phase V):** Priorities & Tags, Search & Filter, Sort Tasks
- **Advanced Level (Phase V):** Recurring Tasks, Due Dates & Time Reminders

### V. Architecture Patterns

**Monorepo Structure:**
- /specs/ organized by type: /features, /api, /database, /ui
- /frontend/ - Next.js application
- /backend/ - FastAPI application
- /.spec-kit/ - Spec-Kit configuration
- /history/ - Prompt History Records (PHRs) and ADRs
- Each subdirectory may have its own CLAUDE.md for context

**API Design:**
- RESTful endpoints for all CRUD operations
- JWT-based authentication for user isolation
- All endpoints require valid JWT token in Authorization: Bearer <token> header
- User data filtering enforced on every operation (users only see their own data)

**Stateless Architecture:**
- Server holds NO state (ready for next request)
- Conversation state stored in database (Neon PostgreSQL)
- Enables horizontal scaling and resilience

**Event-Driven Architecture (Phase V):**
- Kafka for decoupled microservices (task-events, reminders, task-updates topics)
- Dapr for infrastructure abstraction (Pub/Sub, State, Service Invocation, Bindings, Secrets)
- Separate services: Notification Service, Recurring Task Service, Audit Service

### VI. Quality Standards

**Code Quality:**
- Clean code principles with proper project structure
- Type safety required (Python type hints, TypeScript strict mode)
- Error handling with HTTPException (FastAPI) and proper status codes
- No hardcoded secrets or tokens; use environment variables (.env)
- Code must reference Task and Spec sections in comments

**Testing:**
- Tests written before implementation (TDD) where applicable
- Red-Green-Refactor cycle enforced
- Integration tests for: API contracts, database interactions, inter-service communication

**Observability:**
- Structured logging required
- Metrics and traces for production monitoring
- Alerting configured for critical failures

**Documentation:**
- Every feature must have corresponding spec in /specs/
- CLAUDE.md files provide context at different levels (root, frontend, backend)
- README.md with comprehensive setup and deployment instructions
- PHRs (Prompt History Records) created for every user input (verbatim, not truncated)
- ADRs (Architectural Decision Records) for significant decisions (with user consent)

### VII. Authentication & Security

**User Isolation:**
- JWT tokens issued by Better Auth on frontend
- Shared secret (BETTER_AUTH_SECRET) used by both frontend and backend
- Backend middleware verifies JWT on all requests
- Task ownership enforced on every CRUD operation
- Users only see/modify their own tasks

**Security Requirements:**
- No API keys or secrets in code
- Domain allowlist configuration for hosted ChatKit
- Secure secret store via Dapr or Kubernetes Secrets
- Audit trail maintained via Kafka events

### VIII. Agent Behavior Constraints

**What Agents MUST DO:**
- Generate code only with referenced Task ID
- Modify architecture only with speckit.plan update
- Propose features only with speckit.specify update
- Change principles only with constitution.md update
- Reference Task IDs and Spec sections in code comments
- Stop and request clarification if underspecified

**What Agents MUST NOT DO:**
- Freestyle code or architecture
- Generate missing requirements
- Create tasks on their own
- Alter stack choices without justification
- Add endpoints, fields, or flows not in spec
- Ignore acceptance criteria
- Produce "creative" implementations violating plan

## Development Workflow

### Spec-Kit Lifecycle

**1. Constitution (WHY):**
- File: speckit.constitution
- Defines: Architecture values, security rules, tech stack constraints, performance expectations
- Agents must check this before proposing solutions

**2. Specify (WHAT):**
- File: speckit.specify
- Contains: User journeys, requirements, acceptance criteria, domain rules, business constraints
- Agents must not infer missing requirements

**3. Plan (HOW):**
- File: speckit.plan
- Contains: Component breakdown, APIs & schemas, service boundaries, responsibilities, sequencing
- All architectural output MUST be generated from Specify file

**4. Tasks (BREAKDOWN):**
- File: speckit.tasks
- Each Task contains: Task ID, description, preconditions, expected outputs, artifacts to modify, links back to Specify + Plan

**5. Implement (CODE):**
- Agents write code referencing Task IDs, following Plan exactly
- No new features or flows invented
- Stop and request clarification if underspecified

**Golden Rule: No task = No code.**

### MCP Integration

MCP server exposes Spec-Kit commands as prompts:
- `/sp.specify` - Create/update feature specification
- `/sp.plan` - Generate architectural plan
- `/sp.tasks` - Break down plan into actionable tasks
- `/sp.implement` - Execute tasks and implement features
- `/sp.adr` - Create Architectural Decision Records (with user consent)
- `/sp.phr` - Create Prompt History Records

### ADR Creation

When architecturally significant decisions are detected:
- Test for significance: Impact (long-term?), Alternatives (multiple viable options?), Scope (cross-cutting?)
- If ALL true: Suggest "📋 Architectural decision detected: [brief] — Document reasoning and tradeoffs? Run `/sp.adr <title>`"
- Wait for user consent; NEVER auto-create ADRs

## Deliverables & Submission

### Per Phase

**Phase I Deliverables:**
- GitHub repository with constitution file, specs history, /src folder, README.md, CLAUDE.md
- Working console application (Add, Delete, Update, View, Mark Complete)

**Phase II Deliverables:**
- Full-stack monorepo with frontend (Next.js) and backend (FastAPI)
- RESTful API endpoints with JWT authentication
- Neon Serverless PostgreSQL database
- Deployed to Vercel (frontend) + cloud backend

**Phase III Deliverables:**
- AI-powered chatbot (OpenAI ChatKit + Agents SDK + MCP)
- MCP tools for task operations (add_task, list_tasks, complete_task, delete_task, update_task)
- Stateless chat endpoint with database-persisted conversations
- Natural language interface for todo management

**Phase IV Deliverables:**
- Docker containers for frontend and backend
- Helm charts for Kubernetes deployment
- Local Minikube deployment
- AIOps tools configured (kubectl-ai, kagent)

**Phase V Deliverables:**
- Advanced features (Recurring Tasks, Due Dates, Priorities, Tags, Search, Filter, Sort)
- Kafka event streaming (task-events, reminders, task-updates)
- Dapr integration (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- Cloud deployment (Azure AKS / Google GKE / DigitalOcean DOKS)
- CI/CD pipeline (GitHub Actions)
- Monitoring and logging configured

### Final Submission Requirements

1. **Public GitHub Repository** containing:
   - All source code for all completed phases
   - /specs folder with all specification files
   - CLAUDE.md with Claude Code instructions
   - README.md with comprehensive documentation
   - Clear folder structure for each phase

2. **Deployed Application Links:**
   - Phase II: Vercel/frontend URL + Backend API URL
   - Phase III-V: Chatbot URL
   - Phase IV: Instructions for local Minikube setup
   - Phase V: Cloud deployment URL

3. **Demo Video** (maximum 90 seconds):
   - Demonstrate all implemented features
   - Show spec-driven development workflow
   - Judges only watch first 90 seconds

4. **WhatsApp Number** for presentation invitation

## Bonus Opportunities

| Bonus Feature | Points |
| :---- | :---: |
| Reusable Intelligence – Create and use reusable intelligence via Claude Code Subagents and Agent Skills | +200 |
| Create and use Cloud-Native Blueprints via Agent Skills | +200 |
| Multi-language Support – Support Urdu in chatbot | +100 |
| Voice Commands – Add voice input for todo commands | +200 |
| **TOTAL BONUS** | **+600** |

## Governance

**Constitution Supremacy:**
- Constitution supersedes all other practices and configuration files
- All PRs/reviews must verify compliance with constitution principles
- Complexity must be justified against principles

**Amendments:**
- Constitution changes require documentation, approval, and migration plan
- Amendments must update all dependent templates to maintain sync

**Agent Compliance:**
- Every agent (Claude, Copilot, Gemini, local LLMs) must follow Constitution
- Before every session, agents re-read `.specify/memory/constitution.md`
- Non-compliance is a failure mode that must be corrected

**Versioning:**
- Constitution version: MAJOR.MINOR.PATCH
- Major changes: Core principles, tech stack, phase structure
- Minor changes: Process refinements, clarifications
- Patch changes: Typo fixes, formatting

**Version**: 1.0.0 | **Ratified**: 2025-12-01 | **Last Amended**: 2025-12-01

---

*This Constitution governs all development activities for Hackathon II: The Evolution of Todo. Non-compliance may result in point deductions or disqualification.*

**Project Team:** Panaversity, PIAIC, and GIAIC
**Contact:** Panaversity Founders (Zia, Rehan, Junaid, Wania)
**Documentation:** https://ai-native.panaversity.org/docs
