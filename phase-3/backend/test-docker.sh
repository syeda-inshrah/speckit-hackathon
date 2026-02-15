#!/bin/bash
# Local Docker Test Script for Phase 3 Backend

echo "=========================================="
echo "Phase 3 Backend - Local Docker Test"
echo "=========================================="
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "Please edit .env file with your actual values:"
    echo "  1. DATABASE_URL - Your Neon database URL"
    echo "  2. BETTER_AUTH_SECRET - Generate with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
    echo "  3. LLM_PROVIDER - Choose: OPENROUTER or GROQ"
    echo "  4. OPENROUTER_API_KEY - Get from https://openrouter.ai/keys (if using OpenRouter)"
    echo "  5. GROQ_API_KEY - Get from https://console.groq.com/keys (if using Groq)"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "Loading environment variables from .env..."
source .env

# Verify required variables
if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set in .env file"
    exit 1
fi

if [ -z "$BETTER_AUTH_SECRET" ]; then
    echo "ERROR: BETTER_AUTH_SECRET is not set in .env file"
    exit 1
fi

# Check LLM provider configuration
LLM_PROVIDER=${LLM_PROVIDER:-OPENROUTER}

if [ "$LLM_PROVIDER" = "GROQ" ]; then
    if [ -z "$GROQ_API_KEY" ]; then
        echo "ERROR: GROQ_API_KEY is not set in .env file"
        echo "Get your key from: https://console.groq.com/keys"
        exit 1
    fi
    echo "✓ Using Groq provider"
else
    if [ -z "$OPENROUTER_API_KEY" ]; then
        echo "ERROR: OPENROUTER_API_KEY is not set in .env file"
        echo "Get your key from: https://openrouter.ai/keys"
        exit 1
    fi
    echo "✓ Using OpenRouter provider"
fi

echo "✓ All required environment variables are set"
echo ""

# Build Docker image
echo "Building Docker image..."
docker build -t phase3-backend .

if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi

echo "✓ Docker image built successfully"
echo ""

# Run container
echo "Starting container on port 7860..."
docker run -p 7860:7860 \
  -e DATABASE_URL="$DATABASE_URL" \
  -e BETTER_AUTH_SECRET="$BETTER_AUTH_SECRET" \
  -e LLM_PROVIDER="${LLM_PROVIDER:-OPENROUTER}" \
  -e OPENROUTER_API_KEY="$OPENROUTER_API_KEY" \
  -e OPENROUTER_MODEL="${OPENROUTER_MODEL:-anthropic/claude-3.5-sonnet}" \
  -e GROQ_API_KEY="$GROQ_API_KEY" \
  -e GROQ_MODEL="${GROQ_MODEL:-llama-3.3-70b-versatile}" \
  -e FRONTEND_URL="${FRONTEND_URL:-http://localhost:3000}" \
  --name phase3-backend \
  phase3-backend

echo ""
echo "Container stopped. To remove:"
echo "  docker rm phase3-backend"
