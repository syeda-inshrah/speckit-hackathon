# Docker Image Contract - Frontend

## Overview

**Component:** Frontend Docker Image
**Image Name:** `todo-frontend:latest`
**Base Image:** `node:20-alpine`
**Maintainer:** Todo App Team
**Version:** 1.0.0

---

## Image Specifications

### Build Requirements

**Build Context:**
- Source: `phase-3/frontend/`
- Dockerfile: `phase-4/frontend/Dockerfile`
- Build time: < 3 minutes (first build), < 1 minute (cached)
- Build size: < 200MB

**Build Arguments:**
None required

**Build Command:**
```bash
docker build -t todo-frontend:latest -f phase-4/frontend/Dockerfile phase-3/frontend
```

---

## Runtime Contract

### Exposed Ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 3000 | TCP/HTTP | Next.js application server |

### Required Environment Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | string | Yes | - | Backend API URL (e.g., http://backend-service:8001) |
| NODE_ENV | string | No | production | Environment mode (development/production) |

### Optional Environment Variables

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| NEXT_PUBLIC_ENABLE_ANALYTICS | boolean | false | Enable analytics tracking |
| NEXT_PUBLIC_LOG_LEVEL | string | info | Logging level (debug/info/warn/error) |
| PORT | number | 3000 | Server port (if different from default) |

---

## Health Check Contract

### Endpoint: GET /health

**URL:** `http://localhost:3000/health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK`: Application is healthy
- `503 Service Unavailable`: Application is unhealthy

**Response Time:** < 100ms

**Docker Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

---

## Security Contract

### User Execution

**User:** `nextjs`
**UID:** `1001`
**GID:** `1001`

**Verification:**
```bash
docker run --rm todo-frontend:latest whoami
# Expected output: nextjs
```

### Capabilities

**Dropped Capabilities:** ALL
**Added Capabilities:** None

### File System

**Working Directory:** `/app`
**Read-Only Root Filesystem:** No (Next.js requires write access for cache)

---

## Resource Requirements

### Minimum Resources

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 50m | 100m |
| Memory | 64Mi | 128Mi |
| Disk | 200MB | 300MB |

### Resource Limits

| Resource | Limit |
|----------|-------|
| CPU | 500m |
| Memory | 512Mi |

---

## Startup Contract

### Startup Time

**Expected:** < 15 seconds
**Maximum:** 30 seconds

### Startup Sequence

1. Container starts
2. Node.js runtime initializes
3. Next.js server starts
4. Health endpoint becomes available
5. Application ready to serve traffic

### Startup Logs

**Expected Log Pattern:**
```
> todo-frontend@1.0.0 start
> next start

ready - started server on 0.0.0.0:3000, url: http://localhost:3000
```

---

## API Contract

### Served Routes

| Route | Method | Description |
|-------|--------|-------------|
| / | GET | Home page |
| /signin | GET | Sign in page |
| /signup | GET | Sign up page |
| /tasks | GET | Tasks page (authenticated) |
| /chat | GET | Chat page (authenticated) |
| /health | GET | Health check endpoint |
| /_next/* | GET | Next.js static assets |

### External Dependencies

| Dependency | Type | Required | Description |
|------------|------|----------|-------------|
| Backend API | HTTP | Yes | Backend service at NEXT_PUBLIC_API_URL |
| Browser | Client | Yes | Modern browser with JavaScript enabled |

---

## Volume Mounts

### Required Volumes

None

### Optional Volumes

| Path | Purpose | Read/Write |
|------|---------|------------|
| /app/.next/cache | Build cache (dev only) | RW |

---

## Networking Contract

### Ingress

**Port:** 3000
**Protocol:** HTTP
**Path:** All paths (/)

### Egress

**Required Connections:**
- Backend API (configured via NEXT_PUBLIC_API_URL)
- DNS resolution

**Ports:**
- 80/443 (HTTP/HTTPS to backend)
- 53 (DNS)

---

## Logging Contract

### Log Format

**Standard Output (stdout):**
- Next.js server logs
- Application logs
- Request logs

**Standard Error (stderr):**
- Error messages
- Stack traces

### Log Level

Controlled by `NEXT_PUBLIC_LOG_LEVEL` environment variable

### Sample Logs

```
ready - started server on 0.0.0.0:3000
info  - Loaded env from /app/.env.local
info  - Using webpack 5
```

---

## Graceful Shutdown Contract

### Shutdown Signal

**Signal:** SIGTERM

### Shutdown Sequence

1. Receive SIGTERM
2. Stop accepting new connections
3. Complete in-flight requests (max 30s)
4. Close server
5. Exit with code 0

### Shutdown Timeout

**Maximum:** 30 seconds

---

## Testing Contract

### Smoke Test

```bash
# Start container
docker run -d -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://backend:8001 \
  --name frontend-test \
  todo-frontend:latest

# Wait for startup
sleep 10

# Test health endpoint
curl -f http://localhost:3000/health

# Test home page
curl -f http://localhost:3000/

# Cleanup
docker stop frontend-test
docker rm frontend-test
```

### Expected Test Results

- Health endpoint returns 200 OK
- Home page returns 200 OK
- No errors in logs

---

## Versioning Contract

### Image Tags

| Tag | Description | Stability |
|-----|-------------|-----------|
| latest | Latest build | Development |
| v1.0.0 | Semantic version | Stable |
| sha-abc123 | Git commit SHA | Immutable |

### Backward Compatibility

**Breaking Changes:** Require major version bump
**New Features:** Require minor version bump
**Bug Fixes:** Require patch version bump

---

## Compliance Contract

### Security Compliance

- [ ] Runs as non-root user
- [ ] No hardcoded secrets
- [ ] Minimal base image (Alpine)
- [ ] Regular security updates
- [ ] Vulnerability scanning (Trivy)

### Best Practices

- [ ] Multi-stage build
- [ ] Layer caching optimization
- [ ] .dockerignore file
- [ ] Health check implemented
- [ ] Proper signal handling

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
- Missing NEXT_PUBLIC_API_URL
- Port 3000 already in use
- Insufficient resources

**Resolution:**
```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker inspect <container-id> | jq '.[0].Config.Env'

# Check port availability
netstat -an | grep 3000
```

#### Issue: Health check failing

**Symptoms:** Container marked unhealthy
**Possible Causes:**
- Application not fully started
- Health endpoint not responding
- Network issues

**Resolution:**
```bash
# Check health status
docker inspect --format='{{.State.Health.Status}}' <container-id>

# Test health endpoint manually
docker exec <container-id> wget -O- http://localhost:3000/health

# Check application logs
docker logs <container-id>
```

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial frontend Docker image
- Multi-stage build implementation
- Health check endpoint
- Non-root user execution
- Alpine Linux base image

---

## Approval

**Contract Owner:** Frontend Team
**Reviewed By:** DevOps Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Dockerfile](../../frontend/Dockerfile)
- [Phase 4 Specification](../spec.md)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
