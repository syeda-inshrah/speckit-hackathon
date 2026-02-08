# Todo Backend

FastAPI backend for multi-user todo application with JWT authentication.

## Features

- User authentication (signup/signin)
- JWT token-based authorization
- Task CRUD operations
- User isolation (users only see their own tasks)
- PostgreSQL database with SQLModel ORM

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Create `.env` file with required variables (see `.env.example`)

3. Run database migrations:
```bash
uv run alembic upgrade head
```

4. Start development server:
```bash
uv run uvicorn src.main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
