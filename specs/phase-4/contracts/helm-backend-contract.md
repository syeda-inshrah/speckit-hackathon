# Helm Chart Contract - Backend

## Overview

**Chart Name:** `backend`
**Chart Version:** 1.0.0
**App Version:** 1.0.0
**Description:** Helm chart for Todo App Backend (FastAPI + MCP)
**Maintainer:** Todo App Team

---

## Chart Structure

```
backend/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration values
├── templates/              # Kubernetes manifest templates
│   ├── deployment.yaml     # Deployment template
│   ├── service.yaml        # Service template
│   ├── configmap.yaml      # ConfigMap template
│   ├── secret.yaml         # Secret template
│   ├── _helpers.tpl        # Template helpers
│   └── NOTES.txt           # Post-install notes
├── charts/                 # Dependency charts (none)
└── .helmignore            # Files to ignore
```

---

## Chart Metadata (Chart.yaml)

```yaml
apiVersion: v2
name: backend
description: Todo App Backend - FastAPI with MCP integration
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - backend
  - fastapi
  - mcp
  - ai
home: https://github.com/user/repo
sources:
  - https://github.com/user/repo
maintainers:
  - name: Todo App Team
    email: team@example.com
```

---

## Values Schema

### Required Values

These values MUST be provided at installation time:

```yaml
secrets:
  databaseUrl: ""           # PostgreSQL connection string
  betterAuthSecret: ""      # JWT signing secret (min 32 chars)
  groqApiKey: ""            # Groq API key
```

**Installation Example:**
```bash
helm install backend ./helm/backend \
  --set secrets.databaseUrl="postgresql://..." \
  --set secrets.betterAuthSecret="your-secret-32-chars-long" \
  --set secrets.groqApiKey="your-groq-api-key"
```

### Default Values

Complete default values.yaml structure:

```yaml
# Replica configuration
replicaCount: 2

# Image configuration
image:
  repository: todo-backend
  tag: latest
  pullPolicy: IfNotPresent

# Service configuration
service:
  type: ClusterIP
  port: 8001
  annotations: {}

# Resource limits
resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi

# Health check configuration
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

# Application configuration (non-sensitive)
config:
  llmProvider: "GROQ"
  frontendUrl: "http://frontend-service:3000"
  groqBaseUrl: "https://api.groq.com"
  groqModel: "openai/gpt-oss-20b"
  agentName: "TodoAssistant"
  agentInstructions: "You are a helpful AI assistant for managing todo tasks."
  maxTokens: 2000
  temperature: 0.7

# Secrets (sensitive - must be provided)
secrets:
  databaseUrl: ""
  betterAuthSecret: ""
  groqApiKey: ""
  jwtAlgorithm: "HS256"
  jwtExpirationDays: "7"

# Security context
securityContext:
  runAsNonRoot: true
  runAsUser: 1001
  runAsGroup: 1001
  allowPrivilegeEscalation: false

# Update strategy
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0

# Pod annotations
podAnnotations: {}

# Node selector
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity: {}

# Service account
serviceAccount:
  create: false
  name: ""
```

---

## Template Helpers (_helpers.tpl)

### Required Helper Functions

```yaml
{{/*
Expand the name of the chart.
*/}}
{{- define "backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "backend.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "backend.labels" -}}
helm.sh/chart: {{ include "backend.chart" . }}
{{ include "backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

---

## Installation Contract

### Prerequisites

- Kubernetes 1.24+
- Helm 3.12+
- Backend Docker image available
- Database credentials available
- API keys available

### Installation Steps

**1. Prepare values file:**
```yaml
# values-prod.yaml
secrets:
  databaseUrl: "postgresql://user:pass@host/db?ssl=require"
  betterAuthSecret: "your-secret-32-characters-long"
  groqApiKey: "your-groq-api-key"

config:
  frontendUrl: "http://frontend-service:3000"

replicaCount: 3

resources:
  requests:
    cpu: 300m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi
```

**2. Install chart:**
```bash
helm install backend ./helm/backend -f values-prod.yaml
```

**3. Verify installation:**
```bash
helm status backend
kubectl get pods -l app.kubernetes.io/name=backend
```

### Installation Validation

**Success Criteria:**
- [ ] Chart installs without errors
- [ ] All pods reach Running state
- [ ] Health checks pass
- [ ] Service is created
- [ ] ConfigMap is created
- [ ] Secret is created
- [ ] Deployment is ready

**Validation Commands:**
```bash
# Check release status
helm status backend

# Check all resources
helm get manifest backend | kubectl get -f -

# Test backend health
kubectl run test --image=curlimages/curl --rm -it -- \
  curl http://backend-service:8001/health
```

---

## Upgrade Contract

### Upgrade Process

**1. Update values or image:**
```yaml
# values-prod.yaml
image:
  tag: v1.1.0

replicaCount: 4
```

**2. Perform upgrade:**
```bash
helm upgrade backend ./helm/backend -f values-prod.yaml
```

**3. Monitor rollout:**
```bash
kubectl rollout status deployment/backend-deployment
```

### Upgrade Guarantees

- Zero downtime during upgrade
- Rolling update strategy
- Automatic rollback on failure
- Revision history maintained

### Upgrade Validation

```bash
# Check upgrade status
helm status backend

# Verify new version
helm get values backend

# Check pod versions
kubectl get pods -l app.kubernetes.io/name=backend \
  -o jsonpath='{.items[*].spec.containers[*].image}'
```

---

## Rollback Contract

### Rollback Process

**1. List revisions:**
```bash
helm history backend
```

**2. Rollback to previous:**
```bash
helm rollback backend
```

**3. Rollback to specific revision:**
```bash
helm rollback backend 3
```

### Rollback Guarantees

- Restores previous configuration
- Maintains zero downtime
- Preserves data (stateless app)
- Automatic pod recreation

---

## Uninstall Contract

### Uninstall Process

```bash
# Uninstall release
helm uninstall backend

# Verify cleanup
kubectl get all -l app.kubernetes.io/name=backend
```

### Cleanup Guarantees

**Removed Resources:**
- Deployment
- Service
- ConfigMap
- Secret
- Pods

**Preserved Resources:**
- PersistentVolumeClaims (if any)
- External database data

---

## Customization Contract

### Common Customizations

#### 1. Change Replica Count

```yaml
replicaCount: 5
```

#### 2. Change Resource Limits

```yaml
resources:
  requests:
    cpu: 500m
    memory: 512Mi
  limits:
    cpu: 2000m
    memory: 2Gi
```

#### 3. Change Service Type

```yaml
service:
  type: LoadBalancer
  port: 8001
```

#### 4. Add Pod Annotations

```yaml
podAnnotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8001"
```

#### 5. Configure Node Selector

```yaml
nodeSelector:
  disktype: ssd
  zone: us-west-1a
```

#### 6. Configure Affinity

```yaml
affinity:
  podAntiAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions:
            - key: app.kubernetes.io/name
              operator: In
              values:
                - backend
        topologyKey: kubernetes.io/hostname
```

---

## Testing Contract

### Chart Linting

```bash
# Lint chart
helm lint ./helm/backend

# Expected output:
# ==> Linting ./helm/backend
# [INFO] Chart.yaml: icon is recommended
# 1 chart(s) linted, 0 chart(s) failed
```

### Template Rendering

```bash
# Render templates
helm template backend ./helm/backend -f values-prod.yaml

# Render specific template
helm template backend ./helm/backend -f values-prod.yaml -s templates/deployment.yaml

# Debug rendering
helm template backend ./helm/backend -f values-prod.yaml --debug
```

### Dry Run Installation

```bash
# Dry run install
helm install backend ./helm/backend -f values-prod.yaml --dry-run --debug

# Expected: No errors, valid YAML output
```

### Integration Testing

```bash
# Install to test namespace
helm install backend-test ./helm/backend \
  -f values-test.yaml \
  --namespace test \
  --create-namespace

# Run tests
kubectl run test --image=curlimages/curl --rm -it --namespace test -- \
  curl http://backend-service:8001/health

# Cleanup
helm uninstall backend-test --namespace test
kubectl delete namespace test
```

---

## Security Contract

### Secret Management

**Requirements:**
- Secrets MUST be provided at install time
- Secrets MUST NOT be committed to git
- Secrets MUST be base64 encoded in Kubernetes
- Secrets SHOULD be rotated regularly

**Best Practices:**
```bash
# Use --set for secrets (not in values file)
helm install backend ./helm/backend \
  --set secrets.databaseUrl="..." \
  --set secrets.betterAuthSecret="..." \
  --set secrets.groqApiKey="..."

# Or use separate secrets file (not committed)
helm install backend ./helm/backend -f values.yaml -f secrets.yaml
```

### Security Context

**Enforced:**
- Non-root user execution (UID 1001)
- No privilege escalation
- All capabilities dropped
- Compliant with Pod Security Standards

---

## Monitoring Contract

### Helm Release Monitoring

```bash
# List releases
helm list

# Get release status
helm status backend

# Get release history
helm history backend

# Get release values
helm get values backend

# Get release manifest
helm get manifest backend
```

### Application Monitoring

**Health Checks:**
- Liveness probe: /health
- Readiness probe: /ready

**Metrics (Phase 5):**
- Prometheus metrics endpoint: /metrics
- Grafana dashboards

---

## Documentation Contract

### Required Documentation

- [ ] Chart README.md
- [ ] Values documentation
- [ ] Installation guide
- [ ] Upgrade guide
- [ ] Troubleshooting guide
- [ ] Examples

### NOTES.txt Template

```yaml
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}

Backend service is available at:

  http://{{ include "backend.fullname" . }}:{{ .Values.service.port }}

To test the backend:

  kubectl run test --image=curlimages/curl --rm -it -- \
    curl http://{{ include "backend.fullname" . }}:{{ .Values.service.port }}/health
```

---

## Compliance Contract

### Helm Best Practices

- [x] Chart.yaml complete and valid
- [x] values.yaml documented
- [x] Templates use helpers
- [x] Labels follow conventions
- [x] NOTES.txt provides useful info
- [x] .helmignore excludes unnecessary files
- [x] Chart passes helm lint
- [x] Templates render correctly

### Kubernetes Best Practices

- [x] Resource limits defined
- [x] Health checks configured
- [x] Security context defined
- [x] Rolling updates configured
- [x] Labels and selectors consistent

---

## Change Log

### Version 1.0.0 (2026-02-18)

- Initial backend Helm chart
- Deployment, Service, ConfigMap, Secret templates
- Configurable values
- Helper functions
- Documentation

---

## Approval

**Contract Owner:** Backend Team
**Reviewed By:** DevOps Team, Platform Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Helm Chart](../../helm/backend/)
- [Phase 4 Specification](../spec.md)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Documentation](https://helm.sh/docs/)
