# Docker Compose Contract

## Overview

**Component:** Docker Compose Configuration
**File:** `docker-compose.yml`
**Version:** 3.8
**Purpose:** Local development and testing of full stack

---

## Service Definitions

### Frontend Service

**Service Name:** `frontend`

**Configuration:**
```yaml
frontend:
  build:
    context: ../phase-3/frontend
    dockerfile: ../../phase-4/frontend/Dockerfile
  image: todo-frontend:latest
  container_name: todo-frontend
  ports:
    - "3000:3000"
  environment:
    - NEXT_PUBLIC_API_URL=http://backend:8001
    - NODE_ENV=production
  depends_on:
    backend:
      condition: service_healthy
  healthcheck:
    test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"]
    interval: 30s
    timeout: 3s
    retries: 3
    start_period: 40s
  networks:
    - todo-network
  restart: unless-stopped
```

**Exposed Ports:**
- Host: 3000
- Container: 3000

**Dependencies:**
- Backend service (with health check)

---

### Backend Service

**Service Name:** `backend`

**Configuration:**
```yaml
backend:
  build:
    context: ../phase-3/backend
    dockerfile: ../../phase-4/backend/Dockerfile
  image: todo-backend:latest
  container_name: todo-backend
  ports:
    - "8001:8001"
  env_file:
    - ../phase-3/backend/.env
  environment:
    - FRONTEND_URL=http://frontend:3000
  healthcheck:
    test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"]
    interval: 30s
    timeout: 3s
    retries: 3
    start_period: 40s
  networks:
    - todo-network
  restart: unless-stopped
```

**Exposed Ports:**
- Host: 8001
- Container: 8001

**Environment:**
- Loaded from `.env` file
- FRONTEND_URL override for CORS

---

## Network Configuration

**Network Name:** `todo-network`

**Configuration:**
```yaml
networks:
  todo-network:
    driver: bridge
```

**Purpose:**
- Isolate todo app services
- Enable service-to-service communication
- DNS resolution by service name

---

## Volume Configuration

**Volumes:** None (stateless application)

**Note:** Database is external (Neon PostgreSQL)

---

## Usage Contract

### Starting Services

**Command:**
```bash
cd phase-4
docker-compose up -d
```

**Expected Behavior:**
1. Build images if not present
2. Create network
3. Start backend service
4. Wait for backend health check
5. Start frontend service
6. Both services running and healthy

**Verification:**
```bash
docker-compose ps

# Expected output:
# NAME            IMAGE                 STATUS         PORTS
# todo-backend    todo-backend:latest   Up (healthy)   0.0.0.0:8001->8001/tcp
# todo-frontend   todo-frontend:latest  Up (healthy)   0.0.0.0:3000->3000/tcp
```

---

### Stopping Services

**Command:**
```bash
docker-compose down
```

**Expected Behavior:**
1. Stop frontend service
2. Stop backend service
3. Remove containers
4. Remove network

**Preserve Images:**
```bash
docker-compose down --rmi none
```

**Remove Everything:**
```bash
docker-compose down --rmi all --volumes
```

---

### Viewing Logs

**All Services:**
```bash
docker-compose logs -f
```

**Specific Service:**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

**Last N Lines:**
```bash
docker-compose logs --tail=100 backend
```

---

### Rebuilding Services

**Rebuild All:**
```bash
docker-compose build
```

**Rebuild Specific Service:**
```bash
docker-compose build backend
```

**Rebuild and Restart:**
```bash
docker-compose up -d --build
```

---

## Health Check Contract

### Frontend Health Check

**Command:** `node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"`

**Interval:** 30 seconds
**Timeout:** 3 seconds
**Retries:** 3
**Start Period:** 40 seconds

**Success:** Exit code 0
**Failure:** Exit code 1

---

### Backend Health Check

**Command:** `python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"`

**Interval:** 30 seconds
**Timeout:** 3 seconds
**Retries:** 3
**Start Period:** 40 seconds

**Success:** Exit code 0
**Failure:** Exit code 1

---

## Dependency Contract

### Service Dependencies

**Frontend depends on Backend:**
```yaml
depends_on:
  backend:
    condition: service_healthy
```

**Behavior:**
- Frontend waits for backend to be healthy
- Backend must pass health check before frontend starts
- Ensures backend API is available when frontend starts

---

## Environment Variables Contract

### Frontend Environment Variables

**Source:** Inline in docker-compose.yml

**Variables:**
- `NEXT_PUBLIC_API_URL`: Backend API URL (http://backend:8001)
- `NODE_ENV`: Environment mode (production)

**Note:** Uses service name `backend` for DNS resolution

---

### Backend Environment Variables

**Source:** `.env` file (`../phase-3/backend/.env`)

**Required Variables:**
- DATABASE_URL
- BETTER_AUTH_SECRET
- GROQ_API_KEY
- LLM_PROVIDER
- GROQ_BASE_URL
- GROQ_MODEL

**Override:**
- `FRONTEND_URL`: Set to http://frontend:3000 for CORS

---

## Networking Contract

### Service Communication

**Frontend to Backend:**
- URL: http://backend:8001
- DNS: Resolved by Docker network
- Protocol: HTTP

**Backend to Frontend:**
- URL: http://frontend:3000
- DNS: Resolved by Docker network
- Protocol: HTTP (CORS)

**External Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8001

---

## Testing Contract

### Smoke Test

```bash
# Start services
docker-compose up -d

# Wait for services to be healthy
sleep 30

# Test backend health
curl -f http://localhost:8001/health

# Test frontend health
curl -f http://localhost:3000/health

# Test backend API
curl -f http://localhost:8001/docs

# Test frontend UI
curl -f http://localhost:3000/

# Check logs
docker-compose logs --tail=50

# Stop services
docker-compose down
```

**Expected Results:**
- All health checks return 200 OK
- Backend API docs accessible
- Frontend UI loads
- No errors in logs

---

### Integration Test

```bash
# Start services
docker-compose up -d

# Wait for healthy state
docker-compose ps

# Test frontend-to-backend communication
docker-compose exec frontend curl -f http://backend:8001/health

# Test backend-to-database communication
docker-compose exec backend python -c "
import asyncio
import asyncpg
from src.core.config import settings
asyncio.run(asyncpg.connect(settings.DATABASE_URL))
print('Database connection successful')
"

# Test full stack
# 1. Open browser to http://localhost:3000
# 2. Sign up / Sign in
# 3. Test chat functionality
# 4. Verify task operations

# Cleanup
docker-compose down
```

---

## Performance Contract

### Build Performance

**First Build:**
- Frontend: < 3 minutes
- Backend: < 4 minutes
- Total: < 7 minutes

**Cached Build:**
- Frontend: < 1 minute
- Backend: < 1 minute
- Total: < 2 minutes

---

### Startup Performance

**Service Startup:**
- Backend: < 30 seconds to healthy
- Frontend: < 15 seconds to healthy (after backend)
- Total: < 45 seconds

---

### Resource Usage

**Expected Resource Usage:**
- Frontend: ~200MB RAM, 10% CPU
- Backend: ~300MB RAM, 20% CPU
- Total: ~500MB RAM, 30% CPU

**Monitoring:**
```bash
docker stats
```

---

## Troubleshooting Contract

### Common Issues

#### Issue: Services fail to start

**Symptoms:**
```
ERROR: Service 'backend' failed to build
```

**Diagnosis:**
```bash
docker-compose build --no-cache
docker-compose logs
```

**Resolution:**
- Check Dockerfile syntax
- Verify build context
- Check for missing dependencies

---

#### Issue: Health checks failing

**Symptoms:**
```
backend is unhealthy
```

**Diagnosis:**
```bash
docker-compose ps
docker-compose logs backend
docker-compose exec backend curl http://localhost:8001/health
```

**Resolution:**
- Check application logs
- Verify health endpoint
- Check database connectivity
- Increase start_period if needed

---

#### Issue: Services can't communicate

**Symptoms:**
```
curl: (6) Could not resolve host: backend
```

**Diagnosis:**
```bash
docker-compose exec frontend ping backend
docker network inspect phase-4_todo-network
```

**Resolution:**
- Verify services are on same network
- Check service names in URLs
- Restart services

---

#### Issue: Port already in use

**Symptoms:**
```
ERROR: for frontend  Cannot start service frontend:
Ports are not available: listen tcp 0.0.0.0:3000: bind: address already in use
```

**Diagnosis:**
```bash
# Check what's using the port
netstat -an | grep 3000
lsof -i :3000
```

**Resolution:**
- Stop conflicting service
- Change port mapping in docker-compose.yml
- Use different host port

---

## Development Workflow

### Development Mode

**For development with hot reload:**

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  frontend:
    build:
      context: ../phase-3/frontend
      dockerfile: Dockerfile.dev  # Development Dockerfile
    volumes:
      - ../phase-3/frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev

  backend:
    build:
      context: ../phase-3/backend
      dockerfile: Dockerfile.dev  # Development Dockerfile
    volumes:
      - ../phase-3/backend:/app
    environment:
      - RELOAD=true
    command: uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Usage:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

---

## Security Contract

### Security Best Practices

- [x] No hardcoded secrets in docker-compose.yml
- [x] Secrets loaded from .env file
- [x] .env file in .gitignore
- [x] Services run as non-root users
- [x] Network isolation
- [x] Health checks implemented

### Security Warnings

**⚠️ Do not commit:**
- `.env` files with real credentials
- `docker-compose.override.yml` with secrets

**⚠️ Production:**
- Do not use docker-compose in production
- Use Kubernetes for production deployments

---

## Compliance Contract

### Docker Compose Best Practices

- [x] Version specified (3.8)
- [x] Service names descriptive
- [x] Health checks defined
- [x] Dependencies specified
- [x] Networks defined
- [x] Restart policies set
- [x] Environment variables externalized

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial docker-compose configuration
- Frontend and backend services
- Health checks
- Network configuration
- Dependency management

---

## Approval

**Contract Owner:** DevOps Team
**Reviewed By:** Backend Team, Frontend Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [docker-compose.yml](../../docker-compose.yml)
- [Phase 4 Specification](../spec.md)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
