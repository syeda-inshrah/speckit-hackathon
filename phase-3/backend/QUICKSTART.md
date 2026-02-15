# Quick Start Guide - Phase 3 Backend

## 🚨 Fixing "DATABASE_URL is not set" Error

This error means the environment variables are not configured. Here's how to fix it:

---

## 🔧 Option 1: Test Locally (Recommended First)

### Step 1: Set Up Environment Variables

```bash
cd phase-3/backend

# Copy example file
cp .env.example .env

# Edit .env with your values
# Windows: notepad .env
# Mac/Linux: nano .env
```

Your `.env` should have:

**Option A: Using OpenRouter (Multiple Models)**
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-generated-secret-here
LLM_PROVIDER=OPENROUTER
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
FRONTEND_URL=http://localhost:3000
```

**Option B: Using Groq (Ultra-Fast)**
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-generated-secret-here
LLM_PROVIDER=GROQ
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
GROQ_MODEL=llama-3.3-70b-versatile
FRONTEND_URL=http://localhost:3000
```

### Step 2: Run Test Script

**Windows:**
```bash
test-docker.bat
```

**Linux/Mac:**
```bash
chmod +x test-docker.sh
./test-docker.sh
```

The script will:
- ✅ Validate all environment variables
- ✅ Build Docker image
- ✅ Run container on port 7860
- ✅ Show logs in real-time

### Step 3: Test the API

```bash
# In another terminal
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

## 🌐 Option 2: Deploy to Hugging Face Spaces

If you're deploying to HF Spaces, you need to configure secrets there:

### Step 1: Go to Your Space Settings

1. Open your Space on Hugging Face
2. Click **Settings** tab
3. Scroll to **Variables and secrets**

### Step 2: Add Required Secrets

Add these three secrets (click **Add** after each):

**DATABASE_URL:**
```
postgresql://user:password@host/database?sslmode=require
```
Get from: https://neon.tech

**BETTER_AUTH_SECRET:**
```
X9Wk9_Pqznh1o6aAIHSd8xvOqy5iy21QqNH_-9k8cxU
```
Generate with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**LLM_PROVIDER:**
```
OPENROUTER
```
Or use `GROQ` for ultra-fast inference

**OPENROUTER_API_KEY** (if using OpenRouter):
```
sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Get from: https://openrouter.ai/keys

**GROQ_API_KEY** (if using Groq):
```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
Get from: https://console.groq.com/keys

### Step 3: Add Optional Secrets

**OPENROUTER_MODEL** (optional):
```
anthropic/claude-3.5-sonnet
```

**GROQ_MODEL** (optional):
```
llama-3.3-70b-versatile
```

**FRONTEND_URL** (optional):
```
https://your-frontend.vercel.app
```

### Step 4: Restart Space

After adding all secrets:
1. Click **Factory reboot** in Settings
2. Wait for Space to rebuild (5-10 minutes)
3. Check Logs tab for startup messages

---

## 🧪 Option 3: Run Without Docker (Local Development)

```bash
cd phase-3/backend

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Set environment variables
# Windows (PowerShell):
$env:DATABASE_URL="postgresql://..."
$env:BETTER_AUTH_SECRET="your-secret"
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Linux/Mac:
export DATABASE_URL="postgresql://..."
export BETTER_AUTH_SECRET="your-secret"
export OPENROUTER_API_KEY="sk-or-v1-..."

# Run with uvicorn
uvicorn app:app --host 0.0.0.0 --port 7860 --reload

# Or run app.py directly
python app.py
```

---

## 📋 Environment Variables Checklist

### Required (Must Have)
- [ ] `DATABASE_URL` - PostgreSQL connection string
- [ ] `BETTER_AUTH_SECRET` - JWT secret (32+ characters)
- [ ] `LLM_PROVIDER` - Choose: `OPENROUTER` or `GROQ`
- [ ] `OPENROUTER_API_KEY` - Required if using OpenRouter
- [ ] `GROQ_API_KEY` - Required if using Groq

### Optional (Have Defaults)
- [ ] `OPENROUTER_MODEL` - Default: `anthropic/claude-3.5-sonnet`
- [ ] `GROQ_MODEL` - Default: `llama-3.3-70b-versatile`
- [ ] `FRONTEND_URL` - Default: `http://localhost:3000`
- [ ] `OPENROUTER_BASE_URL` - Default: `https://openrouter.ai/api/v1`
- [ ] `GROQ_BASE_URL` - Default: `https://api.groq.com/openai/v1`
- [ ] `JWT_ALGORITHM` - Default: `HS256`
- [ ] `JWT_EXPIRATION_DAYS` - Default: `7`

---

## 🎯 Quick Setup Commands

### Get Database (Neon)
```bash
# 1. Go to https://neon.tech
# 2. Sign up (free)
# 3. Create project
# 4. Copy connection string
# Format: postgresql://user:pass@host/db?sslmode=require
```

### Get LLM API Key

**Option A: OpenRouter (Multiple Models)**
```bash
# 1. Go to https://openrouter.ai
# 2. Sign up (free $5 credits)
# 3. Go to https://openrouter.ai/keys
# 4. Create new key
# 5. Copy key (starts with sk-or-v1-)
# 6. Set LLM_PROVIDER=OPENROUTER in .env
```

**Option B: Groq (Ultra-Fast)**
```bash
# 1. Go to https://console.groq.com
# 2. Sign up (free tier)
# 3. Go to https://console.groq.com/keys
# 4. Create new key
# 5. Copy key (starts with gsk_)
# 6. Set LLM_PROVIDER=GROQ in .env
```

### Generate JWT Secret
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## ✅ Verification Steps

After setting up environment variables:

### 1. Check Environment
```bash
# Windows
echo %DATABASE_URL%
echo %BETTER_AUTH_SECRET%
echo %OPENROUTER_API_KEY%

# Linux/Mac
echo $DATABASE_URL
echo $BETTER_AUTH_SECRET
echo $OPENROUTER_API_KEY
```

### 2. Test Docker Build
```bash
docker build -t phase3-backend .
```

### 3. Test Container Run
```bash
docker run -p 7860:7860 --env-file .env phase3-backend
```

### 4. Test Health Endpoint
```bash
curl http://localhost:7860/health
```

---

## 🐛 Common Issues

### Issue: "DATABASE_URL is not set"
**Cause**: Environment variables not loaded
**Solution**:
- Local: Create `.env` file with all variables
- HF Spaces: Add secrets in Space settings

### Issue: "OPENROUTER_API_KEY is not set" or "GROQ_API_KEY is not set"
**Cause**: Missing AI API key for selected provider
**Solution**:
- OpenRouter: Get key from https://openrouter.ai/keys
- Groq: Get key from https://console.groq.com/keys
- Make sure `LLM_PROVIDER` matches your API key

### Issue: ".env file not found"
**Cause**: No .env file in directory
**Solution**:
```bash
cp .env.example .env
# Then edit .env with your values
```

### Issue: "Connection refused to database"
**Cause**: Invalid DATABASE_URL
**Solution**:
- Verify URL format: `postgresql://user:pass@host/db?sslmode=require`
- Check database is active in Neon dashboard

---

## 💡 Pro Tips

1. **Test locally first** - Verify everything works before deploying to HF
2. **Use test scripts** - `test-docker.bat` or `test-docker.sh` automate setup
3. **Check logs** - Always check container logs for errors
4. **Verify secrets** - Double-check all environment variables are set correctly
5. **Start with free tiers** - Neon and OpenRouter both have free options

---

## 📞 Need Help?

If you're still having issues:

1. **Check .env file exists**: `ls -la .env` or `dir .env`
2. **Verify .env format**: No quotes around values
3. **Check Docker is running**: `docker ps`
4. **View container logs**: `docker logs phase3-backend`
5. **Test without Docker**: Run `python app.py` directly

---

## 🎉 Success Indicators

You'll know it's working when:
- ✅ Container starts without errors
- ✅ Health endpoint returns 200 OK
- ✅ Logs show "Application startup complete"
- ✅ Can access API docs at http://localhost:7860/docs

---

**Next Step**: Use the test scripts (`test-docker.bat` or `test-docker.sh`) to validate your setup!
