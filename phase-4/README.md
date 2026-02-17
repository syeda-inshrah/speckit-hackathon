# Phase 4: Local Kubernetes Deployment

**Status:** 📋 Planning Complete - Ready for Implementation
**Date:** 2026-02-18
**Duration:** 8 days (estimated)
**Points:** 200
**Objective:** Deploy Phase 3 Todo Chatbot to local Kubernetes cluster using Minikube

## Overview

Phase 4 transforms the Phase 3 AI-powered Todo Chatbot into a cloud-native application deployed on a local Kubernetes cluster. This phase introduces containerization with Docker, orchestration with Kubernetes, and package management with Helm Charts.

**Planning Completed:**
- ✅ Comprehensive specifications (7 documents)
- ✅ Implementation plan with Architecture Decision Records
- ✅ Task breakdown (35 tasks)
- ✅ Technical research and best practices
- ✅ Contract documents (8 contracts)
- ✅ Data models and schemas
- ✅ Comprehensive checklist

## Objectives

- Containerize frontend (Next.js) and backend (FastAPI + MCP) applications
- Deploy on Minikube (local Kubernetes cluster)
- Create Helm charts for package management
- Use AI DevOps tools (Docker AI/Gordon, kubectl-ai, Kagent)
- Implement cloud-native best practices
- Achieve zero-downtime deployments

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Containerization** | Docker (Docker Desktop) |
| **Docker AI** | Docker AI Agent (Gordon) |
| **Orchestration** | Kubernetes (Minikube) |
| **Package Manager** | Helm Charts |
| **AI DevOps** | kubectl-ai, Kagent |
| **Application** | Phase III Todo Chatbot |

## Requirements

### 1. Containerization
- [x] Dockerize frontend application (Next.js)
- [x] Dockerize backend application (FastAPI with AI chat)
- [ ] Use Docker AI Agent (Gordon) for AI-assisted operations
- [ ] Optimize Docker images (multi-stage builds)

### 2. Kubernetes Manifests
- [ ] Create Deployment manifests for frontend and backend
- [ ] Create Service manifests for networking
- [ ] Create ConfigMap for application configuration
- [ ] Create Secrets for sensitive data (API keys, DB credentials)
- [ ] Create Ingress for external access (optional)

### 3. Helm Charts
- [ ] Package application as Helm chart
- [ ] Create `Chart.yaml` with metadata
- [ ] Create `values.yaml` for configuration
- [ ] Create templates for Kubernetes resources
- [ ] Support easy deployment and upgrades

### 4. AIOps Integration
- [ ] Use Docker AI (Gordon) for container operations
- [ ] Use kubectl-ai for Kubernetes operations
- [ ] Use Kagent for cluster analysis and optimization

## 📁 Project Structure

```
hackathon-02/
├── specs/                             # Root specs folder
│   └── phase-4/                       # ✅ Phase 4 specifications
│       ├── spec.md                    # Main specification document
│       ├── plan.md                    # Implementation plan with ADRs
│       ├── tasks.md                   # Task breakdown (35 tasks)
│       ├── research.md                # Technical research & best practices
│       ├── data-model.md              # Data models & schemas
│       ├── checklist.md               # Comprehensive checklist
│       ├── SUMMARY.md                 # Executive summary
│       └── contracts/                 # Contract documents
│           ├── README.md              # Contracts overview
│           ├── docker-backend-contract.md
│           ├── docker-frontend-contract.md
│           ├── docker-compose-contract.md
│           ├── k8s-backend-deployment-contract.md
│           ├── k8s-frontend-deployment-contract.md
│           ├── helm-backend-contract.md
│           ├── helm-frontend-contract.md
│           └── minikube-setup-contract.md
└── phase-4/
    ├── README.md                      # This file
    ├── frontend/                      # Frontend Docker artifacts (to be created)
    │   ├── Dockerfile
    │   └── .dockerignore
    ├── backend/                       # Backend Docker artifacts (to be created)
    │   ├── Dockerfile
    │   └── .dockerignore
    ├── docker-compose.yml             # Local testing (to be created)
    ├── k8s/                           # Kubernetes manifests (to be created)
    │   ├── frontend/
    │   │   ├── deployment.yaml
    │   │   ├── service.yaml
    │   │   └── configmap.yaml
    │   └── backend/
    │       ├── deployment.yaml
    │       ├── service.yaml
    │       ├── configmap.yaml
    │       └── secret.yaml
    ├── helm/                          # Helm charts (to be created)
    │   ├── frontend/
    │   │   ├── Chart.yaml
    │   │   ├── values.yaml
    │   │   └── templates/
    │   └── backend/
    │       ├── Chart.yaml
    │       ├── values.yaml
    │       └── templates/
    └── docs/                          # Documentation (to be created)
        ├── DOCKER.md
        ├── KUBERNETES.md
        ├── HELM.md
        └── TROUBLESHOOTING.md
```

## AIOps Tools Usage

### Docker AI (Gordon)

```bash
# Check capabilities
docker ai "What can you do?"

# Build images with AI assistance
docker ai "Build optimized images for Next.js and FastAPI"

# Troubleshoot container issues
docker ai "Why is my container failing to start?"
```

**Note:** Enable Gordon in Docker Desktop 4.53+ → Settings → Beta features

### kubectl-ai

```bash
# Deploy with AI assistance
kubectl-ai "deploy the todo frontend with 2 replicas"

# Scale applications
kubectl-ai "scale the backend to handle more load"

# Troubleshoot issues
kubectl-ai "check why the pods are failing"
```

### Kagent

```bash
# Analyze cluster health
kagent "analyze the cluster health"

# Optimize resources
kagent "optimize resource allocation"

# Get recommendations
kagent "suggest improvements for my deployment"
```

## 📚 Documentation

### Specification Documents

| Document | Purpose | Audience |
|----------|---------|----------|
| [spec.md](../specs/phase-4/spec.md) | Complete Phase 4 specification | All teams |
| [plan.md](../specs/phase-4/plan.md) | Implementation plan with ADRs | Developers, DevOps |
| [tasks.md](../specs/phase-4/tasks.md) | Detailed task breakdown (35 tasks) | Developers |
| [research.md](../specs/phase-4/research.md) | Technical research & best practices | Developers, DevOps |
| [data-model.md](../specs/phase-4/data-model.md) | Data models & schemas | Developers |
| [checklist.md](../specs/phase-4/checklist.md) | Comprehensive checklist | All teams |
| [SUMMARY.md](../specs/phase-4/SUMMARY.md) | Executive summary | Management, Stakeholders |

### Contract Documents

See [contracts/README.md](../specs/phase-4/contracts/README.md) for complete list of 8 contract documents covering Docker, Kubernetes, Helm, and Minikube.

---

## 🎯 Implementation Phases

### Phase 1: Docker Containerization (Days 1-2)
- [ ] Create frontend Dockerfile
- [ ] Create backend Dockerfile
- [ ] Implement health checks
- [ ] Create docker-compose.yml
- [ ] Test locally

### Phase 2: Kubernetes Manifests (Days 3-4)
- [ ] Setup Minikube
- [ ] Create K8s manifests
- [ ] Deploy to Minikube
- [ ] Test end-to-end

### Phase 3: Helm Charts (Days 5-6)
- [ ] Create Helm chart structure
- [ ] Templatize manifests
- [ ] Test installation/upgrade/rollback
- [ ] Document charts

### Phase 4: AI-Assisted DevOps (Day 7)
- [ ] Setup Docker AI (Gordon)
- [ ] Setup kubectl-ai
- [ ] Document usage

### Phase 5: Documentation (Day 8)
- [ ] Create setup guides
- [ ] Create deployment guides
- [ ] Create troubleshooting guides

**Track Progress:** Use [checklist.md](../specs/phase-4/checklist.md) for detailed task tracking

---

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Disk: 20GB free

**Recommended:**
- CPU: 6 cores
- RAM: 12GB
- Disk: 40GB free

### Install Minikube

```bash
# macOS
brew install minikube

# Windows (using Chocolatey)
choco install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### Install kubectl

```bash
# macOS
brew install kubectl

# Windows (using Chocolatey)
choco install kubernetes-cli

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### Install Helm

```bash
# macOS
brew install helm

# Windows (using Chocolatey)
choco install kubernetes-helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Install kubectl-ai

```bash
# Install kubectl-ai
go install github.com/GoogleCloudPlatform/kubectl-ai@latest
```

### Install Kagent

```bash
# Install Kagent
npm install -g @kagent-dev/kagent
```

## 🚀 Quick Start

### 1. Start Minikube

```bash
# Start Minikube with recommended resources
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=40g \
  --driver=docker \
  --kubernetes-version=v1.28.0

# Verify cluster is running
minikube status
kubectl cluster-info
kubectl get nodes

# Enable metrics server (optional)
minikube addons enable metrics-server
```

### 2. Build Docker Images

```bash
# Point Docker to Minikube's Docker daemon
eval $(minikube docker-env)

# Build frontend image
docker build -t todo-frontend:latest \
  -f phase-4/frontend/Dockerfile \
  phase-3/frontend

# Build backend image
docker build -t todo-backend:latest \
  -f phase-4/backend/Dockerfile \
  phase-3/backend

# Verify images
docker images | grep todo
```

### 3. Deploy with Kubernetes Manifests

```bash
# Deploy backend
kubectl apply -f phase-4/k8s/backend/

# Deploy frontend
kubectl apply -f phase-4/k8s/frontend/

# Verify deployments
kubectl get deployments
kubectl get pods
kubectl get services

# Access frontend
minikube service frontend-service --url
```

### 4. Deploy with Helm (Alternative)

```bash
# Install backend chart
helm install backend phase-4/helm/backend \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.betterAuthSecret="your-secret" \
  --set secrets.groqApiKey="your-key"

# Install frontend chart
helm install frontend phase-4/helm/frontend

# Verify installations
helm list
kubectl get all

# Upgrade
helm upgrade backend phase-4/helm/backend
helm upgrade frontend phase-4/helm/frontend

# Uninstall
helm uninstall backend
helm uninstall frontend
```

### 5. Access the Application

```bash
# Access frontend (NodePort)
minikube service frontend-service --url
# Opens browser to http://192.168.49.2:30000

# Or port forward
kubectl port-forward service/frontend-service 3000:3000
# Access at http://localhost:3000

# Check backend (internal only)
kubectl run test-pod --image=curlimages/curl --rm -it -- \
  curl http://backend-service:8001/health
```

---

## 📊 Success Metrics

### Technical Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Frontend image size | <200MB | 📋 Planned |
| Backend image size | <300MB | 📋 Planned |
| Build time (first) | <5 min | 📋 Planned |
| Build time (cached) | <2 min | 📋 Planned |
| Frontend startup | <15s | 📋 Planned |
| Backend startup | <30s | 📋 Planned |
| All health checks | Passing | 📋 Planned |
| Zero downtime updates | Yes | 📋 Planned |

---

## 🔐 Security

### Security Best Practices

✅ **Container Security:**
- Non-root user execution (UID 1001)
- No privilege escalation
- All capabilities dropped
- Minimal base images (Alpine)
- Regular security updates

✅ **Kubernetes Security:**
- Pod Security Standards (Restricted)
- RBAC enabled
- Secrets for sensitive data
- Network policies (optional)
- Security context configured

✅ **Secret Management:**
- No hardcoded secrets
- Kubernetes Secrets for credentials
- .env files in .gitignore
- Secrets rotation support

---

## Environment Variables

The following environment variables need to be configured:

**Backend (via Kubernetes Secret):**
- `DATABASE_URL` - Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET` - JWT secret key (min 32 chars)
- `GROQ_API_KEY` - Groq API key
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `JWT_EXPIRATION_DAYS` - JWT expiration (default: 7)

**Backend (via ConfigMap):**
- `LLM_PROVIDER` - LLM provider (GROQ/OPENROUTER)
- `FRONTEND_URL` - Frontend URL for CORS
- `GROQ_BASE_URL` - Groq API base URL
- `GROQ_MODEL` - Groq model name

**Frontend (via ConfigMap):**
- `NEXT_PUBLIC_API_URL` - Backend API URL
- `NODE_ENV` - Environment mode (production)

## Monitoring and Debugging

```bash
# View pod logs
kubectl logs <pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# Describe pod for troubleshooting
kubectl describe pod <pod-name>

# Execute commands in pod
kubectl exec -it <pod-name> -- /bin/bash

# View cluster events
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Minikube won't start**
```bash
# Check Docker is running
docker ps

# Delete and recreate cluster
minikube delete
minikube start --cpus=4 --memory=8192
```

**Issue: Image pull errors**
```bash
# Build images in Minikube context
eval $(minikube docker-env)
docker build -t todo-frontend:latest -f phase-4/frontend/Dockerfile phase-3/frontend
docker build -t todo-backend:latest -f phase-4/backend/Dockerfile phase-3/backend
```

**Issue: Pods not starting**
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

**For more troubleshooting:** See [TROUBLESHOOTING.md](./docs/TROUBLESHOOTING.md) (to be created)

---

## Development Approach

Following **Spec-Driven Development (SDD)** workflow:

1. ✅ **Specify** → Comprehensive specifications completed
2. ✅ **Plan** → Architecture and ADRs documented
3. ✅ **Tasks** → 35 tasks broken down with dependencies
4. 📋 **Implement** → Ready to execute using Claude Code

**Planning Phase Complete** - All specifications, plans, tasks, research, contracts, and checklists are ready for implementation.

## Resources

### Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Docker AI (Gordon)](https://docs.docker.com/ai/gordon/)
- [kubectl-ai GitHub](https://github.com/GoogleCloudPlatform/kubectl-ai)
- [Kagent GitHub](https://github.com/kagent-dev/kagent)

### Tutorials
- [Kubernetes Basics](https://kubernetes.io/docs/tutorials/kubernetes-basics/)
- [Helm Getting Started](https://helm.sh/docs/chart_template_guide/getting_started/)
- [Minikube Tutorial](https://minikube.sigs.k8s.io/docs/start/)

---

## 📞 Support

### Getting Help

**Documentation:**
- Read [spec.md](../specs/phase-4/spec.md) for complete specifications
- Check [contracts](../specs/phase-4/contracts/) for detailed requirements
- Review [SUMMARY.md](../specs/phase-4/SUMMARY.md) for executive overview
- Use [checklist.md](../specs/phase-4/checklist.md) to track progress

**Team Contacts:**
- Technical Lead: Architecture and design decisions
- Backend Team: Backend implementation
- Frontend Team: Frontend implementation
- DevOps Team: Infrastructure and deployment
- QA Team: Testing and validation

---

## 📚 References

### Internal
- [Hackathon Specification](../Hackathon II - Todo Spec-Driven Development.md)
- [Phase 3 Implementation](../phase-3/)

### External
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

---

## Next Steps

### Immediate Actions

1. **Review and Approve Specifications**
   - Technical lead review
   - Stakeholder approval

2. **Setup Development Environment**
   - Install required tools
   - Configure Minikube
   - Verify prerequisites

3. **Begin Implementation**
   - Start with Phase 1 (Docker)
   - Follow [tasks.md](../specs/phase-4/tasks.md)
   - Track progress with [checklist.md](../specs/phase-4/checklist.md)

### Phase 5 Preparation

**Cloud Deployment Planning:**
- Choose cloud provider (GKE, EKS, AKS)
- Plan Kafka integration
- Plan Dapr integration
- Plan CI/CD pipeline

---

## Submission Requirements

- [ ] Public GitHub repository with all Phase 4 code
- [ ] Working Minikube deployment
- [ ] Helm charts for easy deployment
- [ ] Complete documentation
- [ ] Demo video (max 90 seconds)
- [ ] AIOps tools usage documented

---

**Last Updated:** 2026-02-18
**Version:** 1.0.0
**Status:** 📋 Planning Complete - Ready for Implementation
**Repository:** https://github.com/syeda-inshrah/speckit-hackathon
