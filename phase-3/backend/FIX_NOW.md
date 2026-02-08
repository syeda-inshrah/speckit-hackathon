# 🚨 IMMEDIATE FIX - Environment Variables Not Set

## The Problem

Your Docker container is working correctly! It's validating that required environment variables are set before starting. The error means you need to configure:

1. `DATABASE_URL` - PostgreSQL connection string
2. `BETTER_AUTH_SECRET` - JWT secret key
3. `OPENROUTER_API_KEY` - AI API key

---

## ✅ SOLUTION - 3 Simple Steps

### Step 1: Check Your .env File

```bash
cd phase-3/backend

# Check if .env exists
dir .env  # Windows
ls -la .env  # Linux/Mac
```

**If .env doesn't exist:**
```bash
# Copy the example
copy .env.example .env  # Windows
cp .env.example .env  # Linux/Mac
```

### Step 2: Edit .env File

Open `.env` in a text editor and set these values:

```env
# Required - Get from https://neon.tech
DATABASE_URL=postgresql://neondb_owner:npg_qhZgFa9Ls1Jz@ep-billowing-violet-ahbfodkd-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require

# Required - Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
BETTER_AUTH_SECRET=X9Wk9_Pqznh1o6aAIHSd8xvOqy5iy21QqNH_-9k8cxU

# Required - Get from https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# Optional (have defaults)
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
FRONTEND_URL=http://localhost:3000
```

### Step 3: Run Docker with Environment Variables

**Option A: Use Test Script (Easiest)**
```bash
# Windows
test-docker.bat

# Linux/Mac
chmod +x test-docker.sh
./test-docker.sh
```

**Option B: Manual Docker Run**
```bash
# Build image
docker build -t phase3-backend .

# Run with .env file
docker run -p 7860:7860 --env-file .env phase3-backend
```

**Option C: Pass Variables Directly**
```bash
docker run -p 7860:7860 \
  -e DATABASE_URL="postgresql://user:pass@host/db?sslmode=require" \
  -e BETTER_AUTH_SECRET="your-secret-here" \
  -e OPENROUTER_API_KEY="sk-or-v1-your-key" \
  phase3-backend
```

---

## 🎯 For Hugging Face Spaces Deployment

If you're deploying to HF Spaces (not testing locally):

### 1. Go to Your Space
```
https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME
```

### 2. Click Settings Tab

### 3. Scroll to "Variables and secrets"

### 4. Add These Secrets

Click **Add** after each:

**DATABASE_URL:**
```
postgresql://user:password@host/database?sslmode=require
```

**BETTER_AUTH_SECRET:**
```
your-generated-secret-here
```

**OPENROUTER_API_KEY:**
```
sk-or-v1-xxxxxxxxxxxxx
```

### 5. Restart Space

Click **Factory reboot** in Settings

---

## 🔑 How to Get Required Values

### DATABASE_URL (Neon)
```bash
1. Go to https://neon.tech
2. Sign up (free)
3. Create new project
4. Click "Connection Details"
5. Copy connection string
6. Make sure it ends with ?sslmode=require
```

### BETTER_AUTH_SECRET (Generate)
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### OPENROUTER_API_KEY (OpenRouter)
```bash
1. Go to https://openrouter.ai
2. Sign up (free $5 credits)
3. Go to https://openrouter.ai/keys
4. Click "Create Key"
5. Copy the key (starts with sk-or-v1-)
```

---

## ✅ Verify It's Working

After setting environment variables:

```bash
# Test health endpoint
curl http://localhost:7860/health

# Expected response:
{
  "status": "healthy",
  "service": "todo-backend-ai",
  "version": "2.0.0",
  "features": {
    "auth": "enabled",
    "tasks": "enabled",
    "ai_chat": "enabled"
  }
}
```

---

## 🐛 Still Having Issues?

### Check .env Format
```bash
# Correct format (NO quotes):
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=X9Wk9_Pqznh1o6aAIHSd8xvOqy5iy21QqNH_-9k8cxU

# Wrong format (WITH quotes):
DATABASE_URL="postgresql://..."  # ❌ Don't use quotes
BETTER_AUTH_SECRET='...'         # ❌ Don't use quotes
```

### Check Docker is Running
```bash
docker ps
```

### View Container Logs
```bash
docker logs phase3-backend
```

### Test Without Docker
```bash
cd phase-3/backend
.venv\Scripts\activate  # Windows
python app.py
```

---

## 📋 Quick Checklist

- [ ] .env file exists in phase-3/backend/
- [ ] DATABASE_URL is set (from Neon)
- [ ] BETTER_AUTH_SECRET is set (generated)
- [ ] OPENROUTER_API_KEY is set (from OpenRouter)
- [ ] No quotes around values in .env
- [ ] Docker is running
- [ ] Built image: `docker build -t phase3-backend .`
- [ ] Run with: `docker run -p 7860:7860 --env-file .env phase3-backend`

---

## 🎉 Success Indicators

You'll know it's working when you see:

```
==========================================
Todo Backend API with AI Chat - Starting
==========================================

Environment Check:
  Python: Python 3.13.12
  Working directory: /app
  User: appuser

Checking environment variables...
  ✓ DATABASE_URL is set
  ✓ BETTER_AUTH_SECRET is set
  ✓ OPENROUTER_API_KEY is set
  ✓ FRONTEND_URL: http://localhost:3000
  ✓ OPENROUTER_MODEL: anthropic/claude-3.5-sonnet

Verifying application structure...
  ✓ app.py found
  ✓ src directory found

Running database migrations...
  ✓ Migrations completed

Starting FastAPI application...
  Host: 0.0.0.0
  Port: 7860
  Entry: app:app
  Features: Auth, Tasks, AI Chat

INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7860
```

---

**Your Next Command:**

```bash
cd phase-3/backend
test-docker.bat
```

This will validate everything and start the container! 🚀
