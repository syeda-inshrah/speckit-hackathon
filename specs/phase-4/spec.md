# Phase 4: Local Kubernetes Deployment Specification

## Overview

**Phase:** IV - Local Kubernetes Deployment
**Objective:** Deploy the Phase 3 Todo Chatbot on a local Kubernetes cluster using Minikube, Helm Charts, and AI-assisted DevOps tools
**Status:** Planning
**Date:** 2026-02-18

## Context

Building upon Phase 3's AI-powered chatbot, Phase 4 focuses on containerizing the application and deploying it to a local Kubernetes environment. This phase introduces cloud-native deployment patterns, container orchestration, and infrastructure-as-code practices using Helm charts.

## Goals

### Primary Goals
1. Containerize frontend (Next.js) and backend (FastAPI) applications
2. Create production-ready Docker images with optimization
3. Deploy applications to local Minikube cluster
4. Implement Helm charts for repeatable deployments
5. Use AI-assisted DevOps tools (Gordon, kubectl-ai, kagent)

### Success Criteria
- [ ] Docker images build successfully for both services
- [ ] Containers run locally with docker-compose
- [ ] Minikube cluster deploys all components
- [ ] Helm charts install without errors
- [ ] All pods reach Running state
- [ ] Frontend-to-backend communication works
- [ ] Backend connects to Neon DB successfully
- [ ] Chat functionality works end-to-end in K8s
- [ ] Application survives pod restarts

## Scope

### In Scope
- Docker containerization of existing Phase 3 application
- Multi-stage Docker builds for optimization
- Docker Compose for local testing
- Kubernetes deployment manifests
- Helm chart creation for both services
- ConfigMaps for configuration management
- Secrets for sensitive data
- Service networking configuration
- Minikube local deployment
- Health checks and readiness probes
- Resource limits and requests
- Documentation for setup and deployment

### Out of Scope
- Cloud deployment (reserved for Phase 5)
- Kafka/event-driven architecture (Phase 5)
- Dapr integration (Phase 5)
- CI/CD pipelines (Phase 5)
- Advanced features (recurring tasks, reminders - Phase 5)
- Horizontal Pod Autoscaling
- Ingress controllers (optional)
- Monitoring and logging infrastructure
- Database migration to Kubernetes

## User Stories

### As a DevOps Engineer
- I want to containerize the application so that it can run consistently across environments
- I want to use Helm charts so that deployments are repeatable and configurable
- I want to deploy to Minikube so that I can test Kubernetes configurations locally
- I want to use AI tools (Gordon, kubectl-ai) so that I can work more efficiently

### As a Developer
- I want the application to run in Kubernetes so that it's production-ready
- I want health checks so that Kubernetes can automatically restart failed containers
- I want environment-based configuration so that I can deploy to different environments
- I want to test locally before cloud deployment

### As a System Administrator
- I want proper resource limits so that containers don't consume excessive resources
- I want secrets management so that credentials are stored securely
- I want service discovery so that components can communicate reliably
- I want documentation so that I can maintain the deployment

## Technical Requirements

### Docker Requirements

#### Frontend Container
- Base image: Node.js 20 Alpine
- Multi-stage build (build → production)
- Non-root user execution
- Health check endpoint
- Environment variable configuration
- Optimized layer caching
- Size target: < 200MB

#### Backend Container
- Base image: Python 3.13 Alpine
- Multi-stage build (dependencies → runtime)
- Non-root user execution
- Health check endpoint
- Environment variable configuration
- Optimized layer caching
- Size target: < 300MB

#### Docker Compose
- Frontend service definition
- Backend service definition
- Network configuration
- Volume mounts for development
- Environment variable files
- Health check configuration

### Kubernetes Requirements

#### Deployments
- Frontend: 2 replicas minimum
- Backend: 2 replicas minimum
- Rolling update strategy
- Resource requests and limits
- Liveness and readiness probes
- Environment variables from ConfigMap
- Secrets mounted as volumes or env vars

#### Services
- Frontend: NodePort or LoadBalancer
- Backend: ClusterIP (internal)
- Proper port mapping
- Service discovery labels

#### ConfigMaps
- Frontend configuration (API URL, etc.)
- Backend configuration (non-sensitive)
- Application settings

#### Secrets
- Database connection string
- API keys (Groq, OpenAI)
- JWT secret
- Better Auth secret

### Helm Requirements

#### Chart Structure
```
helm/
├── frontend/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── templates/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   └── _helpers.tpl
│   └── .helmignore
└── backend/
    ├── Chart.yaml
    ├── values.yaml
    ├── templates/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── configmap.yaml
    │   ├── secret.yaml
    │   └── _helpers.tpl
    └── .helmignore
```

#### Values Configuration
- Configurable replica counts
- Configurable resource limits
- Configurable image tags
- Environment-specific overrides
- Service type configuration

### Minikube Requirements
- Minimum resources: 4 CPU, 8GB RAM
- Docker driver
- Ingress addon (optional)
- Metrics server (optional)
- Dashboard access

## Architecture

### Container Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Docker Images                         │
│                                                          │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │  Frontend Image  │      │  Backend Image   │        │
│  │                  │      │                  │        │
│  │  - Next.js App   │      │  - FastAPI App   │        │
│  │  - Node 20       │      │  - Python 3.13   │        │
│  │  - Port 3000     │      │  - Port 8001     │        │
│  │  - Health Check  │      │  - Health Check  │        │
│  └──────────────────┘      └──────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Kubernetes Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      Minikube Cluster                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Namespace: default                       │ │
│  │                                                             │ │
│  │  ┌──────────────────┐         ┌──────────────────┐        │ │
│  │  │ Frontend Deploy  │         │ Backend Deploy   │        │ │
│  │  │  - 2 Replicas    │         │  - 2 Replicas    │        │ │
│  │  │  - Port 3000     │         │  - Port 8001     │        │ │
│  │  └────────┬─────────┘         └────────┬─────────┘        │ │
│  │           │                            │                   │ │
│  │  ┌────────▼─────────┐         ┌────────▼─────────┐        │ │
│  │  │ Frontend Service │         │ Backend Service  │        │ │
│  │  │  - NodePort      │         │  - ClusterIP     │        │ │
│  │  │  - Port 30000    │         │  - Port 8001     │        │ │
│  │  └──────────────────┘         └──────────────────┘        │ │
│  │           │                            ▲                   │ │
│  │           └────────────────────────────┘                   │ │
│  │                                                             │ │
│  │  ┌──────────────────┐         ┌──────────────────┐        │ │
│  │  │   ConfigMaps     │         │     Secrets      │        │ │
│  │  │  - Frontend cfg  │         │  - DB credentials│        │ │
│  │  │  - Backend cfg   │         │  - API keys      │        │ │
│  │  └──────────────────┘         └──────────────────┘        │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                                │
│                           ▼                                    │
│                  ┌──────────────────┐                         │
│                  │   External DB    │                         │
│                  │  Neon PostgreSQL │                         │
│                  └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Non-Functional Requirements

### Performance
- Container startup time: < 30 seconds
- Image build time: < 5 minutes
- Helm install time: < 2 minutes
- Application response time: < 2 seconds

### Security
- Non-root container execution
- Secrets stored in Kubernetes Secrets
- No hardcoded credentials in images
- Read-only root filesystem (where possible)
- Security context constraints

### Reliability
- Health checks for automatic recovery
- Rolling updates with zero downtime
- Graceful shutdown handling
- Persistent data handling

### Maintainability
- Clear documentation
- Parameterized Helm charts
- Consistent naming conventions
- Proper labeling and annotations

## Dependencies

### External Dependencies
- Docker Desktop 4.53+ (for Gordon)
- Minikube 1.32+
- kubectl 1.28+
- Helm 3.12+
- kubectl-ai (optional)
- Kagent (optional)

### Application Dependencies
- Phase 3 Todo Chatbot (completed)
- Neon PostgreSQL database (external)
- Groq API (external)

## Constraints

### Technical Constraints
- Must run on local Minikube (no cloud resources)
- Must use existing Phase 3 application code
- Must maintain connection to external Neon DB
- Must support both development and production configs

### Resource Constraints
- Local machine resources (CPU, RAM, disk)
- Minikube resource limits
- Docker Desktop resource allocation

### Time Constraints
- Must complete before Phase 5
- Must follow spec-driven development workflow

## Risks and Mitigations

### Risk: Docker image size too large
**Impact:** Slow builds and deployments
**Mitigation:** Use multi-stage builds, Alpine base images, optimize layers

### Risk: Minikube resource exhaustion
**Impact:** Pods fail to start or crash
**Mitigation:** Set appropriate resource limits, monitor usage, increase Minikube resources

### Risk: Network connectivity issues
**Impact:** Services can't communicate
**Mitigation:** Proper service configuration, DNS testing, network policies

### Risk: Configuration management complexity
**Impact:** Difficult to maintain multiple environments
**Mitigation:** Use Helm values, ConfigMaps, clear documentation

### Risk: Gordon/kubectl-ai unavailable
**Impact:** Can't use AI-assisted tools
**Mitigation:** Fallback to standard Docker/kubectl commands, document both approaches

## Acceptance Criteria

### Docker Acceptance Criteria
- [ ] Frontend Dockerfile builds without errors
- [ ] Backend Dockerfile builds without errors
- [ ] Images are optimized (multi-stage builds)
- [ ] Images run as non-root user
- [ ] Health checks are implemented
- [ ] docker-compose.yml works locally
- [ ] Images are tagged properly

### Kubernetes Acceptance Criteria
- [ ] All deployments reach Running state
- [ ] Services are accessible
- [ ] ConfigMaps are applied correctly
- [ ] Secrets are mounted properly
- [ ] Health checks pass
- [ ] Resource limits are set
- [ ] Rolling updates work

### Helm Acceptance Criteria
- [ ] Charts install without errors
- [ ] Charts can be upgraded
- [ ] Charts can be rolled back
- [ ] Values override works
- [ ] Templates render correctly
- [ ] Chart documentation is complete

### Functional Acceptance Criteria
- [ ] Frontend loads in browser
- [ ] Backend API responds
- [ ] Chat functionality works
- [ ] Database connection succeeds
- [ ] User authentication works
- [ ] Task operations work via chat
- [ ] Application survives pod restarts

## Documentation Requirements

### Required Documentation
1. Docker setup guide
2. Minikube installation guide
3. Helm chart usage guide
4. Deployment procedures
5. Troubleshooting guide
6. Architecture diagrams
7. Configuration reference

### Documentation Format
- Markdown format
- Clear step-by-step instructions
- Code examples
- Screenshots where helpful
- Troubleshooting section

## Testing Strategy

### Docker Testing
- Build images locally
- Run containers with docker-compose
- Test health endpoints
- Verify environment variables
- Check container logs

### Kubernetes Testing
- Deploy to Minikube
- Verify pod status
- Test service connectivity
- Check ConfigMap/Secret mounting
- Test rolling updates
- Simulate pod failures

### Integration Testing
- End-to-end chat flow
- Database connectivity
- API authentication
- Task CRUD operations
- Multi-pod communication

## Deliverables

1. **Docker Artifacts**
   - `phase-4/frontend/Dockerfile`
   - `phase-4/backend/Dockerfile`
   - `phase-4/docker-compose.yml`
   - `.dockerignore` files

2. **Kubernetes Manifests**
   - `phase-4/k8s/frontend/` (deployment, service, configmap)
   - `phase-4/k8s/backend/` (deployment, service, configmap, secret)

3. **Helm Charts**
   - `phase-4/helm/frontend/` (complete chart)
   - `phase-4/helm/backend/` (complete chart)

4. **Documentation**
   - `phase-4/README.md` (main guide)
   - `phase-4/docs/DOCKER.md` (Docker guide)
   - `phase-4/docs/KUBERNETES.md` (K8s guide)
   - `phase-4/docs/HELM.md` (Helm guide)
   - `phase-4/docs/TROUBLESHOOTING.md`

5. **Specification Documents**
   - `phase-4/specs/spec.md` (this document)
   - `phase-4/specs/plan.md`
   - `phase-4/specs/tasks.md`
   - `phase-4/specs/research.md`
   - `phase-4/specs/checklist.md`
   - `phase-4/specs/contracts/`

## References

- [Hackathon Specification](../Hackathon II - Todo Spec-Driven Development.md)
- [Phase 3 Implementation](../phase-3/)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-18 | Claude Sonnet 4.5 | Initial specification |
