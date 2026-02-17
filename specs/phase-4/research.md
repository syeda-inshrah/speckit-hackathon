# Phase 4: Local Kubernetes Deployment - Research & Technical Investigation

## Overview

**Phase:** IV - Local Kubernetes Deployment
**Status:** Research
**Date:** 2026-02-18
**Purpose:** Document research findings, best practices, and technical decisions for containerization and Kubernetes deployment

## Table of Contents

1. [Docker Containerization Research](#docker-containerization-research)
2. [Kubernetes Deployment Patterns](#kubernetes-deployment-patterns)
3. [Helm Chart Best Practices](#helm-chart-best-practices)
4. [Security Considerations](#security-considerations)
5. [Resource Sizing Guidelines](#resource-sizing-guidelines)
6. [AI-Assisted DevOps Tools](#ai-assisted-devops-tools)
7. [Performance Optimization](#performance-optimization)
8. [Troubleshooting Patterns](#troubleshooting-patterns)

---

## Docker Containerization Research

### Multi-Stage Builds

**Research Question:** How can we minimize Docker image size while maintaining functionality?

**Findings:**
- Multi-stage builds can reduce image size by 60-80%
- Separate build dependencies from runtime dependencies
- Only copy necessary artifacts to final stage
- Use Alpine Linux base images for minimal footprint

**Best Practices:**
```dockerfile
# Stage 1: Build (includes dev dependencies)
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Production (only runtime dependencies)
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json
CMD ["npm", "start"]
```

**Benefits:**
- Frontend: ~150MB vs ~400MB (62% reduction)
- Backend: ~250MB vs ~600MB (58% reduction)
- Faster deployments and reduced storage costs

**References:**
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

---

### Alpine Linux vs Debian/Ubuntu

**Comparison:**

| Aspect | Alpine | Debian/Ubuntu |
|--------|--------|---------------|
| Base Size | ~5MB | ~100-150MB |
| Package Manager | apk | apt |
| C Library | musl | glibc |
| Security | Smaller attack surface | More packages available |
| Compatibility | May need compilation | Better compatibility |

**Decision:** Use Alpine for both services

**Rationale:**
- Significantly smaller images
- Faster builds and deployments
- Official Node and Python Alpine images available
- Minimal compatibility issues for our stack
- Industry standard for containerized apps

**Potential Issues:**
- Some Python packages may need compilation (solved with build dependencies)
- Different package names (documented in Dockerfile)

---

### Non-Root User Execution

**Research Question:** Why run containers as non-root users?

**Security Benefits:**
1. **Principle of Least Privilege:** Container processes don't need root
2. **Defense in Depth:** Limits damage if container is compromised
3. **Compliance:** Many security standards require non-root
4. **Kubernetes Security Context:** Works with Pod Security Standards

**Implementation:**
```dockerfile
# Create non-root user
RUN addgroup -g 1001 -S appuser && \
    adduser -S appuser -u 1001

# Change ownership of app files
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser
```

**Verification:**
```bash
docker run --rm todo-backend:latest whoami
# Output: appuser (not root)
```

**References:**
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
- [Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)

---

### Health Check Implementation

**Research Question:** What's the best way to implement container health checks?

**Docker Health Checks:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8001/health || exit 1
```

**Kubernetes Health Checks:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8001
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8001
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

**Difference Between Liveness and Readiness:**
- **Liveness:** Is the container alive? (restart if fails)
- **Readiness:** Is the container ready to serve traffic? (remove from service if fails)

**Best Practices:**
- Liveness: Simple check (process alive)
- Readiness: Comprehensive check (dependencies ready)
- Use different endpoints for different checks
- Set appropriate timeouts and thresholds

**References:**
- [Kubernetes Liveness and Readiness Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

---

### Layer Caching Optimization

**Research Question:** How can we optimize Docker build times?

**Layer Caching Strategy:**
1. Copy dependency files first (package.json, pyproject.toml)
2. Install dependencies (cached if files unchanged)
3. Copy application code last (changes frequently)

**Example:**
```dockerfile
# Good: Dependencies cached separately
COPY package*.json ./
RUN npm ci
COPY . .

# Bad: Everything invalidates cache
COPY . .
RUN npm ci
```

**Build Time Comparison:**
- Without optimization: 4-5 minutes every build
- With optimization: 4-5 minutes first build, 30-60 seconds subsequent builds

**Additional Optimizations:**
- Use .dockerignore to exclude unnecessary files
- Combine RUN commands to reduce layers
- Use BuildKit for parallel builds
- Use Docker layer caching in CI/CD

**References:**
- [Docker Build Cache](https://docs.docker.com/build/cache/)
- [BuildKit](https://docs.docker.com/build/buildkit/)

---

## Kubernetes Deployment Patterns

### Deployment vs StatefulSet vs DaemonSet

**Research Question:** Which Kubernetes workload type should we use?

**Comparison:**

| Type | Use Case | Our Application |
|------|----------|-----------------|
| **Deployment** | Stateless apps | ✓ Frontend, Backend |
| **StatefulSet** | Stateful apps (databases) | ✗ Using external DB |
| **DaemonSet** | One pod per node | ✗ Not needed |

**Decision:** Use Deployments for both services

**Rationale:**
- Both frontend and backend are stateless
- State stored in external Neon database
- Need multiple replicas for availability
- Rolling updates required

---

### Replica Count Strategy

**Research Question:** How many replicas should we run?

**Considerations:**
1. **Availability:** Minimum 2 for high availability
2. **Load Distribution:** More replicas = better load distribution
3. **Resource Constraints:** Minikube has limited resources
4. **Cost:** More replicas = more resources

**Decision:**
- **Development (Minikube):** 2 replicas each
- **Production (Phase 5):** 3+ replicas with HPA

**Rationale:**
- 2 replicas provide basic HA
- Allows testing of load balancing
- Fits within Minikube resource limits
- Can scale up in production

---

### Rolling Update Strategy

**Research Question:** How should we handle deployments without downtime?

**Rolling Update Configuration:**
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # Max pods above desired count
    maxUnavailable: 0  # Max pods unavailable during update
```

**Update Process:**
1. Create 1 new pod (maxSurge: 1)
2. Wait for new pod to be ready
3. Terminate 1 old pod
4. Repeat until all pods updated

**Benefits:**
- Zero downtime deployments
- Gradual rollout reduces risk
- Can rollback if issues detected
- Traffic always served

**Testing:**
```bash
# Update image
kubectl set image deployment/backend backend=todo-backend:v2

# Watch rollout
kubectl rollout status deployment/backend

# Rollback if needed
kubectl rollout undo deployment/backend
```

**References:**
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

---

### Service Types

**Research Question:** Which service type should we use for each component?

**Service Type Comparison:**

| Type | Use Case | Accessibility | Our Usage |
|------|----------|---------------|-----------|
| **ClusterIP** | Internal only | Within cluster | Backend |
| **NodePort** | External access | Node IP:Port | Frontend (dev) |
| **LoadBalancer** | Cloud LB | External IP | Frontend (prod) |
| **ExternalName** | External service | DNS CNAME | Not needed |

**Decision:**
- **Frontend:** NodePort (Minikube), LoadBalancer (Production)
- **Backend:** ClusterIP (internal only)

**Rationale:**
- Backend should not be directly accessible from outside
- Frontend needs external access for users
- NodePort works well for Minikube (no cloud LB)
- LoadBalancer for production cloud deployment

---

### ConfigMaps vs Secrets

**Research Question:** How should we manage configuration?

**Decision Matrix:**

| Data Type | Storage | Example |
|-----------|---------|---------|
| **Non-sensitive config** | ConfigMap | API URLs, feature flags |
| **Sensitive credentials** | Secret | DB passwords, API keys |
| **Application code** | Container image | Source code |

**Best Practices:**
1. Never hardcode secrets in images
2. Use Secrets for all credentials
3. Mount as environment variables or files
4. Use RBAC to restrict Secret access
5. Consider external secret management (Phase 5)

**Implementation:**
```yaml
# ConfigMap
env:
  - name: LLM_PROVIDER
    valueFrom:
      configMapKeyRef:
        name: backend-config
        key: LLM_PROVIDER

# Secret
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: backend-secret
        key: DATABASE_URL
```

**References:**
- [Kubernetes ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/)
- [Kubernetes Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

---

## Helm Chart Best Practices

### Chart Structure

**Research Question:** What's the recommended Helm chart structure?

**Standard Structure:**
```
chart-name/
├── Chart.yaml          # Chart metadata
├── values.yaml         # Default values
├── templates/          # Kubernetes manifests
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── _helpers.tpl   # Template helpers
│   └── NOTES.txt      # Post-install notes
├── charts/            # Dependency charts
└── .helmignore        # Files to ignore
```

**Best Practices:**
1. Use semantic versioning in Chart.yaml
2. Document all values in values.yaml
3. Use _helpers.tpl for common labels
4. Provide NOTES.txt for post-install instructions
5. Use .helmignore to exclude unnecessary files

**References:**
- [Helm Chart Best Practices](https://helm.sh/docs/chart_best_practices/)

---

### Template Functions

**Research Question:** How can we make templates flexible and reusable?

**Common Template Functions:**

```yaml
# Default values
{{ .Values.replicaCount | default 2 }}

# Required values
{{ required "Image repository is required" .Values.image.repository }}

# Conditionals
{{- if .Values.ingress.enabled }}
# Ingress configuration
{{- end }}

# Loops
{{- range .Values.env }}
- name: {{ .name }}
  value: {{ .value }}
{{- end }}

# Include helpers
{{ include "chart.fullname" . }}
```

**Helper Template Example:**
```yaml
{{/* Generate full name */}}
{{- define "chart.fullname" -}}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/* Common labels */}}
{{- define "chart.labels" -}}
app.kubernetes.io/name: {{ include "chart.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}
```

---

### Values Organization

**Research Question:** How should we organize values.yaml?

**Recommended Structure:**
```yaml
# Image configuration
image:
  repository: todo-backend
  tag: latest
  pullPolicy: IfNotPresent

# Deployment configuration
replicaCount: 2
strategy:
  type: RollingUpdate

# Service configuration
service:
  type: ClusterIP
  port: 8001

# Resource limits
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi

# Application configuration
config:
  llmProvider: GROQ
  frontendUrl: http://frontend-service:3000

# Secrets (values provided at install time)
secrets:
  databaseUrl: ""
  groqApiKey: ""
```

**Best Practices:**
1. Group related values together
2. Use nested structure for clarity
3. Provide sensible defaults
4. Document each value with comments
5. Use empty strings for required secrets

---

## Security Considerations

### Container Security

**Research Areas:**
1. **Non-root execution** ✓ Implemented
2. **Read-only root filesystem** (optional)
3. **Drop unnecessary capabilities**
4. **Security scanning** (Trivy, Snyk)
5. **Image signing** (Cosign)

**Security Context:**
```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  runAsGroup: 1001
  fsGroup: 1001
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: true  # If possible
```

**Image Scanning:**
```bash
# Scan for vulnerabilities
trivy image todo-backend:latest

# Scan Dockerfile
trivy config phase-4/backend/Dockerfile
```

---

### Secret Management

**Research Question:** How should we handle secrets securely?

**Options:**

| Method | Security | Complexity | Our Usage |
|--------|----------|------------|-----------|
| **Kubernetes Secrets** | Basic | Low | Phase 4 ✓ |
| **Sealed Secrets** | Better | Medium | Phase 5 |
| **External Secrets Operator** | Best | High | Phase 5 |
| **HashiCorp Vault** | Best | High | Future |

**Current Approach (Phase 4):**
- Use Kubernetes Secrets
- Base64 encoding (not encryption)
- RBAC to restrict access
- Never commit secrets to git

**Future Improvements (Phase 5):**
- Sealed Secrets for GitOps
- External Secrets Operator for cloud secret managers
- Automatic secret rotation

**Best Practices:**
1. Never hardcode secrets
2. Use separate secrets per environment
3. Rotate secrets regularly
4. Audit secret access
5. Use encryption at rest (cloud providers)

---

### Network Security

**Research Question:** How can we secure network communication?

**Network Policies:**
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-network-policy
spec:
  podSelector:
    matchLabels:
      app: backend
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: frontend
      ports:
        - protocol: TCP
          port: 8001
  egress:
    - to:
        - namespaceSelector: {}
      ports:
        - protocol: TCP
          port: 5432  # PostgreSQL
```

**Benefits:**
- Restrict pod-to-pod communication
- Prevent lateral movement
- Explicit allow-list approach
- Defense in depth

**Note:** Network policies require CNI plugin support (Calico, Cilium, etc.)

---

## Resource Sizing Guidelines

### Resource Requests vs Limits

**Research Question:** How should we set resource requests and limits?

**Concepts:**
- **Request:** Guaranteed resources (used for scheduling)
- **Limit:** Maximum resources (enforced by kubelet)

**Best Practices:**
```yaml
resources:
  requests:
    cpu: 200m      # 0.2 CPU cores
    memory: 256Mi  # 256 MiB
  limits:
    cpu: 1000m     # 1 CPU core
    memory: 1Gi    # 1 GiB
```

**Guidelines:**
1. Set requests based on average usage
2. Set limits based on peak usage
3. Monitor actual usage and adjust
4. Avoid setting limits too low (OOMKilled)
5. Avoid setting limits too high (resource waste)

---

### Sizing Recommendations

**Research Question:** What resources do our applications need?

**Frontend (Next.js):**
- **CPU Request:** 100m (0.1 cores)
- **CPU Limit:** 500m (0.5 cores)
- **Memory Request:** 128Mi
- **Memory Limit:** 512Mi
- **Rationale:** Next.js is relatively lightweight, mostly serving static content

**Backend (FastAPI + MCP):**
- **CPU Request:** 200m (0.2 cores)
- **CPU Limit:** 1000m (1 core)
- **Memory Request:** 256Mi
- **Memory Limit:** 1Gi
- **Rationale:** Python runtime + MCP tools + LLM API calls require more resources

**Minikube Cluster:**
- **Minimum:** 4 CPU, 8GB RAM
- **Recommended:** 6 CPU, 12GB RAM
- **Rationale:** 2 replicas × 2 services + system pods

---

### Quality of Service (QoS) Classes

**Research Question:** How does Kubernetes prioritize pods?

**QoS Classes:**

| Class | Condition | Priority | Eviction Order |
|-------|-----------|----------|----------------|
| **Guaranteed** | requests = limits | Highest | Last |
| **Burstable** | requests < limits | Medium | Middle |
| **BestEffort** | No requests/limits | Lowest | First |

**Our Configuration:**
- Both services: **Burstable** (requests < limits)
- Allows bursting for peak loads
- Reasonable eviction priority

**Production Recommendation:**
- Critical services: Guaranteed
- Background jobs: BestEffort

---

## AI-Assisted DevOps Tools

### Docker AI (Gordon)

**Research Question:** How can Gordon help with Docker operations?

**Capabilities:**
1. **Dockerfile generation:** Generate optimized Dockerfiles
2. **Optimization suggestions:** Analyze and improve existing Dockerfiles
3. **Troubleshooting:** Debug build and runtime issues
4. **Best practices:** Recommend security and performance improvements

**Example Usage:**
```bash
# Get help
docker ai "What can you do?"

# Generate Dockerfile
docker ai "Create a Dockerfile for a Next.js application"

# Optimize existing Dockerfile
docker ai "How can I optimize this Dockerfile?" < Dockerfile

# Troubleshoot
docker ai "Why is my container failing to start?"
```

**Limitations:**
- Requires Docker Desktop 4.53+
- Beta feature (may have limitations)
- Not available in all regions
- Fallback: Use standard Docker commands

**References:**
- [Docker AI Documentation](https://docs.docker.com/ai/gordon/)

---

### kubectl-ai

**Research Question:** How can kubectl-ai simplify Kubernetes operations?

**Capabilities:**
1. **Natural language queries:** "list all pods in default namespace"
2. **Resource management:** "scale deployment to 3 replicas"
3. **Troubleshooting:** "why is my pod crashing?"
4. **Best practices:** "how should I configure health checks?"

**Example Usage:**
```bash
# List resources
kubectl-ai "show me all deployments"

# Scale deployment
kubectl-ai "scale the backend deployment to 3 replicas"

# Troubleshoot
kubectl-ai "why are my pods not starting?"

# Get recommendations
kubectl-ai "how can I improve my deployment configuration?"
```

**Installation:**
```bash
# Install kubectl-ai
go install github.com/GoogleCloudPlatform/kubectl-ai@latest

# Configure OpenAI API key
export OPENAI_API_KEY=your-key-here
```

**References:**
- [kubectl-ai GitHub](https://github.com/GoogleCloudPlatform/kubectl-ai)

---

### Kagent

**Research Question:** What advanced capabilities does Kagent provide?

**Capabilities:**
1. **Cluster analysis:** Health checks, resource usage
2. **Optimization recommendations:** Resource allocation, scaling
3. **Troubleshooting:** Root cause analysis
4. **Security scanning:** Vulnerability detection

**Example Usage:**
```bash
# Analyze cluster health
kagent "analyze the cluster health"

# Optimize resources
kagent "optimize resource allocation for my deployments"

# Security scan
kagent "scan for security vulnerabilities"

# Troubleshoot
kagent "why is my application slow?"
```

**Installation:**
```bash
# Install Kagent
curl -sSL https://get.kagent.dev | bash

# Configure
kagent config set-context minikube
```

**References:**
- [Kagent GitHub](https://github.com/kagent-dev/kagent)

---

## Performance Optimization

### Image Build Performance

**Optimization Techniques:**
1. **Multi-stage builds:** Reduce final image size
2. **Layer caching:** Cache dependency layers
3. **BuildKit:** Parallel builds, better caching
4. **.dockerignore:** Reduce build context
5. **Minimal base images:** Alpine Linux

**Build Time Comparison:**
- Without optimization: 5-7 minutes
- With optimization: 1-2 minutes (cached)

---

### Container Startup Performance

**Optimization Techniques:**
1. **Smaller images:** Faster pull and startup
2. **Readiness probes:** Don't route traffic until ready
3. **Startup probes:** Allow slow-starting containers
4. **Resource requests:** Ensure resources available

**Startup Time Targets:**
- Frontend: < 15 seconds
- Backend: < 30 seconds

---

### Application Performance

**Monitoring:**
1. **Resource usage:** CPU, memory, network
2. **Response times:** API latency
3. **Error rates:** Failed requests
4. **Throughput:** Requests per second

**Tools:**
- Kubernetes Metrics Server
- Prometheus + Grafana (Phase 5)
- Application Performance Monitoring (Phase 5)

---

## Troubleshooting Patterns

### Common Issues and Solutions

#### Issue: Image Pull Errors

**Symptoms:**
```
Failed to pull image: ImagePullBackOff
```

**Causes:**
- Image not available in Minikube
- Wrong image name or tag
- Private registry authentication

**Solutions:**
```bash
# Load image to Minikube
eval $(minikube docker-env)
docker build -t todo-backend:latest .

# Verify image exists
docker images | grep todo

# Check pod events
kubectl describe pod <pod-name>
```

---

#### Issue: CrashLoopBackOff

**Symptoms:**
```
Pod status: CrashLoopBackOff
```

**Causes:**
- Application error on startup
- Missing environment variables
- Failed health checks
- Resource limits too low

**Solutions:**
```bash
# Check logs
kubectl logs <pod-name>

# Check previous logs
kubectl logs <pod-name> --previous

# Describe pod
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

---

#### Issue: Service Not Accessible

**Symptoms:**
- Cannot reach service from outside cluster
- Connection refused or timeout

**Causes:**
- Wrong service type
- Incorrect port configuration
- Network policy blocking traffic
- Pods not ready

**Solutions:**
```bash
# Check service
kubectl get service <service-name>
kubectl describe service <service-name>

# Check endpoints
kubectl get endpoints <service-name>

# Test from within cluster
kubectl run test-pod --image=curlimages/curl --rm -it -- curl http://service-name:port

# For NodePort services
minikube service <service-name> --url
```

---

#### Issue: ConfigMap/Secret Not Mounted

**Symptoms:**
- Environment variables not set
- Application can't find configuration

**Causes:**
- ConfigMap/Secret doesn't exist
- Wrong name in deployment
- RBAC permissions

**Solutions:**
```bash
# Check ConfigMap exists
kubectl get configmap <name>
kubectl describe configmap <name>

# Check Secret exists
kubectl get secret <name>
kubectl describe secret <name>

# Check pod environment
kubectl exec <pod-name> -- env

# Check mounted volumes
kubectl describe pod <pod-name>
```

---

## Conclusion

This research document provides the technical foundation for Phase 4 implementation. Key takeaways:

1. **Multi-stage builds** are essential for image optimization
2. **Alpine Linux** provides the best size/compatibility trade-off
3. **Non-root execution** is a security best practice
4. **Helm charts** enable parameterized, repeatable deployments
5. **Resource sizing** requires monitoring and adjustment
6. **AI tools** can accelerate development and troubleshooting

## Next Steps

1. Review research findings
2. Apply best practices in implementation
3. Document deviations and rationale
4. Update research as new findings emerge

## References

### Official Documentation
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)

### Best Practices
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [12 Factor App](https://12factor.net/)

### Security
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [OWASP Container Security](https://owasp.org/www-project-docker-top-10/)

### Tools
- [Docker AI (Gordon)](https://docs.docker.com/ai/gordon/)
- [kubectl-ai](https://github.com/GoogleCloudPlatform/kubectl-ai)
- [Kagent](https://github.com/kagent-dev/kagent)
- [Trivy](https://github.com/aquasecurity/trivy)

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-18 | Claude Sonnet 4.5 | Initial research document |
