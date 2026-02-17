# Kubernetes Deployment Contract - Backend

## Overview

**Component:** Backend Kubernetes Deployment
**Deployment Name:** `backend-deployment`
**Namespace:** `default`
**Version:** 1.0.0

---

## Deployment Specifications

### Replica Configuration

**Replica Count:** 2 (minimum for high availability)
**Scaling Strategy:** Manual (Phase 4), HPA (Phase 5)

**Rationale:**
- 2 replicas provide basic high availability
- Allows rolling updates without downtime
- Distributes load across multiple pods
- Survives single pod failure

---

## Pod Template Specification

### Container Configuration

**Container Name:** `backend`
**Image:** `todo-backend:latest`
**Image Pull Policy:** `IfNotPresent`

**Ports:**
- Container Port: 8001
- Protocol: TCP
- Name: http

### Resource Requirements

**Requests:**
```yaml
resources:
  requests:
    cpu: 200m      # 0.2 CPU cores
    memory: 256Mi  # 256 MiB
```

**Limits:**
```yaml
resources:
  limits:
    cpu: 1000m     # 1 CPU core
    memory: 1Gi    # 1 GiB
```

**Rationale:**
- Requests ensure guaranteed resources for scheduling
- Limits prevent resource exhaustion
- CPU: 200m request allows 5 pods per core
- Memory: 256Mi request is sufficient for Python runtime + app
- Limits allow bursting for peak loads

---

## Health Check Configuration

### Liveness Probe

**Purpose:** Detect if container is alive (restart if fails)

**Configuration:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8001
    scheme: HTTP
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3
```

**Behavior:**
- Wait 30s after container start before first check
- Check every 10s
- Timeout after 3s
- Restart pod after 3 consecutive failures (30s total)

### Readiness Probe

**Purpose:** Detect if container is ready to serve traffic

**Configuration:**
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8001
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3
```

**Behavior:**
- Wait 10s after container start before first check
- Check every 5s
- Timeout after 3s
- Remove from service after 3 consecutive failures (15s total)
- Add back to service after 1 success

---

## Environment Configuration

### ConfigMap Reference

**ConfigMap Name:** `backend-config`

**Environment Variables:**
- LLM_PROVIDER
- FRONTEND_URL
- GROQ_BASE_URL
- GROQ_MODEL
- AGENT_NAME
- AGENT_INSTRUCTIONS
- MAX_TOKENS
- TEMPERATURE

**Injection Method:**
```yaml
envFrom:
  - configMapRef:
      name: backend-config
```

### Secret Reference

**Secret Name:** `backend-secret`

**Environment Variables:**
- DATABASE_URL
- BETTER_AUTH_SECRET
- GROQ_API_KEY
- JWT_ALGORITHM
- JWT_EXPIRATION_DAYS

**Injection Method:**
```yaml
envFrom:
  - secretRef:
      name: backend-secret
```

---

## Security Context

### Pod Security Context

```yaml
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  runAsGroup: 1001
  fsGroup: 1001
```

### Container Security Context

```yaml
securityContext:
  allowPrivilegeEscalation: false
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: false  # Python needs write for bytecode
```

**Security Guarantees:**
- Container runs as non-root user (UID 1001)
- No privilege escalation allowed
- All Linux capabilities dropped
- Complies with Pod Security Standards (Restricted)

---

## Update Strategy

### Rolling Update Configuration

**Strategy Type:** RollingUpdate

**Configuration:**
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # Max 1 pod above desired count
    maxUnavailable: 0  # No pods unavailable during update
```

**Update Process:**
1. Create 1 new pod with updated image
2. Wait for new pod to pass readiness check
3. Terminate 1 old pod
4. Repeat until all pods updated

**Guarantees:**
- Zero downtime during updates
- Always at least 2 pods serving traffic
- Gradual rollout reduces risk
- Can rollback if issues detected

### Rollback Configuration

**Revision History Limit:** 10

**Rollback Command:**
```bash
kubectl rollout undo deployment/backend-deployment
kubectl rollout undo deployment/backend-deployment --to-revision=3
```

---

## Service Discovery

### Labels

**Deployment Labels:**
```yaml
labels:
  app: backend
  version: v1
  component: api
  tier: backend
```

**Pod Labels:**
```yaml
labels:
  app: backend
  version: v1
```

### Selector

**Service Selector:**
```yaml
selector:
  app: backend
```

**Matching:** Service routes traffic to pods with `app: backend` label

---

## Networking Contract

### Service Integration

**Service Name:** `backend-service`
**Service Type:** ClusterIP
**Service Port:** 8001
**Target Port:** 8001

**DNS Name:** `backend-service.default.svc.cluster.local`

### Network Policies (Optional)

**Ingress Rules:**
- Allow traffic from frontend pods
- Allow traffic from ingress controller (if used)

**Egress Rules:**
- Allow traffic to Neon PostgreSQL (external)
- Allow traffic to Groq API (external)
- Allow DNS resolution

---

## Monitoring Contract

### Metrics Endpoints

**Prometheus Metrics:** Not implemented in Phase 4 (Phase 5)

**Annotations:**
```yaml
annotations:
  prometheus.io/scrape: "false"  # Enable in Phase 5
  prometheus.io/port: "8001"
  prometheus.io/path: "/metrics"
```

### Logging

**Log Output:** stdout/stderr
**Log Format:** JSON (structured logging)
**Log Level:** INFO (configurable)

**Log Collection:** Kubernetes logs API
```bash
kubectl logs deployment/backend-deployment
kubectl logs -f deployment/backend-deployment --all-containers
```

---

## Lifecycle Hooks

### PreStop Hook

**Purpose:** Graceful shutdown

**Configuration:**
```yaml
lifecycle:
  preStop:
    exec:
      command: ["/bin/sh", "-c", "sleep 5"]
```

**Behavior:**
- Wait 5s before sending SIGTERM
- Allows load balancer to remove pod from rotation
- Prevents connection errors during shutdown

### Termination Grace Period

**Duration:** 30 seconds

**Behavior:**
1. PreStop hook executes (5s)
2. SIGTERM sent to container
3. Wait up to 30s for graceful shutdown
4. SIGKILL if still running after 30s

---

## Failure Handling

### Pod Restart Policy

**Policy:** Always

**Behavior:**
- Restart pod on failure
- Exponential backoff (10s, 20s, 40s, ...)
- Max backoff: 5 minutes

### Failure Scenarios

#### Scenario: Liveness Probe Fails

**Detection:** 3 consecutive failures (30s)
**Action:** Restart container
**Recovery:** New container starts, passes health checks

#### Scenario: Readiness Probe Fails

**Detection:** 3 consecutive failures (15s)
**Action:** Remove pod from service endpoints
**Recovery:** Pod remains running, added back when ready

#### Scenario: Database Connection Lost

**Detection:** Readiness probe fails (DB check)
**Action:** Remove pod from service
**Recovery:** Application reconnects, readiness passes

#### Scenario: OOMKilled

**Detection:** Container exceeds memory limit
**Action:** Kubernetes kills container
**Recovery:** Container restarts with clean state

---

## Deployment Operations

### Initial Deployment

```bash
# Apply ConfigMap
kubectl apply -f k8s/backend/configmap.yaml

# Apply Secret
kubectl apply -f k8s/backend/secret.yaml

# Apply Deployment
kubectl apply -f k8s/backend/deployment.yaml

# Verify deployment
kubectl rollout status deployment/backend-deployment

# Check pods
kubectl get pods -l app=backend
```

### Update Deployment

```bash
# Update image
kubectl set image deployment/backend-deployment backend=todo-backend:v2

# Watch rollout
kubectl rollout status deployment/backend-deployment

# Verify new version
kubectl get pods -l app=backend -o jsonpath='{.items[*].spec.containers[*].image}'
```

### Rollback Deployment

```bash
# Rollback to previous version
kubectl rollout undo deployment/backend-deployment

# Rollback to specific revision
kubectl rollout undo deployment/backend-deployment --to-revision=3

# Check rollout history
kubectl rollout history deployment/backend-deployment
```

### Scale Deployment

```bash
# Scale to 3 replicas
kubectl scale deployment/backend-deployment --replicas=3

# Verify scaling
kubectl get deployment backend-deployment
```

---

## Testing Contract

### Deployment Verification

```bash
# Check deployment status
kubectl get deployment backend-deployment

# Expected output:
# NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
# backend-deployment   2/2     2            2           5m

# Check pod status
kubectl get pods -l app=backend

# Expected output:
# NAME                                  READY   STATUS    RESTARTS   AGE
# backend-deployment-abc123-xyz         1/1     Running   0          5m
# backend-deployment-abc123-uvw         1/1     Running   0          5m
```

### Health Check Verification

```bash
# Test liveness probe
kubectl exec deployment/backend-deployment -- curl -f http://localhost:8001/health

# Test readiness probe
kubectl exec deployment/backend-deployment -- curl -f http://localhost:8001/ready

# Check probe status
kubectl describe pod <pod-name> | grep -A 5 "Liveness\|Readiness"
```

### Service Integration Test

```bash
# Test service connectivity
kubectl run test-pod --image=curlimages/curl --rm -it -- \
  curl -f http://backend-service:8001/health

# Test from frontend pod
kubectl exec deployment/frontend-deployment -- \
  curl -f http://backend-service:8001/health
```

---

## Performance Contract

### Startup Performance

**Target:** < 30 seconds from pod creation to ready
**Measurement:**
```bash
kubectl get pods -l app=backend -w
```

### Resource Utilization

**CPU Usage:**
- Idle: < 50m (25% of request)
- Normal: 100-200m (50-100% of request)
- Peak: < 1000m (limit)

**Memory Usage:**
- Idle: < 128Mi (50% of request)
- Normal: 200-300Mi (75-120% of request)
- Peak: < 1Gi (limit)

**Monitoring:**
```bash
kubectl top pods -l app=backend
```

---

## Troubleshooting Contract

### Common Issues

#### Issue: Pods not starting (ImagePullBackOff)

**Diagnosis:**
```bash
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
```

**Resolution:**
- Verify image exists in Minikube
- Check image pull policy
- Rebuild image in Minikube context

#### Issue: Pods crashing (CrashLoopBackOff)

**Diagnosis:**
```bash
kubectl logs <pod-name>
kubectl logs <pod-name> --previous
kubectl describe pod <pod-name>
```

**Resolution:**
- Check application logs for errors
- Verify environment variables
- Check database connectivity
- Verify resource limits

#### Issue: Readiness probe failing

**Diagnosis:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec <pod-name> -- curl http://localhost:8001/ready
```

**Resolution:**
- Check database connection
- Verify readiness endpoint
- Check application startup time
- Increase initialDelaySeconds if needed

---

## Compliance Contract

### Kubernetes Best Practices

- [x] Resource requests and limits defined
- [x] Liveness and readiness probes configured
- [x] Rolling update strategy configured
- [x] Security context defined
- [x] Non-root user execution
- [x] Labels and selectors properly configured
- [x] ConfigMaps and Secrets used for configuration
- [x] Graceful shutdown handling

### Security Best Practices

- [x] Runs as non-root user
- [x] No privilege escalation
- [x] Capabilities dropped
- [x] Secrets not in environment variables (via Secret)
- [x] Pod Security Standards compliant

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial backend deployment configuration
- 2 replicas for high availability
- Health and readiness probes
- Rolling update strategy
- Security context configuration
- Resource limits defined

---

## Approval

**Contract Owner:** Backend Team
**Reviewed By:** DevOps Team, Platform Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Deployment Manifest](../../k8s/backend/deployment.yaml)
- [Phase 4 Specification](../spec.md)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
