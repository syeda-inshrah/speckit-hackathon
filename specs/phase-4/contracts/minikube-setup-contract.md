# Minikube Environment Contract

## Overview

**Component:** Minikube Local Kubernetes Cluster
**Purpose:** Local development and testing environment for Phase 4
**Version:** 1.32+
**Kubernetes Version:** 1.28+

---

## System Requirements

### Minimum Requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| CPU | 2 cores | 4 cores |
| RAM | 4GB | 8GB |
| Disk Space | 20GB | 40GB |
| OS | Windows 10+, macOS 10.13+, Linux | Latest versions |

### Software Prerequisites

**Required:**
- Docker Desktop 4.0+ (or Docker Engine)
- kubectl 1.24+
- Minikube 1.32+

**Optional:**
- Helm 3.12+
- kubectl-ai
- Kagent

---

## Installation Contract

### Minikube Installation

**macOS:**
```bash
# Using Homebrew
brew install minikube

# Verify installation
minikube version
```

**Windows:**
```bash
# Using Chocolatey
choco install minikube

# Or download installer from:
# https://minikube.sigs.k8s.io/docs/start/

# Verify installation
minikube version
```

**Linux:**
```bash
# Download and install
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version
```

---

## Cluster Configuration

### Cluster Startup

**Basic Startup:**
```bash
minikube start
```

**Recommended Startup (Phase 4):**
```bash
minikube start \
  --cpus=4 \
  --memory=8192 \
  --disk-size=40g \
  --driver=docker \
  --kubernetes-version=v1.28.0
```

**Configuration Explanation:**
- `--cpus=4`: Allocate 4 CPU cores
- `--memory=8192`: Allocate 8GB RAM
- `--disk-size=40g`: Allocate 40GB disk
- `--driver=docker`: Use Docker driver
- `--kubernetes-version=v1.28.0`: Specific K8s version

### Cluster Verification

```bash
# Check cluster status
minikube status

# Expected output:
# minikube
# type: Control Plane
# host: Running
# kubelet: Running
# apiserver: Running
# kubeconfig: Configured

# Check cluster info
kubectl cluster-info

# Check nodes
kubectl get nodes

# Expected output:
# NAME       STATUS   ROLES           AGE   VERSION
# minikube   Ready    control-plane   1m    v1.28.0
```

---

## Driver Configuration

### Docker Driver (Recommended)

**Advantages:**
- Cross-platform support
- Easy to use
- Good performance
- Integrated with Docker Desktop

**Configuration:**
```bash
minikube start --driver=docker
```

**Verification:**
```bash
minikube config get driver
# Output: docker
```

### Alternative Drivers

**VirtualBox:**
```bash
minikube start --driver=virtualbox
```

**Hyper-V (Windows):**
```bash
minikube start --driver=hyperv
```

**KVM2 (Linux):**
```bash
minikube start --driver=kvm2
```

---

## Addon Configuration

### Essential Addons

**Metrics Server (Recommended):**
```bash
# Enable metrics server
minikube addons enable metrics-server

# Verify
kubectl top nodes
kubectl top pods
```

**Dashboard (Optional):**
```bash
# Enable dashboard
minikube addons enable dashboard

# Access dashboard
minikube dashboard
```

**Ingress (Phase 5):**
```bash
# Enable ingress
minikube addons enable ingress

# Verify
kubectl get pods -n ingress-nginx
```

### List Available Addons

```bash
minikube addons list
```

---

## Docker Integration

### Docker Environment

**Point Docker CLI to Minikube:**
```bash
# Set Docker environment
eval $(minikube docker-env)

# Verify
docker ps

# Build images in Minikube
docker build -t todo-frontend:latest -f phase-4/frontend/Dockerfile phase-3/frontend
docker build -t todo-backend:latest -f phase-4/backend/Dockerfile phase-3/backend

# Verify images
docker images | grep todo
```

**Reset Docker Environment:**
```bash
# Reset to host Docker
eval $(minikube docker-env -u)
```

---

## Networking Contract

### Service Access

**NodePort Services:**
```bash
# Get service URL
minikube service <service-name> --url

# Example: Frontend service
minikube service frontend-service --url
# Output: http://192.168.49.2:30000

# Open in browser
minikube service frontend-service
```

**ClusterIP Services:**
```bash
# Port forward to access
kubectl port-forward service/backend-service 8001:8001

# Access at http://localhost:8001
```

**LoadBalancer Services:**
```bash
# Minikube tunnel (requires separate terminal)
minikube tunnel

# Service will get external IP
kubectl get service
```

### DNS Resolution

**Internal DNS:**
- Format: `<service-name>.<namespace>.svc.cluster.local`
- Example: `backend-service.default.svc.cluster.local`
- Short form: `backend-service` (within same namespace)

**Test DNS:**
```bash
kubectl run test-pod --image=busybox --rm -it -- nslookup backend-service
```

---

## Resource Management

### Resource Allocation

**Check Current Resources:**
```bash
# Check node resources
kubectl describe node minikube

# Check resource usage
kubectl top nodes
kubectl top pods --all-namespaces
```

**Adjust Resources:**
```bash
# Stop cluster
minikube stop

# Delete cluster
minikube delete

# Start with new resources
minikube start --cpus=6 --memory=12288
```

### Resource Monitoring

**Monitor Resource Usage:**
```bash
# Real-time monitoring
watch kubectl top nodes
watch kubectl top pods

# Docker stats
docker stats
```

---

## Persistence Contract

### Cluster Persistence

**Stop Cluster (Preserves State):**
```bash
minikube stop
```

**Start Cluster (Restores State):**
```bash
minikube start
```

**Delete Cluster (Removes Everything):**
```bash
minikube delete
```

### Data Persistence

**Note:** Minikube uses ephemeral storage by default

**Persistent Volumes:**
- Supported via hostPath
- Data persists across pod restarts
- Data lost on cluster delete

**External Database:**
- Phase 4 uses external Neon PostgreSQL
- Data persists independently of Minikube

---

## Troubleshooting Contract

### Common Issues

#### Issue: Minikube won't start

**Symptoms:**
```
❌  Exiting due to PROVIDER_DOCKER_NOT_RUNNING
```

**Diagnosis:**
```bash
# Check Docker is running
docker ps

# Check Minikube status
minikube status

# Check logs
minikube logs
```

**Resolution:**
- Start Docker Desktop
- Delete and recreate cluster: `minikube delete && minikube start`
- Check system resources

---

#### Issue: Insufficient resources

**Symptoms:**
```
Pods stuck in Pending state
Node pressure warnings
```

**Diagnosis:**
```bash
# Check node resources
kubectl describe node minikube

# Check pod events
kubectl describe pod <pod-name>

# Check resource usage
kubectl top nodes
kubectl top pods
```

**Resolution:**
```bash
# Increase resources
minikube stop
minikube delete
minikube start --cpus=6 --memory=12288
```

---

#### Issue: Image pull errors

**Symptoms:**
```
ImagePullBackOff
ErrImagePull
```

**Diagnosis:**
```bash
# Check if using Minikube Docker
echo $DOCKER_HOST

# Check images in Minikube
eval $(minikube docker-env)
docker images
```

**Resolution:**
```bash
# Build images in Minikube context
eval $(minikube docker-env)
docker build -t todo-frontend:latest -f phase-4/frontend/Dockerfile phase-3/frontend
docker build -t todo-backend:latest -f phase-4/backend/Dockerfile phase-3/backend

# Set imagePullPolicy to IfNotPresent
kubectl patch deployment <deployment-name> -p '{"spec":{"template":{"spec":{"containers":[{"name":"<container-name>","imagePullPolicy":"IfNotPresent"}]}}}}'
```

---

#### Issue: Service not accessible

**Symptoms:**
```
Connection refused
Timeout errors
```

**Diagnosis:**
```bash
# Check service
kubectl get service <service-name>

# Check endpoints
kubectl get endpoints <service-name>

# Check pods
kubectl get pods -l app=<app-label>

# Test from within cluster
kubectl run test-pod --image=curlimages/curl --rm -it -- curl http://<service-name>:<port>
```

**Resolution:**
```bash
# For NodePort services
minikube service <service-name> --url

# For ClusterIP services
kubectl port-forward service/<service-name> <local-port>:<service-port>

# Check firewall rules
# Verify pod selector matches
```

---

## Performance Optimization

### Startup Performance

**Fast Startup:**
```bash
# Use cached images
minikube start --cache-images

# Skip unnecessary checks
minikube start --wait=false
```

### Build Performance

**Use BuildKit:**
```bash
export DOCKER_BUILDKIT=1
docker build ...
```

**Layer Caching:**
- Use .dockerignore
- Order Dockerfile commands properly
- Cache dependency layers

---

## Maintenance Contract

### Regular Maintenance

**Update Minikube:**
```bash
# macOS
brew upgrade minikube

# Windows
choco upgrade minikube

# Linux
# Download latest version and reinstall
```

**Update Kubernetes:**
```bash
# Stop cluster
minikube stop

# Delete cluster
minikube delete

# Start with new version
minikube start --kubernetes-version=v1.29.0
```

**Clean Up:**
```bash
# Remove unused images
eval $(minikube docker-env)
docker image prune -a

# Remove unused volumes
docker volume prune

# Clean Minikube cache
minikube delete --all --purge
```

---

## Backup and Recovery

### Backup Cluster State

**Export Resources:**
```bash
# Export all resources
kubectl get all --all-namespaces -o yaml > cluster-backup.yaml

# Export specific namespace
kubectl get all -n default -o yaml > default-namespace-backup.yaml
```

### Restore Cluster State

**Apply Backup:**
```bash
# Restore resources
kubectl apply -f cluster-backup.yaml
```

**Note:** External data (Neon DB) is not affected by Minikube state

---

## Security Contract

### Cluster Security

**RBAC:**
- Enabled by default
- Use service accounts for applications
- Follow principle of least privilege

**Network Policies:**
- Supported (requires CNI plugin)
- Optional for Phase 4
- Recommended for Phase 5

**Pod Security:**
- Pod Security Standards supported
- Enforce Restricted policy for production

---

## Testing Contract

### Cluster Health Check

```bash
# Check cluster status
minikube status

# Check node health
kubectl get nodes
kubectl describe node minikube

# Check system pods
kubectl get pods -n kube-system

# Check cluster info
kubectl cluster-info

# Run diagnostics
minikube logs
```

### Application Testing

```bash
# Deploy test application
kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
kubectl expose deployment hello-minikube --type=NodePort --port=8080

# Access application
minikube service hello-minikube --url

# Cleanup
kubectl delete deployment hello-minikube
kubectl delete service hello-minikube
```

---

## Compliance Contract

### Best Practices

- [x] Allocate sufficient resources (4 CPU, 8GB RAM)
- [x] Use Docker driver for consistency
- [x] Enable metrics-server for monitoring
- [x] Build images in Minikube context
- [x] Use imagePullPolicy: IfNotPresent
- [x] Regular maintenance and updates
- [x] Backup important configurations

### Production Readiness

**⚠️ Minikube is NOT for production:**
- Single-node cluster
- No high availability
- Limited scalability
- Development/testing only

**For Production:**
- Use managed Kubernetes (GKE, EKS, AKS)
- Or self-managed multi-node cluster
- Implement proper monitoring and logging
- Configure backup and disaster recovery

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial Minikube environment contract
- Configuration guidelines
- Troubleshooting procedures
- Best practices

---

## Approval

**Contract Owner:** DevOps Team
**Reviewed By:** Platform Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [Minikube Drivers](https://minikube.sigs.k8s.io/docs/drivers/)
- [Minikube Addons](https://minikube.sigs.k8s.io/docs/handbook/addons/)
- [Phase 4 Specification](../spec.md)
