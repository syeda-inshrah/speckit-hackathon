---
title: Todo AI Assistant API
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Todo AI Assistant API 🤖

A production-ready FastAPI backend for multi-user todo application with **AI-powered chat assistant**. Manage your tasks using natural language!

## 🌟 Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **Multi-user Support** - Complete user isolation
- 📝 **Task Management** - Full CRUD operations
- 🤖 **AI Chat Assistant** - Natural language task management
- 🗄️ **PostgreSQL Database** - Persistent storage with async support
- ⚡ **FastAPI** - High-performance async API
- 📚 **Auto Documentation** - Interactive Swagger UI

## 🤖 AI Chat Features

The AI assistant can help you:
- ✅ Create tasks from natural language
- ✅ Update and modify existing tasks
- ✅ Mark tasks as complete
- ✅ Search and filter tasks
- ✅ Get task summaries and insights
- ✅ Understand context from conversation history

**Example conversations:**
- "Create a task to buy groceries tomorrow"
- "Show me all my pending tasks"
- "Mark the grocery task as complete"
- "What tasks do I have for this week?"

## 🚀 Quick Start

### Access the API

Once deployed, access:
- **API Docs**: `https://YOUR-USERNAME-SPACE-NAME.hf.space/docs`
- **Health Check**: `https://YOUR-USERNAME-SPACE-NAME.hf.space/health`
- **API Info**: `https://YOUR-USERNAME-SPACE-NAME.hf.space/api/info`

### Test the API

```bash
# Health check
curl https://YOUR-USERNAME-SPACE-NAME.hf.space/health

# Create user
curl -X POST https://YOUR-USERNAME-SPACE-NAME.hf.space/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Sign in
curl -X POST https://YOUR-USERNAME-SPACE-NAME.hf.space/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Chat with AI (use token from signin)
curl -X POST https://YOUR-USERNAME-SPACE-NAME.hf.space/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"Create a task to finish the project report","user_id":"USER_ID"}'
```

## ⚙️ Configuration

### Required Secrets

Configure these in **Space Settings > Variables and secrets**:

#### 1. DATABASE_URL (Required)
Your PostgreSQL connection string from [Neon](https://neon.tech)

```
postgresql://user:password@host/database?sslmode=require
```

#### 2. BETTER_AUTH_SECRET (Required)
JWT secret key (minimum 32 characters)

Generate with:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 3. LLM_PROVIDER (Optional)
Choose your LLM provider. Default: `OPENROUTER`

Options:
- `OPENROUTER` - Multiple models, pay-as-you-go
- `GROQ` - Ultra-fast inference, free tier

#### 4. OPENROUTER_API_KEY (Required if using OpenRouter)
Your OpenRouter API key for AI chat functionality

Get your key from: [OpenRouter](https://openrouter.ai/keys)

```
sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 5. OPENROUTER_MODEL (Optional)
AI model to use. Default: `anthropic/claude-3.5-sonnet`

Available models:
- `anthropic/claude-3.5-sonnet` (Recommended)
- `openai/gpt-4-turbo`
- `anthropic/claude-3-opus`
- `meta-llama/llama-3.1-70b-instruct`
- `google/gemini-pro-1.5`

#### 6. GROQ_API_KEY (Required if using Groq)
Your Groq API key for ultra-fast AI inference

Get your key from: [Groq Console](https://console.groq.com/keys)

```
gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 7. GROQ_MODEL (Optional)
Groq model to use. Default: `llama-3.3-70b-versatile`

Available models:
- `llama-3.3-70b-versatile` (Recommended)
- `llama-3.1-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

#### 8. FRONTEND_URL (Optional)
Your frontend URL for CORS. Default: `http://localhost:3000`

```
https://your-frontend.vercel.app
```

### How to Set Secrets

1. Go to your Space
2. Click **Settings** tab
3. Scroll to **Variables and secrets**
4. Add each secret:
   - Name: `DATABASE_URL`
   - Value: Your database URL
   - Click **Add**
5. Repeat for all required secrets
6. **Restart the Space**

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/signin` - Authenticate user

### Tasks (Protected - Requires JWT)
- `GET /api/{user_id}/tasks` - List all tasks
- `POST /api/{user_id}/tasks` - Create task
- `GET /api/{user_id}/tasks/{id}` - Get task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

### AI Chat (Protected - Requires JWT)
- `POST /api/chat` - Send message to AI assistant
- `GET /api/conversations/{user_id}` - Get user conversations
- `GET /api/conversations/{conversation_id}/messages` - Get conversation messages

### Health & Info
- `GET /health` - Health check
- `GET /` - API information
- `GET /api/info` - Endpoint details

## 🗄️ Database Setup

### Neon (Recommended - Free Tier Available)

1. Go to [neon.tech](https://neon.tech)
2. Sign up and create a project
3. Copy the connection string
4. Add as `DATABASE_URL` secret in Space settings

### Alternative Providers
- [Supabase](https://supabase.com) - Free tier
- [Railway](https://railway.app) - Free tier
- [Render](https://render.com) - Free tier

## 🤖 AI Setup

### Choose Your LLM Provider

#### Option 1: OpenRouter (Recommended for Production)

**Why OpenRouter?**
- ✅ Access to multiple AI models (Claude, GPT-4, Llama, Gemini)
- ✅ OpenAI-compatible API
- ✅ Pay-per-use pricing (no subscriptions)
- ✅ Free credits for new users ($5)
- ✅ Automatic fallback between models

**Get API Key:**
1. Go to [OpenRouter](https://openrouter.ai)
2. Sign up for free account
3. Go to [Keys](https://openrouter.ai/keys)
4. Create new API key
5. Add as `OPENROUTER_API_KEY` secret
6. Set `LLM_PROVIDER=OPENROUTER`

**Pricing:**
- Claude 3.5 Sonnet: ~$3 per million tokens
- GPT-4 Turbo: ~$10 per million tokens
- Typical usage: 100 messages ≈ $0.10-$0.50

#### Option 2: Groq (Recommended for Development)

**Why Groq?**
- ✅ Ultra-fast inference (up to 10x faster)
- ✅ Free tier with generous limits
- ✅ OpenAI-compatible API
- ✅ Optimized for Llama models
- ✅ Perfect for development and testing

**Get API Key:**
1. Go to [Groq Console](https://console.groq.com)
2. Sign up for free account
3. Go to [Keys](https://console.groq.com/keys)
4. Create new API key
5. Add as `GROQ_API_KEY` secret
6. Set `LLM_PROVIDER=GROQ`

**Pricing:**
- Free tier available
- Llama 3.3 70B: Free during beta
- Ultra-fast response times
- Llama 3.1 70B: ~$0.50 per million tokens

**Typical usage:** 100 chat messages ≈ $0.10-$0.50

## 🔒 Security Features

- ✅ Password hashing with bcrypt (12 rounds)
- ✅ JWT tokens (HS256, 7-day expiry)
- ✅ User isolation at database level
- ✅ Protected routes with middleware
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Non-root Docker user
- ✅ Secure API key handling

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115.0+
- **Language**: Python 3.13
- **ORM**: SQLModel 0.0.22 (async)
- **Database**: PostgreSQL (asyncpg driver)
- **Auth**: JWT (python-jose)
- **Password**: Passlib + bcrypt
- **Migrations**: Alembic 1.14.0
- **AI**: OpenAI SDK + OpenRouter
- **MCP**: Model Context Protocol

## 📊 Monitoring

### Check Status
```bash
# Health check
curl https://YOUR-SPACE.hf.space/health

# Expected response
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

### View Logs
1. Go to your Space
2. Click **Logs** tab
3. Monitor real-time logs

## 🐛 Troubleshooting

### Space Won't Start

**Check Logs:**
1. Go to Space > **Logs** tab
2. Look for error messages

**Common Issues:**

1. **"DATABASE_URL is not set"**
   - Add `DATABASE_URL` in Space settings
   - Restart the Space

2. **"OPENROUTER_API_KEY is not set"**
   - Add `OPENROUTER_API_KEY` in Space settings
   - Get key from https://openrouter.ai/keys
   - Restart the Space

3. **"Connection refused" to database**
   - Verify DATABASE_URL is correct
   - Check database is active
   - Ensure URL has `?sslmode=require`

4. **AI chat not working**
   - Verify OPENROUTER_API_KEY is valid
   - Check OpenRouter account has credits
   - Review logs for API errors

### Test Locally

```bash
# Build Docker image
docker build -t todo-ai-backend .

# Run with environment variables
docker run -p 7860:7860 \
  -e DATABASE_URL="your-db-url" \
  -e BETTER_AUTH_SECRET="your-secret" \
  -e OPENROUTER_API_KEY="your-openrouter-key" \
  todo-ai-backend

# Test
curl http://localhost:7860/health
```

## 📚 Documentation

Once running, visit `/docs` for interactive API documentation with:
- All endpoints listed
- Request/response schemas
- Try-it-out functionality
- Authentication support
- AI chat examples

## 🔄 Updating

To update your Space:

```bash
# Make changes locally
git add .
git commit -m "Update: description"
git push

# Hugging Face will automatically rebuild
```

## 💡 Tips

1. **Use Neon free tier** for database (0.5GB storage)
2. **Start with Claude 3.5 Sonnet** for best AI performance
3. **Monitor OpenRouter usage** to control costs
4. **Test locally** before pushing to HF
5. **Keep secrets secure** - never commit them
6. **Use health endpoint** for monitoring

## 🎯 Use Cases

### Task Management via Chat
```
User: "Create a task to prepare presentation for Monday"
AI: "I've created a task: 'Prepare presentation' with due date Monday"

User: "Show me all my tasks"
AI: "You have 3 tasks: 1) Prepare presentation (pending)..."

User: "Mark the presentation task as done"
AI: "Great! I've marked 'Prepare presentation' as complete"
```

### Smart Task Organization
```
User: "What should I focus on today?"
AI: "Based on your tasks, I recommend focusing on..."

User: "Remind me about urgent tasks"
AI: "You have 2 urgent tasks: 1) Submit report (due today)..."
```

## 📞 Support

- **API Docs**: Visit `/docs` endpoint
- **Health Check**: Visit `/health` endpoint
- **Logs**: Check Space logs tab
- **OpenRouter**: https://openrouter.ai/docs
- **Issues**: Check error messages in logs

## 📄 License

MIT License

## 🏆 Credits

Built with FastAPI, SQLModel, PostgreSQL, and OpenRouter.
Part of Hackathon II: The Evolution of Todo by Panaversity, PIAIC, and GIAIC.

---

**Status**: ✅ Ready for deployment
**Port**: 7860 (Hugging Face Spaces)
**Health**: `/health` endpoint
**AI**: Powered by OpenRouter
