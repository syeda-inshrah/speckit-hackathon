# Phase 4: Local Kubernetes Deployment - Implementation Plan

## Overview

**Phase:** IV - Local Kubernetes Deployment
**Status:** Planning
**Date:** 2026-02-18
**Dependencies:** Phase 3 (AI Chatbot) - Completed

## Executive Summary

This plan outlines the implementation strategy for containerizing the Phase 3 Todo Chatbot and deploying it to a local Kubernetes cluster using Minikube. The approach follows cloud-native best practices with Docker containerization, Helm chart packaging, and AI-assisted DevOps tooling.

## Architecture Decisions

### ADR-001: Multi-Stage Docker Builds

**Decision:** Use multi-stage Docker builds for both frontend and backend

**Rationale:**
- Reduces final image size by 60-70%
- Separates build dependencies from runtime dependencies
- Improves security by excluding build tools from production images
- Faster deployment and startup times

**Alternatives Considered:**
- Single-stage builds: Simpler but results in bloated images
- External build process: More complex CI/CD setup

**Implementation:**
- Frontend: Build stage (npm build) → Production stage (serve static files)
- Backend: Dependencies stage (pip install) → Runtime stage (app only)

### ADR-002: Alpine Linux Base Images

**Decision:** Use Alpine Linux as base images for both services

**Rationale:**
- Minimal size (~5MB base vs ~100MB+ for Ubuntu)
- Reduced attack surface
- Faster image pulls and deployments
- Industry standard for containerized applications

**Trade-offs:**
- Some packages may require additional compilation
- Different package manager (apk vs apt)
- Potential compatibility issues (rare)

**Mitigation:**
- Use official Node/Python Alpine variants
- Test thoroughly before deployment

### ADR-003: Helm for Deployment Management

**Decision:** Use Helm charts instead of raw Kubernetes manifests

**Rationale:**
- Parameterized deployments (dev, staging, prod)
- Version management and rollback capabilities
- Templating reduces duplication
- Package management for Kubernetes
- Industry standard for K8s deployments

**Alternatives Considered:**
- Kustomize: Good but less feature-rich
- Raw manifests: No parameterization or versioning

### ADR-004: External Database (Neon)

**Decision:** Keep Neon PostgreSQL external, not in Kubernetes

**Rationale:**
- Neon provides managed, serverless PostgreSQL
- Avoid stateful workload complexity in Minikube
- Consistent with Phase 3 architecture
- Easier to manage and backup
- Free tier available

**Trade-offs:**
- Network latency (minimal for local dev)
- External dependency

**Future Consideration:**
- Phase 5 may add in-cluster database for production

### ADR-005: ConfigMaps and Secrets Separation

**Decision:** Use ConfigMaps for non-sensitive config, Secrets for credentials

**Rationale:**
- Security best practice
- Kubernetes-native approach
- Easy to update without rebuilding images
- Supports multiple environments

**Implementation:**
- ConfigMaps: API URLs, feature flags, app settings
- Secrets: DB credentials, API keys, JWT secrets

### ADR-006: NodePort for Frontend Access

**Decision:** Use NodePort service type for frontend in Minikube

**Rationale:**
- Simple access via localhost:30000
- No need for Ingress controller in local dev
- Easy to test and debug
- Minikube-friendly

**Alternatives:**
- LoadBalancer: Requires minikube tunnel
- Ingress: Additional complexity for local dev

**Production Note:**
- Phase 5 will use LoadBalancer or Ingress for cloud deployment

### ADR-007: Health Check Endpoints

**Decision:** Implement dedicated health check endpoints for both services

**Rationale:**
- Kubernetes liveness and readiness probes
- Automatic pod restart on failure
- Zero-downtime deployments
- Better observability

**Implementation:**
- Frontend: `/health` endpoint
- Backend: `/health` and `/ready` endpoints

## Implementation Strategy

### Phase 1: Docker Containerization (Days 1-2)

#### 1.1 Frontend Containerization
**Objective:** Create optimized Docker image for Next.js frontend

**Steps:**
1. Create multi-stage Dockerfile
   - Stage 1: Build (npm install, npm build)
   - Stage 2: Production (copy build artifacts, serve)
2. Add .dockerignore file
3. Configure environment variables
4. Implement health check endpoint
5. Test locally with docker run
6. Optimize image size

**Acceptance Criteria:**
- Image size < 200MB
- Builds in < 3 minutes
- Runs as non-root user
- Health check responds

#### 1.2 Backend Containerization
**Objective:** Create optimized Docker image for FastAPI backend

**Steps:**
1. Create multi-stage Dockerfile
   - Stage 1: Dependencies (pip install)
   - Stage 2: Runtime (copy app, run uvicorn)
2. Add .dockerignore file
3. Configure environment variables
4. Implement health check endpoints
5. Test locally with docker run
6. Optimize image size

**Acceptance Criteria:**
- Image size < 300MB
- Builds in < 4 minutes
- Runs as non-root user
- Health checks respond
- Database connection works

#### 1.3 Docker Compose Setup
**Objective:** Enable local testing with docker-compose

**Steps:**
1. Create docker-compose.yml
2. Define frontend service
3. Define backend service
4. Configure networking
5. Add environment variables
6. Test full stack locally

**Acceptance Criteria:**
- Both services start successfully
- Frontend can reach backend
- Backend can reach Neon DB
- Chat functionality works

### Phase 2: Kubernetes Manifests (Days 3-4)

#### 2.1 Frontend Kubernetes Resources
**Objective:** Create K8s manifests for frontend deployment

**Steps:**
1. Create Deployment manifest
   - 2 replicas
   - Resource limits
   - Liveness/readiness probes
   - Environment variables
2. Create Service manifest (NodePort)
3. Create ConfigMap manifest
4. Test deployment to Minikube

**Acceptance Criteria:**
- Pods reach Running state
- Service is accessible
- ConfigMap is mounted
- Health checks pass

#### 2.2 Backend Kubernetes Resources
**Objective:** Create K8s manifests for backend deployment

**Steps:**
1. Create Deployment manifest
   - 2 replicas
   - Resource limits
   - Liveness/readiness probes
   - Environment variables from ConfigMap/Secret
2. Create Service manifest (ClusterIP)
3. Create ConfigMap manifest
4. Create Secret manifest
5. Test deployment to Minikube

**Acceptance Criteria:**
- Pods reach Running state
- Service is accessible internally
- ConfigMap and Secret are mounted
- Database connection works
- Health checks pass

#### 2.3 Integration Testing
**Objective:** Verify end-to-end functionality in Kubernetes

**Steps:**
1. Deploy both services
2. Test frontend-to-backend communication
3. Test backend-to-database communication
4. Test chat functionality
5. Test pod restart recovery
6. Test rolling updates

**Acceptance Criteria:**
- All services communicate correctly
- Chat functionality works
- Application survives pod restarts
- Rolling updates work without downtime

### Phase 3: Helm Charts (Days 5-6)

#### 3.1 Frontend Helm Chart
**Objective:** Package frontend as Helm chart

**Steps:**
1. Create chart structure
   - Chart.yaml
   - values.yaml
   - templates/
2. Templatize Deployment
3. Templatize Service
4. Templatize ConfigMap
5. Add _helpers.tpl
6. Test helm install/upgrade/rollback

**Acceptance Criteria:**
- Chart installs successfully
- Values override works
- Upgrade works
- Rollback works
- Chart passes helm lint

#### 3.2 Backend Helm Chart
**Objective:** Package backend as Helm chart

**Steps:**
1. Create chart structure
2. Templatize Deployment
3. Templatize Service
4. Templatize ConfigMap
5. Templatize Secret
6. Add _helpers.tpl
7. Test helm install/upgrade/rollback

**Acceptance Criteria:**
- Chart installs successfully
- Values override works
- Secrets are handled securely
- Upgrade works
- Rollback works
- Chart passes helm lint

#### 3.3 Helm Documentation
**Objective:** Document Helm chart usage

**Steps:**
1. Create README.md for each chart
2. Document values.yaml parameters
3. Provide installation examples
4. Document upgrade procedures
5. Document rollback procedures

**Acceptance Criteria:**
- Clear installation instructions
- All parameters documented
- Examples provided
- Troubleshooting section included

### Phase 4: AI-Assisted DevOps (Days 7)

#### 4.1 Docker AI (Gordon) Integration
**Objective:** Use Gordon for Docker operations

**Steps:**
1. Enable Gordon in Docker Desktop
2. Test Gordon capabilities
3. Use Gordon for Dockerfile optimization
4. Use Gordon for troubleshooting
5. Document Gordon usage

**Acceptance Criteria:**
- Gordon is enabled and working
- Dockerfile optimizations applied
- Usage examples documented

#### 4.2 kubectl-ai Integration
**Objective:** Use kubectl-ai for Kubernetes operations

**Steps:**
1. Install kubectl-ai
2. Test basic commands
3. Use for deployment operations
4. Use for troubleshooting
5. Document kubectl-ai usage

**Acceptance Criteria:**
- kubectl-ai installed and working
- Deployment examples documented
- Troubleshooting examples documented

#### 4.3 Kagent Integration (Optional)
**Objective:** Use Kagent for advanced cluster operations

**Steps:**
1. Install Kagent
2. Test cluster analysis
3. Use for resource optimization
4. Document Kagent usage

**Acceptance Criteria:**
- Kagent installed and working
- Usage examples documented

### Phase 5: Documentation (Days 8)

#### 5.1 Setup Documentation
**Objective:** Create comprehensive setup guides

**Steps:**
1. Write Docker setup guide
2. Write Minikube setup guide
3. Write Helm setup guide
4. Create quick start guide
5. Add architecture diagrams

**Acceptance Criteria:**
- Step-by-step instructions
- Prerequisites listed
- Common issues addressed
- Diagrams included

#### 5.2 Deployment Documentation
**Objective:** Document deployment procedures

**Steps:**
1. Write deployment guide
2. Document configuration options
3. Document upgrade procedures
4. Document rollback procedures
5. Create troubleshooting guide

**Acceptance Criteria:**
- Clear deployment steps
- Configuration reference complete
- Troubleshooting section comprehensive

## Technical Implementation Details

### Frontend Dockerfile Structure
```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
USER nextjs
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
CMD ["npm", "start"]
```

### Backend Dockerfile Structure
```dockerfile
# Stage 1: Dependencies
FROM python:3.13-alpine AS builder
WORKDIR /app
RUN apk add --no-cache gcc musl-dev postgresql-dev
COPY pyproject.toml ./
RUN pip install --user -e .

# Stage 2: Runtime
FROM python:3.13-alpine
WORKDIR /app
RUN apk add --no-cache libpq
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001
COPY --from=builder /root/.local /home/appuser/.local
COPY src ./src
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
EXPOSE 8001
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"
CMD ["uvicorn", "src.main:app", "--host", "0.0.0", "--port", "8001"]
```

### Kubernetes Resource Specifications

#### Frontend Deployment
- **Replicas:** 2
- **CPU Request:** 100m
- **CPU Limit:** 500m
- **Memory Request:** 128Mi
- **Memory Limit:** 512Mi
- **Liveness Probe:** HTTP GET /health every 30s
- **Readiness Probe:** HTTP GET /health every 10s

#### Backend Deployment
- **Replicas:** 2
- **CPU Request:** 200m
- **CPU Limit:** 1000m
- **Memory Request:** 256Mi
- **Memory Limit:** 1Gi
- **Liveness Probe:** HTTP GET /health every 30s
- **Readiness Probe:** HTTP GET /ready every 10s

### Helm Values Structure

#### Frontend values.yaml
```yaml
replicaCount: 2
image:
  repository: todo-frontend
  tag: latest
  pullPolicy: IfNotPresent
service:
  type: NodePort
  port: 3000
  nodePort: 30000
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
config:
  apiUrl: http://backend-service:8001
```

#### Backend values.yaml
```yaml
replicaCount: 2
image:
  repository: todo-backend
  tag: latest
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 8001
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi
config:
  llmProvider: GROQ
secrets:
  databaseUrl: ""
  groqApiKey: ""
  jwtSecret: ""
```

## Testing Strategy

### Unit Testing
- Dockerfile builds successfully
- Images run locally
- Health checks respond
- Environment variables load

### Integration Testing
- docker-compose full stack test
- Frontend-to-backend communication
- Backend-to-database communication
- Chat functionality end-to-end

### Kubernetes Testing
- Pods reach Running state
- Services are accessible
- ConfigMaps/Secrets mount correctly
- Health checks pass
- Rolling updates work
- Pod restart recovery

### Helm Testing
- Chart installs successfully
- Values override works
- Upgrade works
- Rollback works
- Chart linting passes

## Risk Mitigation

### Risk: Image Build Failures
**Mitigation:**
- Test builds locally first
- Use proven base images
- Document build requirements
- Provide troubleshooting guide

### Risk: Minikube Resource Exhaustion
**Mitigation:**
- Set appropriate resource limits
- Monitor resource usage
- Document minimum requirements
- Provide scaling guidance

### Risk: Network Connectivity Issues
**Mitigation:**
- Test service discovery
- Verify DNS resolution
- Document network configuration
- Provide debugging commands

### Risk: Configuration Errors
**Mitigation:**
- Validate manifests before apply
- Use helm lint
- Test in isolated namespace
- Document configuration options

## Success Metrics

### Performance Metrics
- Image build time < 5 minutes
- Container startup time < 30 seconds
- Helm install time < 2 minutes
- Application response time < 2 seconds

### Quality Metrics
- All health checks passing
- Zero failed deployments
- All tests passing
- Documentation complete

### Operational Metrics
- Successful pod restarts
- Successful rolling updates
- Successful rollbacks
- Zero downtime deployments

## Timeline

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Docker Containerization | 2 days | Dockerfiles, docker-compose.yml |
| Kubernetes Manifests | 2 days | Deployments, Services, ConfigMaps, Secrets |
| Helm Charts | 2 days | Complete Helm charts for both services |
| AI DevOps Tools | 1 day | Gordon, kubectl-ai, kagent integration |
| Documentation | 1 day | Complete documentation suite |
| **Total** | **8 days** | **Production-ready K8s deployment** |

## Next Steps

1. Review and approve this plan
2. Set up development environment
3. Begin Phase 1: Docker Containerization
4. Follow task breakdown in tasks.md
5. Track progress against checklist.md

## References

- [Phase 4 Specification](./spec.md)
- [Phase 3 Implementation](../../phase-3/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-18 | Claude Sonnet 4.5 | Initial implementation plan |
