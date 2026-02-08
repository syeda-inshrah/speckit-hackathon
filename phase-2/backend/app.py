"""
FastAPI Application Entry Point
Root-level entry point for the Todo Backend API
Can be used with: uvicorn app:app --reload --port 8000
"""

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import core components
from src.core.config import settings
from src.core.database import init_db, engine
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup: Initialize database tables (development only)
    print("🚀 Starting Todo Backend API...")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print(f"🌐 CORS enabled for: {settings.FRONTEND_URL}")

    # Uncomment to auto-create tables on startup (use Alembic migrations in production)
    # await init_db()

    yield

    # Shutdown: Cleanup
    print("👋 Shutting down Todo Backend API...")
    await engine.dispose()


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Multi-user todo application API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api", tags=["Authentication"])
app.include_router(tasks_router, prefix="/api", tags=["Tasks"])


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring and load balancers"""
    return {
        "status": "healthy",
        "service": "todo-backend",
        "version": "1.0.0",
    }


@app.get("/api/info", tags=["Info"])
async def api_info():
    """API information and available endpoints"""
    return {
        "api_version": "1.0.0",
        "endpoints": {
            "auth": {
                "signup": "POST /api/auth/signup",
                "signin": "POST /api/auth/signin",
            },
            "tasks": {
                "list": "GET /api/{user_id}/tasks",
                "create": "POST /api/{user_id}/tasks",
                "get": "GET /api/{user_id}/tasks/{task_id}",
                "update": "PUT /api/{user_id}/tasks/{task_id}",
                "toggle": "PATCH /api/{user_id}/tasks/{task_id}/complete",
                "delete": "DELETE /api/{user_id}/tasks/{task_id}",
            },
        },
        "authentication": "JWT Bearer Token required for task endpoints",
    }


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
