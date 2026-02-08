# Phase IV: Local Kubernetes Deployment

**Status:** In Progress
**Points:** 250
**Due Date:** January 4, 2026

## Overview

Deploy the Todo AI Chatbot (from Phase III) on a local Kubernetes cluster using Minikube, Helm Charts, and AI-powered DevOps tools.

## Objectives

- Containerize frontend (Next.js) and backend (FastAPI + AI Chat) applications
- Deploy on Minikube (local Kubernetes cluster)
- Create Helm charts for package management
- Use AI DevOps tools (Docker AI/Gordon, kubectl-ai, Kagent)
- Implement cloud-native best practices

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

## Planned Directory Structure

```
phase-4/
├── README.md                    # This file
├── docker/
│   ├── frontend/
│   │   └── Dockerfile          # Next.js containerization
│   └── backend/
│       └── Dockerfile          # FastAPI containerization
├── kubernetes/
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── configmap.yaml
│   └── secrets.yaml
├── helm/
│   └── todo-chatbot/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── backend-deployment.yaml
│           └── backend-service.yaml
└── docs/
    ├── DEPLOYMENT.md           # Deployment instructions
    └── AIOPS.md               # AIOps tools usage guide
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

## Prerequisites

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

## Deployment Instructions (Planned)

### 1. Start Minikube

```bash
# Start Minikube cluster
minikube start --driver=docker --cpus=4 --memory=8192

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

### 2. Build Docker Images

```bash
# Build frontend image
cd phase-3/frontend
docker build -t todo-frontend:latest .

# Build backend image
cd ../backend
docker build -t todo-backend:latest .

# Load images into Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest
```

### 3. Deploy with Kubernetes Manifests

```bash
# Apply ConfigMap and Secrets
kubectl apply -f kubernetes/configmap.yaml
kubectl apply -f kubernetes/secrets.yaml

# Deploy backend
kubectl apply -f kubernetes/backend-deployment.yaml
kubectl apply -f kubernetes/backend-service.yaml

# Deploy frontend
kubectl apply -f kubernetes/frontend-deployment.yaml
kubectl apply -f kubernetes/frontend-service.yaml

# Check deployment status
kubectl get pods
kubectl get services
```

### 4. Deploy with Helm (Alternative)

```bash
# Install Helm chart
helm install todo-chatbot ./helm/todo-chatbot

# Check deployment
helm list
kubectl get pods

# Upgrade deployment
helm upgrade todo-chatbot ./helm/todo-chatbot

# Uninstall
helm uninstall todo-chatbot
```

### 5. Access the Application

```bash
# Get Minikube IP
minikube ip

# Port forward to access services
kubectl port-forward service/frontend 3000:3000
kubectl port-forward service/backend 8000:8000

# Or use Minikube tunnel
minikube tunnel
```

## Environment Variables

The following environment variables need to be configured in Kubernetes Secrets:

| Variable | Description | Source |
|----------|-------------|--------|
| `DATABASE_URL` | Neon PostgreSQL connection string | Neon Dashboard |
| `BETTER_AUTH_SECRET` | JWT secret key | Generated |
| `OPENROUTER_API_KEY` | OpenRouter/Groq API key | OpenRouter Dashboard |
| `OPENROUTER_BASE_URL` | API base URL | `https://openrouter.ai/api/v1` |
| `OPENROUTER_MODEL` | AI model to use | `anthropic/claude-3.5-sonnet` |
| `FRONTEND_URL` | Frontend URL | `http://localhost:3000` |

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

## Development Approach

Following **Spec-Driven Development (SDD)** workflow:

1. **Specify** → Write specifications for Kubernetes deployment
2. **Plan** → Design architecture and component breakdown
3. **Tasks** → Break down into actionable tasks
4. **Implement** → Execute using Claude Code

**No manual coding allowed** - Use Claude Code to generate all configurations and manifests.

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

## Next Steps

1. Create Docker configurations for frontend and backend
2. Generate Kubernetes manifests using kubectl-ai
3. Package application as Helm chart
4. Test deployment on Minikube
5. Document deployment process
6. Create demo video (max 90 seconds)
7. Submit to hackathon

## Submission Requirements

- [ ] Public GitHub repository with all Phase IV code
- [ ] Working Minikube deployment
- [ ] Helm charts for easy deployment
- [ ] README with setup instructions
- [ ] Demo video (max 90 seconds)
- [ ] Documentation of AIOps tools usage

## Notes

- Phase IV builds on Phase III (AI-Powered Todo Chatbot)
- Ensure Phase III is fully functional before starting Phase IV
- Use Spec-Driven Development approach throughout
- Leverage AI DevOps tools for efficiency
- Document all steps for reproducibility

---

**Last Updated:** February 8, 2026
**Hackathon:** Evolution of Todo - Phase IV
**Repository:** https://github.com/syeda-inshrah/speckit-hackathon
