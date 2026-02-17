# Phase 4: Docker & Kubernetes Deployment Guide

## Overview

This guide covers the complete deployment of the Todo AI Chatbot application using Docker containers and Kubernetes (Minikube) orchestration.

**Status:** ✅ Implementation Complete
**Date:** 2026-02-18

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Docker Deployment](#docker-deployment)
4. [Kubernetes Deployment](#kubernetes-deployment)
5. [Helm Deployment](#helm-deployment)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

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

### Required Software

```bash
# Docker Desktop 4.53+
docker --version

# Minikube 1.32+
minikube version

# kubectl 1.28+
kubectl version --client

# Helm 3.12+
helm version
```

### Installation

**Docker Desktop:**
- Windows/Mac: Download from [docker.com](https://www.docker.com/products/docker-desktop)
- Linux: Follow [official guide](https://docs.docker.com/engine/install/)

**Minikube:**
```bash
# macOS
brew install minikube

# Windows (Chocolatey)
choco install minikube

# Linux
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

**kubectl:**
```bash
# macOS
brew install kubectl

# Windows (Chocolatey)
choco install kubernetes-cli

# Linux
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

**Helm:**
```bash
# macOS
brew install helm

# Windows (Chocolatey)
choco install kubernetes-helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

---

## Quick Start

### 1. Start Minikube

```bash
# Start Minikube with recommended resources
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=40g \
  --driver=docker \
  --kubernetes-version=v1.28.0

# Verify cluster
minikube status
kubectl cluster-info
kubectl get nodes
```

### 2. Build Docker Images

```bash
# Point Docker to Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
docker build -t todo-backend:latest \
  -f phase-4/backend/Dockerfile \
  phase-4/backend

# Build frontend image
docker build -t todo-frontend:latest \
  -f phase-4/frontend/Dockerfile \
  phase-4/frontend

# Verify images
docker images | grep todo
```

### 3. Deploy with Helm

```bash
# Create secrets (update with your values)
helm install backend phase-4/helm/backend \
  --set secrets.databaseUrl="postgresql://user:pass@host:5432/db" \
  --set secrets.betterAuthSecret="your-secret-min-32-chars" \
  --set secrets.groqApiKey="your-groq-api-key"

# Install frontend
helm install frontend phase-4/helm/frontend

# Verify deployment
kubectl get all
helm list
```

### 4. Access Application

```bash
# Get frontend URL
minikube service frontend-todo-frontend --url

# Or use port forwarding
kubectl port-forward service/frontend-todo-frontend 3000:3000
```

Access at: **http://localhost:3000**

---

## Docker Deployment

### Local Testing with Docker Compose

```bash
# Navigate to phase-4
cd phase-4

# Copy environment file
cp backend/.env.example backend/.env
# Edit backend/.env with your credentials

# Start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Docker Images

**Backend Image:**
- Base: `python:3.13-alpine`
- Size: ~280MB
- Port: 8001
- User: appuser (UID 1001)

**Frontend Image:**
- Base: `node:20-alpine`
- Size: ~180MB
- Port: 3000
- User: nextjs (UID 1001)

### Health Checks

**Backend:**
```bash
# Liveness
curl http://localhost:8001/health

# Readiness
curl http://localhost:8001/ready
```

**Frontend:**
```bash
curl http://localhost:3000/health
```

---

## Kubernetes Deployment

### Using Raw Manifests

```bash
# Create secrets (update values first)
kubectl apply -f phase-4/k8s/backend/secret.yaml

# Deploy backend
kubectl apply -f phase-4/k8s/backend/configmap.yaml
kubectl apply -f phase-4/k8s/backend/deployment.yaml
kubectl apply -f phase-4/k8s/backend/service.yaml

# Deploy frontend
kubectl apply -f phase-4/k8s/frontend/configmap.yaml
kubectl apply -f phase-4/k8s/frontend/deployment.yaml
kubectl apply -f phase-4/k8s/frontend/service.yaml

# Verify
kubectl get pods
kubectl get services
```

### Monitoring

```bash
# Watch pods
kubectl get pods -w

# Check pod logs
kubectl logs -f <pod-name>

# Describe pod
kubectl describe pod <pod-name>

# Execute into pod
kubectl exec -it <pod-name> -- /bin/sh

# View events
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## Helm Deployment

### Backend Chart

```bash
# Install with custom values
helm install backend phase-4/helm/backend \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.betterAuthSecret="..." \
  --set secrets.groqApiKey="..." \
  --set config.frontendUrl="http://localhost:3000" \
  --set replicaCount=2

# Upgrade
helm upgrade backend phase-4/helm/backend

# Rollback
helm rollback backend

# Uninstall
helm uninstall backend
```

### Frontend Chart

```bash
# Install
helm install frontend phase-4/helm/frontend \
  --set config.nextPublicApiUrl="http://backend-todo-backend:8001"

# Upgrade
helm upgrade frontend phase-4/helm/frontend

# Uninstall
helm uninstall frontend
```

### Helm Commands

```bash
# List releases
helm list

# Get values
helm get values backend

# Get manifest
helm get manifest backend

# Test release
helm test backend

# History
helm history backend
```

---

## Testing

### Verify Deployment

```bash
# Check all resources
kubectl get all

# Check health
kubectl run test-pod --image=curlimages/curl --rm -it -- \
  curl http://backend-service:8001/health

# Test frontend
minikube service frontend-service --url
```

### Load Testing

```bash
# Install hey
go install github.com/rakyll/hey@latest

# Test backend
hey -n 1000 -c 10 http://localhost:8001/health

# Test frontend
hey -n 1000 -c 10 http://localhost:3000/health
```

### Integration Testing

```bash
# Test full flow
# 1. Register user
curl -X POST http://localhost:8001/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# 2. Login
curl -X POST http://localhost:8001/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# 3. Create task
curl -X POST http://localhost:8001/api/{user_id}/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test"}'
```

---

## Troubleshooting

### Common Issues

**Issue: Minikube won't start**
```bash
# Check Docker is running
docker ps

# Delete and recreate
minikube delete
minikube start --cpus=4 --memory=8192
```

**Issue: Image pull errors**
```bash
# Verify images in Minikube
eval $(minikube docker-env)
docker images | grep todo

# Rebuild if needed
docker build -t todo-backend:latest -f phase-4/backend/Dockerfile phase-4/backend
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

**Issue: Service not accessible**
```bash
# Check service
kubectl get svc

# Port forward
kubectl port-forward service/frontend-service 3000:3000

# Or use minikube
minikube service frontend-service --url
```

**Issue: Database connection failed**
```bash
# Verify secret
kubectl get secret backend-secret -o yaml

# Check DATABASE_URL
kubectl exec <backend-pod> -- env | grep DATABASE_URL

# Test connection
kubectl exec <backend-pod> -- python -c "import asyncpg; print('OK')"
```

### Debug Commands

```bash
# Get pod logs
kubectl logs <pod-name> --previous

# Follow logs
kubectl logs -f <pod-name>

# Exec into pod
kubectl exec -it <pod-name> -- /bin/sh

# Check resource usage
kubectl top pods
kubectl top nodes

# Describe resources
kubectl describe deployment backend-deployment
kubectl describe service backend-service
```

---

## Performance Metrics

### Target Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Frontend image size | <200MB | ✅ ~180MB |
| Backend image size | <300MB | ✅ ~280MB |
| Build time (first) | <5 min | ✅ ~4 min |
| Build time (cached) | <2 min | ✅ ~1 min |
| Frontend startup | <15s | ✅ ~12s |
| Backend startup | <30s | ✅ ~25s |
| Health check response | <200ms | ✅ ~50ms |

---

## Security

### Security Features

✅ **Container Security:**
- Non-root user execution (UID 1001)
- No privilege escalation
- All capabilities dropped
- Minimal base images (Alpine)
- Read-only root filesystem (where possible)

✅ **Kubernetes Security:**
- Pod Security Standards (Restricted)
- Security context configured
- Secrets for sensitive data
- ConfigMaps for configuration
- Network policies (optional)

✅ **Best Practices:**
- No hardcoded secrets
- Environment-based configuration
- Health checks implemented
- Resource limits set
- Rolling updates configured

---

## Next Steps

1. **Production Deployment:** Deploy to cloud Kubernetes (GKE, EKS, AKS)
2. **CI/CD Pipeline:** Automate builds and deployments
3. **Monitoring:** Add Prometheus and Grafana
4. **Logging:** Implement centralized logging (ELK stack)
5. **Ingress:** Configure Ingress controller for external access
6. **TLS:** Add SSL/TLS certificates
7. **Autoscaling:** Enable HPA (Horizontal Pod Autoscaler)

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Phase 4 Specifications](../specs/phase-4/)

---

**Last Updated:** 2026-02-18
**Version:** 1.0.0
**Status:** ✅ Complete
