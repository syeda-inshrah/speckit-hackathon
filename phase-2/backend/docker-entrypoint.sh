#!/bin/sh
set -e

echo "=========================================="
echo "Todo Backend API - Starting"
echo "=========================================="
echo ""

# Print environment info
echo "Environment Check:"
echo "  Python: $(python --version)"
echo "  Working directory: $(pwd)"
echo "  User: $(whoami)"
echo ""

# Check required environment variables
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set!"
    echo "Please set it in Space settings > Variables and secrets"
    exit 1
fi
echo "  ✓ DATABASE_URL is set"

if [ -z "$BETTER_AUTH_SECRET" ]; then
    echo "ERROR: BETTER_AUTH_SECRET is not set!"
    echo "Please set it in Space settings > Variables and secrets"
    exit 1
fi
echo "  ✓ BETTER_AUTH_SECRET is set"

echo "  ✓ FRONTEND_URL: ${FRONTEND_URL:-http://localhost:3000}"
echo ""

# Verify application files
echo "Verifying application structure..."
if [ ! -f "/app/app.py" ]; then
    echo "ERROR: app.py not found!"
    exit 1
fi
echo "  ✓ app.py found"

if [ ! -d "/app/src" ]; then
    echo "ERROR: src directory not found!"
    exit 1
fi
echo "  ✓ src directory found"
echo ""

# Run database migrations
echo "Running database migrations..."
if alembic upgrade head 2>&1; then
    echo "  ✓ Migrations completed"
else
    echo "  ⚠ Migrations failed (tables may already exist)"
fi
echo ""

# Determine port (7860 for Hugging Face, 8000 for local)
PORT=${PORT:-7860}

# Start the application
echo "Starting FastAPI application..."
echo "  Host: 0.0.0.0"
echo "  Port: $PORT"
echo "  Entry: app:app"
echo ""
echo "=========================================="
echo ""

# Use exec to replace shell with uvicorn process
exec uvicorn app:app --host 0.0.0.0 --port $PORT --log-level info
