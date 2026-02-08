# ✅ FINAL FIX - Add OpenRouter API Key

## 🚨 The Missing Piece

Your `.env` file has `DATABASE_URL` and `BETTER_AUTH_SECRET`, but it's **missing `OPENROUTER_API_KEY`** which is required for AI chat in Phase 3.

---

## 🔑 Get Your OpenRouter API Key (2 minutes)

### Step 1: Sign Up
1. Go to https://openrouter.ai
2. Click "Sign Up" (free account)
3. Complete registration

### Step 2: Get Free Credits
- New users get **$5 free credits**
- No credit card required to start

### Step 3: Create API Key
1. Go to https://openrouter.ai/keys
2. Click "Create Key"
3. Give it a name (e.g., "Todo App")
4. Copy the key (starts with `sk-or-v1-`)

### Step 4: Add to .env File

Open `phase-3/backend/.env` and replace this line:
```env
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

With your actual key:
```env
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 🚀 Run Docker Now

After adding the API key:

**Option 1: Use Test Script (Easiest)**
```bash
cd phase-3/backend
test-docker.bat
```

**Option 2: Manual Docker Run**
```bash
cd phase-3/backend

# Build image
docker build -t phase3-backend .

# Run with .env file
docker run -p 7860:7860 --env-file .env phase3-backend
```

---

## ✅ Expected Output

After adding the API key, you should see:

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
  ✓ OPENROUTER_API_KEY is set          ← This should now pass!
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

## 🧪 Test the API

Once running:

```bash
# Test health
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

# Open API docs
start http://localhost:7860/docs  # Windows
open http://localhost:7860/docs   # Mac
```

---

## 💰 OpenRouter Pricing

Don't worry about costs:
- **Free Credits**: $5 for new users
- **Claude 3.5 Sonnet**: ~$3 per million tokens
- **Typical Usage**: 100 chat messages ≈ $0.10-$0.50
- **Your $5 credit**: ~500-1000 chat messages

---

## 🎯 Quick Summary

1. **Get API Key**: https://openrouter.ai/keys (2 min)
2. **Add to .env**: Replace `your-openrouter-api-key-here` with actual key
3. **Run Docker**: `test-docker.bat` or `docker run -p 7860:7860 --env-file .env phase3-backend`
4. **Test**: `curl http://localhost:7860/health`

---

## 🆘 Still Having Issues?

### Check .env File
```bash
# View your .env file
type .env  # Windows
cat .env   # Linux/Mac

# Make sure it has:
# - DATABASE_URL=postgresql://...
# - BETTER_AUTH_SECRET=...
# - OPENROUTER_API_KEY=sk-or-v1-...
```

### Verify API Key Format
```
✓ Correct: sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
✗ Wrong: your-openrouter-api-key-here
✗ Wrong: "sk-or-v1-..." (no quotes)
```

### Test API Key
```bash
# Test if your OpenRouter key works
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer sk-or-v1-your-key-here"
```

---

**Your next command:**
```bash
cd phase-3/backend
test-docker.bat
```

This will work once you add the OpenRouter API key! 🚀
