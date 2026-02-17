# Kubernetes Deployment Contract - Frontend

## Overview

**Component:** Frontend Kubernetes Deployment
**Deployment Name:** `frontend-deployment`
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

**Container Name:** `frontend`
**Image:** `todo-frontend:latest`
**Image Pull Policy:** `IfNotPresent`

**Ports:**
- Container Port: 3000
- Protocol: TCP
- Name: http

### Resource Requirements

**Requests:**
```yaml
resources:
  requests:
    cpu: 100m      # 0.1 CPU cores
    memory: 128Mi  # 128 MiB
```

**Limits:**
```yaml
resources:
  limits:
    cpu: 500m      # 0.5 CPU cores
    memory: 512Mi  # 512 MiB
```

**Rationale:**
- Requests ensure guaranteed resources for scheduling
- Limits prevent resource exhaustion
- CPU: 100m request allows 10 pods per core
- Memory: 128Mi request is sufficient for Node.js runtime
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
    port: 3000
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
    path: /health
    port: 3000
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

**ConfigMap Name:** `frontend-config`

**Environment Variables:**
- NEXT_PUBLIC_API_URL
- NODE_ENV

**Injection Method:**
```yaml
envFrom:
  - configMapRef:
      name: frontend-config
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
  readOnlyRootFilesystem: false  # Next.js needs write for cache
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
kubectl rollout undo deployment/frontend-deployment
kubectl rollout undo deployment/frontend-deployment --to-revision=3
```

---

## Service Discovery

### Labels

**Deployment Labels:**
```yaml
labels:
  app: frontend
  version: v1
  component: ui
  tier: frontend
```

**Pod Labels:**
```yaml
labels:
  app: frontend
  version: v1
```

### Selector

**Service Selector:**
```yaml
selector:
  app: frontend
```

**Matching:** Service routes traffic to pods with `app: frontend` label

---

## Networking Contract

### Service Integration

**Service Name:** `frontend-service`
**Service Type:** NodePort (Minikube), LoadBalancer (Production)
**Service Port:** 3000
**Target Port:** 3000
**Node Port:** 30000 (Minikube only)

**DNS Name:** `frontend-service.default.svc.cluster.local`

### External Access

**Minikube:**
```bash
minikube service frontend-service --url
# Output: http://192.168.49.2:30000
```

**Production (LoadBalancer):**
```bash
kubectl get service frontend-service
# EXTERNAL-IP will be assigned by cloud provider
```

---

## Monitoring Contract

### Metrics Endpoints

**Prometheus Metrics:** Not implemented in Phase 4 (Phase 5)

**Annotations:**
```yaml
annotations:
  prometheus.io/scrape: "false"  # Enable in Phase 5
  prometheus.io/port: "3000"
  prometheus.io/path: "/metrics"
```

### Logging

**Log Output:** stdout/stderr
**Log Format:** Text (Next.js default)
**Log Level:** INFO

**Log Collection:** Kubernetes logs API
```bash
kubectl logs deployment/frontend-deployment
kubectl logs -f deployment/frontend-deployment --all-containers
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

#### Scenario: Backend Unavailable

**Detection:** Frontend can't reach backend API
**Action:** Frontend shows error messages to users
**Recovery:** Automatic when backend becomes available

#### Scenario: OOMKilled

**Detection:** Container exceeds memory limit
**Action:** Kubernetes kills container
**Recovery:** Container restarts with clean state

---

## Deployment Operations

### Initial Deployment

```bash
# Apply ConfigMap
kubectl apply -f k8s/frontend/configmap.yaml

# Apply Deployment
kubectl apply -f k8s/frontend/deployment.yaml

# Verify deployment
kubectl rollout status deployment/frontend-deployment

# Check pods
kubectl get pods -l app=frontend
```

### Update Deployment

```bash
# Update image
kubectl set image deployment/frontend-deployment frontend=todo-frontend:v2

# Watch rollout
kubectl rollout status deployment/frontend-deployment

# Verify new version
kubectl get pods -l app=frontend -o jsonpath='{.items[*].spec.containers[*].image}'
```

### Rollback Deployment

```bash
# Rollback to previous version
kubectl rollout undo deployment/frontend-deployment

# Rollback to specific revision
kubectl rollout undo deployment/frontend-deployment --to-revision=3

# Check rollout history
kubectl rollout history deployment/frontend-deployment
```

### Scale Deployment

```bash
# Scale to 3 replicas
kubectl scale deployment/frontend-deployment --replicas=3

# Verify scaling
kubectl get deployment frontend-deployment
```

---

## Testing Contract

### Deployment Verification

```bash
# Check deployment status
kubectl get deployment frontend-deployment

# Expected output:
# NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
# frontend-deployment   2/2     2            2           5m

# Check pod status
kubectl get pods -l app=frontend

# Expected output:
# NAME                                   READY   STATUS    RESTARTS   AGE
# frontend-deployment-abc123-xyz         1/1     Running   0          5m
# frontend-deployment-abc123-uvw         1/1     Running   0          5m
```

### Health Check Verification

```bash
# Test liveness probe
kubectl exec deployment/frontend-deployment -- curl -f http://localhost:3000/health

# Test readiness probe (same endpoint)
kubectl exec deployment/frontend-deployment -- curl -f http://localhost:3000/health

# Check probe status
kubectl describe pod <pod-name> | grep -A 5 "Liveness\|Readiness"
```

### Service Integration Test

```bash
# Test service connectivity
kubectl run test-pod --image=curlimages/curl --rm -it -- \
  curl -f http://frontend-service:3000/health

# Test external access (Minikube)
curl $(minikube service frontend-service --url)/health

# Test in browser
minikube service frontend-service
```

---

## Performance Contract

### Startup Performance

**Target:** < 15 seconds from pod creation to ready
**Measurement:**
```bash
kubectl get pods -l app=frontend -w
```

### Resource Utilization

**CPU Usage:**
- Idle: < 20m (20% of request)
- Normal: 50-100m (50-100% of request)
- Peak: < 500m (limit)

**Memory Usage:**
- Idle: < 64Mi (50% of request)
- Normal: 100-150Mi (75-120% of request)
- Peak: < 512Mi (limit)

**Monitoring:**
```bash
kubectl top pods -l app=frontend
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
- Check backend connectivity
- Verify resource limits

#### Issue: Health checks failing

**Diagnosis:**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl exec <pod-name> -- curl http://localhost:3000/health
```

**Resolution:**
- Check health endpoint implementation
- Verify application startup time
- Increase initialDelaySeconds if needed
- Check for port conflicts

#### Issue: Can't access frontend externally

**Diagnosis:**
```bash
kubectl get service frontend-service
minikube service frontend-service --url
kubectl describe service frontend-service
```

**Resolution:**
- Verify service type (NodePort for Minikube)
- Check nodePort configuration
- Verify pod selector matches
- Check firewall rules

---

## Compliance Contract

### Kubernetes Best Practices

- [x] Resource requests and limits defined
- [x] Liveness and readiness probes configured
- [x] Rolling update strategy configured
- [x] Security context defined
- [x] Non-root user execution
- [x] Labels and selectors properly configured
- [x] ConfigMaps used for configuration
- [x] Graceful shutdown handling

### Security Best Practices

- [x] Runs as non-root user
- [x] No privilege escalation
- [x] Capabilities dropped
- [x] Pod Security Standards compliant

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial frontend deployment configuration
- 2 replicas for high availability
- Health and readiness probes
- Rolling update strategy
- Security context configuration
- Resource limits defined

---

## Approval

**Contract Owner:** Frontend Team
**Reviewed By:** DevOps Team, Platform Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Deployment Manifest](../../k8s/frontend/deployment.yaml)
- [Phase 4 Specification](../spec.md)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
