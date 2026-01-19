# Phase II: Full-Stack Web Application

**Status**: ✅ Implementation Complete
**Branch**: `002-fullstack-web-app`
**Date**: 2026-01-11

## Overview

Multi-user todo application with secure authentication and persistent storage. Built following Spec-Driven Development (SDD) principles with complete specification, architectural plan, and task breakdown.

## Features Implemented

### Authentication (User Story 1 - P1) 🎯 MVP
- ✅ User registration with email validation
- ✅ Secure signin with JWT tokens
- ✅ Password hashing (bcrypt, 12 rounds)
- ✅ Protected routes with middleware
- ✅ Session management and signout

### Task Management (User Stories 2-5)
- ✅ Create tasks with title and description
- ✅ View all tasks (organized by completion status)
- ✅ Mark tasks as complete/incomplete
- ✅ Edit task details (inline editing)
- ✅ Delete tasks with confirmation
- ✅ User isolation (users only see their own tasks)

## Technology Stack

### Frontend
- **Framework**: Next.js 16.1.1 (App Router)
- **Language**: TypeScript 5.7.2 (strict mode)
- **Styling**: Tailwind CSS 4.0.0
- **State Management**: React hooks (useState, useEffect)
- **Authentication**: JWT tokens with localStorage

### Backend
- **Framework**: FastAPI 0.128.0
- **Language**: Python 3.13+
- **ORM**: SQLModel 0.0.31 (async)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT (python-jose, HS256)
- **Password Hashing**: Passlib with bcrypt
- **Migrations**: Alembic 1.18.0

## Project Structure

```
phase-2/
├── backend/
│   ├── src/
│   │   ├── main.py                 # FastAPI app with CORS
│   │   ├── models/
│   │   │   ├── user.py            # User SQLModel
│   │   │   └── task.py            # Task SQLModel
│   │   ├── schemas/
│   │   │   ├── auth.py            # Auth Pydantic schemas
│   │   │   └── task.py            # Task Pydantic schemas
│   │   ├── api/
│   │   │   ├── auth.py            # Auth endpoints
│   │   │   └── tasks.py           # Task CRUD endpoints
│   │   ├── core/
│   │   │   ├── config.py          # Settings management
│   │   │   ├── database.py        # Async DB connection
│   │   │   ├── security.py        # Password hashing
│   │   │   └── jwt.py             # JWT token functions
│   │   └── middleware/
│   │       └── auth.py            # JWT authentication
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial.py     # Initial migration
│   │   └── env.py                 # Alembic config
│   ├── pyproject.toml             # Dependencies
│   ├── alembic.ini                # Migration config
│   ├── .env.example               # Environment template
│   └── README.md                  # Backend documentation
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── (auth)/
    │   │   │   ├── signup/page.tsx
    │   │   │   └── signin/page.tsx
    │   │   ├── (dashboard)/
    │   │   │   ├── layout.tsx      # Dashboard layout
    │   │   │   └── dashboard/page.tsx
    │   │   ├── layout.tsx          # Root layout
    │   │   ├── page.tsx            # Home page
    │   │   └── globals.css         # Global styles
    │   ├── components/
    │   │   ├── auth/
    │   │   │   ├── SignupForm.tsx
    │   │   │   └── SigninForm.tsx
    │   │   └── tasks/
    │   │       ├── TaskCard.tsx    # Task display/edit/delete
    │   │       ├── TaskList.tsx    # Task organization
    │   │       └── CreateTaskForm.tsx
    │   ├── lib/
    │   │   └── api-client.ts       # API wrapper with JWT
    │   └── middleware.ts           # Route protection
    ├── package.json                # Dependencies
    ├── tailwind.config.ts          # Tailwind config
    ├── tsconfig.json               # TypeScript config
    └── .env.example                # Environment template
```

## Setup Instructions

### Prerequisites

- **Node.js**: 18+ ([Download](https://nodejs.org/))
- **Python**: 3.13+ ([Download](https://www.python.org/))
- **UV**: Latest (`pip install uv`)
- **Neon Account**: [Sign up](https://neon.tech) (free tier)

### 1. Database Setup

**Create Neon Database:**
1. Go to [Neon Console](https://console.neon.tech)
2. Create a new project
3. Copy the connection string (format: `postgresql://user:pass@host/db`)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd phase-2/backend

# Install dependencies
uv sync

# Create .env file
cp .env.example .env

# Edit .env with your values:
# - DATABASE_URL: Your Neon connection string
# - BETTER_AUTH_SECRET: Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
# - FRONTEND_URL: http://localhost:3000

# Run database migrations
uv run alembic upgrade head

# Start backend server
uv run uvicorn src.main:app --reload --port 8000
```

Backend will be available at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd phase-2/frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local

# Edit .env.local with your values:
# - NEXT_PUBLIC_API_URL: http://localhost:8000
# - BETTER_AUTH_SECRET: Same secret as backend

# Start frontend server
npm run dev
```

Frontend will be available at: **http://localhost:3000**

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | Register new user | No |
| POST | `/api/auth/signin` | Authenticate user | No |

### Tasks

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/{user_id}/tasks` | List all user tasks | Yes |
| POST | `/api/{user_id}/tasks` | Create new task | Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get specific task | Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |

**Authentication**: All protected endpoints require `Authorization: Bearer <jwt-token>` header.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE INDEX ix_tasks_user_id ON tasks(user_id);
CREATE INDEX ix_tasks_completed ON tasks(completed);
CREATE INDEX ix_tasks_created_at ON tasks(created_at);
```

## Testing the Application

### 1. Create Account
1. Navigate to http://localhost:3000
2. Click "Get Started" or "Sign Up"
3. Enter email, password (min 8 chars), and name
4. Submit form → You'll be automatically signed in

### 2. Create Tasks
1. On the dashboard, click "+ Add New Task"
2. Enter task title (required)
3. Optionally add description
4. Click "Create Task"

### 3. Manage Tasks
- **Mark Complete**: Click checkbox next to task
- **Edit Task**: Click edit icon, modify title/description, save
- **Delete Task**: Click delete icon, confirm deletion

### 4. Sign Out
1. Click "Sign Out" button in header
2. You'll be redirected to signin page

## Security Features

- ✅ **Password Hashing**: Bcrypt with 12 salt rounds
- ✅ **JWT Tokens**: HS256 algorithm, 7-day expiry
- ✅ **User Isolation**: Database-level filtering by user_id
- ✅ **Protected Routes**: Middleware redirects unauthenticated users
- ✅ **Input Validation**: Pydantic schemas validate all inputs
- ✅ **CORS Configuration**: Only allows configured frontend origin

## Development

### Running Tests

```bash
# Backend tests (when implemented)
cd phase-2/backend
uv run pytest

# Frontend tests (when implemented)
cd phase-2/frontend
npm test
```

### Code Formatting

```bash
# Backend
cd phase-2/backend
uv run black src/
uv run isort src/

# Frontend
cd phase-2/frontend
npm run lint
```

## Deployment

### Frontend (Vercel)

1. Push code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import repository
4. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend URL
   - `BETTER_AUTH_SECRET`: Same secret as backend
5. Deploy

### Backend (Railway/Render/Vercel)

**Railway:**
1. Go to [Railway](https://railway.app)
2. New Project → Deploy from GitHub
3. Select backend directory
4. Set environment variables
5. Deploy

**Render:**
1. Go to [Render](https://render.com)
2. New Web Service → Connect repository
3. Set build command: `cd phase-2/backend && uv sync`
4. Set start command: `cd phase-2/backend && uv run uvicorn src.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables
6. Deploy

## Troubleshooting

### Backend won't start
- **Error**: `ModuleNotFoundError`
- **Solution**: Run `uv sync` in backend directory

### Database connection error
- **Error**: `could not connect to server`
- **Solution**:
  1. Verify DATABASE_URL in `.env` is correct
  2. Check Neon database is active
  3. Ensure IP is whitelisted in Neon console

### CORS error in browser
- **Error**: `Access to fetch blocked by CORS policy`
- **Solution**:
  1. Verify FRONTEND_URL in backend `.env` matches frontend URL
  2. Restart backend server after changing `.env`

### JWT token invalid
- **Error**: `Invalid or expired token`
- **Solution**:
  1. Verify BETTER_AUTH_SECRET is the SAME in both frontend and backend
  2. Sign out and sign in again to get new token

## Constitution Compliance

This implementation follows all requirements from `.specify/memory/constitution.md`:

- ✅ **Spec-Driven Development**: Followed Specify → Plan → Tasks → Implement lifecycle
- ✅ **Technology Stack**: All required technologies used (Next.js 16+, FastAPI, SQLModel, Neon, JWT)
- ✅ **Basic Level Features**: All 5 features implemented (Add, Delete, Update, View, Mark Complete)
- ✅ **Architecture Patterns**: RESTful API, JWT auth, user isolation, stateless design
- ✅ **Security**: Password hashing, JWT verification, user isolation enforced
- ✅ **Code Quality**: Type safety, error handling, environment variables

## Documentation

- **Specification**: `specs/002-fullstack-web-app/spec.md`
- **Architectural Plan**: `specs/002-fullstack-web-app/plan.md`
- **Task Breakdown**: `specs/002-fullstack-web-app/tasks.md`
- **Data Model**: `specs/002-fullstack-web-app/data-model.md`
- **API Contracts**: `specs/002-fullstack-web-app/contracts/openapi.yaml`
- **Quickstart Guide**: `specs/002-fullstack-web-app/quickstart.md`

## Next Steps

1. **Add Tests**: Implement unit and integration tests (TDD)
2. **Deploy**: Deploy frontend to Vercel and backend to cloud
3. **Phase III**: Implement AI chatbot interface with OpenAI ChatKit
4. **Phase IV**: Containerize with Docker and deploy to Kubernetes
5. **Phase V**: Add advanced features and cloud deployment

## License

This project is part of Hackathon II: The Evolution of Todo by Panaversity, PIAIC, and GIAIC.

## Contact

For questions or issues, refer to the [Panaversity Documentation](https://ai-native.panaversity.org/docs).

---

**Implementation Status**: ✅ Phase II Complete
**Constitution Compliance**: ✅ All requirements met
**Ready for**: Testing, Deployment, and Phase III
