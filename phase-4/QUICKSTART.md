# Phase 4: Local Kubernetes Deployment - Quick Reference

## Quick Start Commands

### Deploy Everything
```bash
# Linux/Mac
cd phase-4
./deploy.sh

# Windows
cd phase-4
deploy.bat
```

### Cleanup Everything
```bash
# Linux/Mac
./cleanup.sh

# Windows
cleanup.bat
```

---

## Manual Deployment

### 1. Start Minikube
```bash
minikube start --cpus=4 --memory=8192 --disk-size=40g
```

### 2. Build Images
```bash
eval $(minikube docker-env)
docker build -t todo-backend:latest -f backend/Dockerfile backend
docker build -t todo-frontend:latest -f frontend/Dockerfile frontend
```

### 3. Deploy with Helm
```bash
# Backend
helm install backend helm/backend \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.betterAuthSecret="..." \
  --set secrets.groqApiKey="..."

# Frontend
helm install frontend helm/frontend
```

### 4. Access Application
```bash
# Get frontend URL
minikube service frontend-todo-frontend --url

# Port-forward backend
kubectl port-forward service/backend-todo-backend 8001:8001
```

---

## Useful Commands

### Monitoring
```bash
# Watch pods
kubectl get pods -w

# View logs
kubectl logs -f <pod-name>

# Describe pod
kubectl describe pod <pod-name>

# Get all resources
kubectl get all
```

### Helm Operations
```bash
# List releases
helm list

# Upgrade release
helm upgrade backend helm/backend

# Rollback release
helm rollback backend

# Get values
helm get values backend
```

### Testing
```bash
# Test health endpoints
curl http://localhost:8001/health
curl http://localhost:8001/ready
curl http://localhost:3000/health

# Test backend API
curl http://localhost:8001/api/info
```

### Cleanup
```bash
# Uninstall releases
helm uninstall backend frontend

# Delete all resources
kubectl delete all --all

# Stop Minikube
minikube stop

# Delete Minikube
minikube delete
```

---

## Environment Variables

### Backend (Required)
```bash
export DATABASE_URL="postgresql://user:pass@host:5432/db"
export BETTER_AUTH_SECRET="your-secret-min-32-chars"
export GROQ_API_KEY="your-groq-api-key"
```

### Frontend (Optional)
```bash
export NEXT_PUBLIC_API_URL="http://backend-service:8001"
```

---

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Image pull errors
```bash
eval $(minikube docker-env)
docker images | grep todo
```

### Service not accessible
```bash
kubectl get svc
minikube service list
```

### Reset everything
```bash
./cleanup.sh
minikube delete
minikube start --cpus=4 --memory=8192
./deploy.sh
```

---

## File Structure

```
phase-4/
├── deploy.sh              # Automated deployment (Linux/Mac)
├── deploy.bat             # Automated deployment (Windows)
├── cleanup.sh             # Cleanup script (Linux/Mac)
├── cleanup.bat            # Cleanup script (Windows)
├── docker-compose.yml     # Local testing
├── backend/               # Backend application
│   ├── Dockerfile         # Backend Docker image
│   └── ...
├── frontend/              # Frontend application
│   ├── Dockerfile         # Frontend Docker image
│   └── ...
├── k8s/                   # Kubernetes manifests
│   ├── backend/           # Backend K8s resources
│   └── frontend/          # Frontend K8s resources
├── helm/                  # Helm charts
│   ├── backend/           # Backend chart
│   └── frontend/          # Frontend chart
└── docs/                  # Documentation
    └── DEPLOYMENT.md      # Comprehensive guide
```

---

## Resources

- **Full Documentation:** [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
- **Implementation Summary:** [IMPLEMENTATION.md](IMPLEMENTATION.md)
- **Phase 4 Overview:** [README.md](README.md)
- **Specifications:** [../specs/phase-4/](../specs/phase-4/)

---

**Quick Start:** Run `./deploy.sh` (Linux/Mac) or `deploy.bat` (Windows)
**Cleanup:** Run `./cleanup.sh` (Linux/Mac) or `cleanup.bat` (Windows)
