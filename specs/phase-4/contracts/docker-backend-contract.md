# Docker Image Contract - Backend

## Overview

**Component:** Backend Docker Image
**Image Name:** `todo-backend:latest`
**Base Image:** `python:3.13-alpine`
**Maintainer:** Todo App Team
**Version:** 1.0.0

---

## Image Specifications

### Build Requirements

**Build Context:**
- Source: `phase-3/backend/`
- Dockerfile: `phase-4/backend/Dockerfile`
- Build time: < 4 minutes (first build), < 1 minute (cached)
- Build size: < 300MB

**Build Arguments:**
None required

**Build Command:**
```bash
docker build -t todo-backend:latest -f phase-4/backend/Dockerfile phase-3/backend
```

---

## Runtime Contract

### Exposed Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 8001 | TCP/HTTP | FastAPI application server |

### Required Environment Variables

| Variable | Type | Required | Description |
|----------|------|----------|-------------|
| DATABASE_URL | string | Yes | PostgreSQL connection string |
| BETTER_AUTH_SECRET | string | Yes | JWT signing secret (min 32 chars) |
| GROQ_API_KEY | string | Yes* | Groq API key (*if LLM_PROVIDER=GROQ) |
| FRONTEND_URL | string | Yes | Frontend URL for CORS |

### Optional Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| LLM_PROVIDER | string | GROQ | LLM provider (GROQ/OPENROUTER) |
| JWT_ALGORITHM | string | HS256 | JWT algorithm |
| JWT_EXPIRATION_DAYS | integer | 7 | JWT expiration days |
| GROQ_BASE_URL | string | https://api.groq.com | Groq API base URL |
| GROQ_MODEL | string | openai/gpt-oss-20b | Groq model name |
| AGENT_NAME | string | TodoAssistant | Agent name |
| AGENT_INSTRUCTIONS | string | - | Agent instructions |
| MAX_TOKENS | integer | 2000 | Max tokens |
| TEMPERATURE | float | 0.7 | Temperature |

---

## Health Check Contract

### Endpoint: GET /health

**URL:** `http://localhost:8001/health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK`: Application is healthy
- `503 Service Unavailable`: Application is unhealthy

**Response Time:** < 200ms

### Endpoint: GET /ready

**URL:** `http://localhost:8001/ready`

**Response:**
```json
{
  "status": "ready",
  "database": "connected"
}
```

**Status Codes:**
- `200 OK`: Application is ready (database connected)
- `503 Service Unavailable`: Application is not ready

**Response Time:** < 500ms (includes DB check)

**Docker Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"
```

---

## Security Contract

### User Execution

**User:** `appuser`
**UID:** `1001`
**GID:** `1001`

**Verification:**
```bash
docker run --rm todo-backend:latest whoami
# Expected output: appuser
```

### Capabilities

**Dropped Capabilities:** ALL
**Added Capabilities:** None

### File System

**Working Directory:** `/app`
**Read-Only Root Filesystem:** No (Python requires write access for bytecode)

### Secrets Management

**Prohibited:**
- Hardcoded credentials in image
- Secrets in environment variables (use Kubernetes Secrets)
- Secrets in logs

**Required:**
- All secrets via Kubernetes Secrets
- No secrets in image layers
- Secrets rotation support

---

## Resource Requirements

### Minimum Resources

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 100m | 200m |
| Memory | 128Mi | 256Mi |
| Disk | 300MB | 500MB |

### Resource Limits

| Resource | Limit |
|----------|-------|
| CPU | 1000m (1 core) |
| Memory | 1Gi |

---

## Startup Contract

### Startup Time

**Expected:** < 30 seconds
**Maximum:** 60 seconds

### Startup Sequence

1. Container starts
2. Python runtime initializes
3. Load environment variables
4. Initialize database connection pool
5. Start FastAPI/Uvicorn server
6. Health endpoint becomes available
7. Readiness check passes (DB connected)
8. Application ready to serve traffic

### Startup Logs

**Expected Log Pattern:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

---

## API Contract

### Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| /health | GET | No | Health check |
| /ready | GET | No | Readiness check |
| /docs | GET | No | API documentation (Swagger) |
| /api/auth/signup | POST | No | User registration |
| /api/auth/signin | POST | No | User authentication |
| /api/{user_id}/tasks | GET | Yes | List tasks |
| /api/{user_id}/tasks | POST | Yes | Create task |
| /api/{user_id}/tasks/{id} | GET | Yes | Get task |
| /api/{user_id}/tasks/{id} | PUT | Yes | Update task |
| /api/{user_id}/tasks/{id} | DELETE | Yes | Delete task |
| /api/{user_id}/tasks/{id}/complete | PATCH | Yes | Toggle completion |
| /api/{user_id}/chat | POST | Yes | Chat with AI |

### Authentication

**Method:** JWT Bearer Token
**Header:** `Authorization: Bearer <token>`
**Token Expiration:** Configurable (default 7 days)

### CORS Configuration

**Allowed Origins:** Configured via FRONTEND_URL
**Allowed Methods:** GET, POST, PUT, DELETE, PATCH, OPTIONS
**Allowed Headers:** Authorization, Content-Type

### External Dependencies

| Dependency | Type | Required | Description |
|------------|------|----------|-------------|
| Neon PostgreSQL | Database | Yes | Primary data store |
| Groq API | HTTP API | Yes* | LLM inference (*if GROQ) |
| OpenRouter API | HTTP API | Yes* | LLM inference (*if OPENROUTER) |

---

## Database Contract

### Connection Requirements

**Protocol:** PostgreSQL
**SSL:** Required
**Connection String Format:**
```
postgresql://<user>:<password>@<host>:<port>/<database>?ssl=require
```

**Connection Pool:**
- Min connections: 5
- Max connections: 20
- Connection timeout: 30s
- Idle timeout: 300s

### Database Schema

**Tables:**
- users
- tasks
- conversations
- messages

**Migrations:**
- Handled by Alembic
- Auto-run on startup (optional)

---

## Volume Mounts

### Required Volumes

None (stateless application)

### Optional Volumes

| Path | Purpose | Read/Write |
|------|---------|------------|
| /app/logs | Application logs (if file logging enabled) | RW |

---

## Networking Contract

### Ingress

**Port:** 8001
**Protocol:** HTTP
**Path:** All paths (/)

### Egress

**Required Connections:**
- Neon PostgreSQL (port 5432)
- Groq API (port 443)
- DNS resolution (port 53)

**Firewall Rules:**
- Allow outbound to Neon DB
- Allow outbound to Groq API
- Allow outbound DNS

---

## Logging Contract

### Log Format

**Standard Output (stdout):**
- Uvicorn access logs
- Application logs
- Request/response logs

**Standard Error (stderr):**
- Error messages
- Stack traces
- Exception details

### Log Level

**Default:** INFO
**Configurable:** Via LOG_LEVEL environment variable
**Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL

### Sample Logs

```
INFO:     127.0.0.1:52000 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:52001 - "POST /api/user-id/chat HTTP/1.1" 200 OK
ERROR:    Database connection failed: connection timeout
```

### Sensitive Data

**Prohibited in Logs:**
- Passwords
- API keys
- JWT tokens
- Database credentials
- User PII (unless necessary)

---

## Graceful Shutdown Contract

### Shutdown Signal

**Signal:** SIGTERM

### Shutdown Sequence

1. Receive SIGTERM
2. Stop accepting new connections
3. Complete in-flight requests (max 30s)
4. Close database connections
5. Close HTTP client connections
6. Exit with code 0

### Shutdown Timeout

**Maximum:** 30 seconds
**Force Kill:** SIGKILL after timeout

---

## Testing Contract

### Smoke Test

```bash
# Start container
docker run -d -p 8001:8001 \
  -e DATABASE_URL="postgresql://..." \
  -e BETTER_AUTH_SECRET="test-secret-32-characters-long" \
  -e GROQ_API_KEY="test-key" \
  -e FRONTEND_URL="http://localhost:3000" \
  --name backend-test \
  todo-backend:latest

# Wait for startup
sleep 15

# Test health endpoint
curl -f http://localhost:8001/health

# Test readiness endpoint
curl -f http://localhost:8001/ready

# Test API docs
curl -f http://localhost:8001/docs

# Cleanup
docker stop backend-test
docker rm backend-test
```

### Expected Test Results

- Health endpoint returns 200 OK
- Readiness endpoint returns 200 OK with database: connected
- API docs accessible
- No errors in logs

---

## Performance Contract

### Response Time SLAs

| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| /health | < 50ms | < 100ms | < 200ms |
| /ready | < 200ms | < 500ms | < 1s |
| /api/*/tasks (GET) | < 200ms | < 500ms | < 1s |
| /api/*/tasks (POST) | < 300ms | < 700ms | < 1.5s |
| /api/*/chat | < 2s | < 5s | < 10s |

### Throughput

**Expected:** 100 requests/second per replica
**Maximum:** 500 requests/second per replica

### Concurrency

**Concurrent Requests:** 50 per replica
**Connection Pool:** 20 database connections

---

## Versioning Contract

### Image Tags

| Tag | Description | Stability |
|-----|-------------|-----------|
| latest | Latest build | Development |
| v1.0.0 | Semantic version | Stable |
| sha-abc123 | Git commit SHA | Immutable |

### API Versioning

**Current Version:** v1
**Versioning Strategy:** URL path (/api/v1/...)
**Backward Compatibility:** Maintained for 1 major version

---

## Compliance Contract

### Security Compliance

- [ ] Runs as non-root user
- [ ] No hardcoded secrets
- [ ] Minimal base image (Alpine)
- [ ] Regular security updates
- [ ] Vulnerability scanning (Trivy)
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input validation)
- [ ] CSRF protection (SameSite cookies)

### Best Practices

- [ ] Multi-stage build
- [ ] Layer caching optimization
- [ ] .dockerignore file
- [ ] Health and readiness checks
- [ ] Proper signal handling
- [ ] Connection pooling
- [ ] Error handling
- [ ] Logging best practices

---

## Support Contract

### Supported Platforms

| Platform | Architecture | Status |
|----------|--------------|--------|
| Linux | amd64 | Supported |
| Linux | arm64 | Supported |
| macOS | amd64 | Supported |
| macOS | arm64 | Supported |
| Windows | amd64 | Supported (via WSL2) |

### Kubernetes Compatibility

**Minimum Version:** 1.24+
**Tested Versions:** 1.28, 1.29, 1.30

---

## Troubleshooting Contract

### Common Issues

#### Issue: Container fails to start

**Symptoms:** Container exits immediately
**Possible Causes:**
- Missing required environment variables
- Invalid DATABASE_URL
- Port 8001 already in use
- Insufficient resources

**Resolution:**
```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker inspect <container-id> | jq '.[0].Config.Env'

# Test database connection
docker exec <container-id> python -c "import asyncpg; ..."
```

#### Issue: Database connection fails

**Symptoms:** Readiness check fails, 503 errors
**Possible Causes:**
- Invalid DATABASE_URL
- Network connectivity issues
- Database not accessible
- SSL/TLS issues

**Resolution:**
```bash
# Check readiness endpoint
curl http://localhost:8001/ready

# Test database connection manually
docker exec <container-id> python -c "
import asyncpg
import asyncio
asyncio.run(asyncpg.connect('$DATABASE_URL'))
"

# Check network connectivity
docker exec <container-id> ping -c 3 <db-host>
```

#### Issue: High memory usage

**Symptoms:** Container OOMKilled, high memory usage
**Possible Causes:**
- Memory leak
- Too many concurrent requests
- Large response payloads
- Insufficient memory limits

**Resolution:**
```bash
# Check memory usage
docker stats <container-id>

# Check resource limits
kubectl describe pod <pod-name>

# Increase memory limits if needed
# Review application for memory leaks
```

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial backend Docker image
- Multi-stage build implementation
- Health and readiness checks
- Non-root user execution
- Alpine Linux base image
- FastAPI + MCP integration
- Groq API support

---

## Approval

**Contract Owner:** Backend Team
**Reviewed By:** DevOps Team, Security Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Dockerfile](../../backend/Dockerfile)
- [Phase 4 Specification](../spec.md)
- [API Documentation](http://localhost:8001/docs)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
