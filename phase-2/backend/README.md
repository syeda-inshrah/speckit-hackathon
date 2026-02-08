---
title: Todo Backend API
emoji: 📝
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
app_port: 7860
---

# Todo Backend API 🚀

A production-ready FastAPI backend for multi-user todo application with JWT authentication.

## 🌟 Features

- 🔐 **JWT Authentication** - Secure token-based authentication
- 👥 **Multi-user Support** - Complete user isolation
- 📝 **Task Management** - Full CRUD operations
- 🗄️ **PostgreSQL Database** - Persistent storage with async support
- ⚡ **FastAPI** - High-performance async API
- 📚 **Auto Documentation** - Interactive Swagger UI

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

#### 3. FRONTEND_URL (Optional)
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
5. Repeat for `BETTER_AUTH_SECRET` and `FRONTEND_URL`
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

## 🔒 Security Features

- ✅ Password hashing with bcrypt (12 rounds)
- ✅ JWT tokens (HS256, 7-day expiry)
- ✅ User isolation at database level
- ✅ Protected routes with middleware
- ✅ Input validation with Pydantic
- ✅ CORS configuration
- ✅ Non-root Docker user

## 🛠️ Technology Stack

- **Framework**: FastAPI 0.115.0+
- **Language**: Python 3.13
- **ORM**: SQLModel 0.0.22 (async)
- **Database**: PostgreSQL (asyncpg driver)
- **Auth**: JWT (python-jose)
- **Password**: Passlib + bcrypt
- **Migrations**: Alembic 1.14.0

## 📊 Monitoring

### Check Status
```bash
# Health check
curl https://YOUR-SPACE.hf.space/health

# Expected response
{"status":"healthy","service":"todo-backend","version":"1.0.0"}
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

2. **"BETTER_AUTH_SECRET is not set"**
   - Add `BETTER_AUTH_SECRET` in Space settings
   - Restart the Space

3. **"Connection refused" to database**
   - Verify DATABASE_URL is correct
   - Check database is active
   - Ensure URL has `?sslmode=require`

4. **"Module not found"**
   - Check `requirements.txt` has all dependencies
   - Rebuild the Space

### Test Locally

```bash
# Build Docker image
docker build -t todo-backend .

# Run with environment variables
docker run -p 7860:7860 \
  -e DATABASE_URL="your-db-url" \
  -e BETTER_AUTH_SECRET="your-secret" \
  todo-backend

# Test
curl http://localhost:7860/health
```

## 📚 Documentation

Once running, visit `/docs` for interactive API documentation with:
- All endpoints listed
- Request/response schemas
- Try-it-out functionality
- Authentication support

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
2. **Monitor logs** regularly for errors
3. **Test locally** before pushing to HF
4. **Keep secrets secure** - never commit them
5. **Use health endpoint** for monitoring

## 📞 Support

- **API Docs**: Visit `/docs` endpoint
- **Health Check**: Visit `/health` endpoint
- **Logs**: Check Space logs tab
- **Issues**: Check error messages in logs

## 📄 License

MIT License

## 🏆 Credits

Built with FastAPI, SQLModel, and PostgreSQL.
Part of Hackathon II: The Evolution of Todo by Panaversity, PIAIC, and GIAIC.

---

**Status**: ✅ Ready for deployment
**Port**: 7860 (Hugging Face Spaces)
**Health**: `/health` endpoint
