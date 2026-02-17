# Helm Chart Contract - Frontend

## Overview

**Chart Name:** `frontend`
**Chart Version:** 1.0.0
**App Version:** 1.0.0
**Description:** Helm chart for Todo App Frontend (Next.js)
**Maintainer:** Todo App Team

---

## Chart Structure

```
frontend/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default configuration values
├── templates/              # Kubernetes manifest templates
│   ├── deployment.yaml     # Deployment template
│   ├── service.yaml        # Service template
│   ├── configmap.yaml      # ConfigMap template
│   ├── _helpers.tpl        # Template helpers
│   └── NOTES.txt           # Post-install notes
├── charts/                 # Dependency charts (none)
└── .helmignore            # Files to ignore
```

---

## Chart Metadata (Chart.yaml)

```yaml
apiVersion: v2
name: frontend
description: Todo App Frontend - Next.js application
type: application
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - frontend
  - nextjs
  - react
home: https://github.com/user/repo
sources:
  - https://github.com/user/repo
maintainers:
  - name: Todo App Team
    email: team@example.com
```

---

## Values Schema

### Default Values

Complete default values.yaml structure:

```yaml
# Replica configuration
replicaCount: 2

# Image configuration
image:
  repository: todo-frontend
  tag: latest
  pullPolicy: IfNotPresent

# Service configuration
service:
  type: NodePort
  port: 3000
  nodePort: 30000
  annotations: {}

# Resource limits
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi

# Health check configuration
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3

# Application configuration
config:
  apiUrl: "http://backend-service:8001"
  nodeEnv: "production"

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
{{- define "frontend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "frontend.fullname" -}}
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
{{- define "frontend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "frontend.labels" -}}
helm.sh/chart: {{ include "frontend.chart" . }}
{{ include "frontend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "frontend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

---

## Installation Contract

### Prerequisites

- Kubernetes 1.24+
- Helm 3.12+
- Frontend Docker image available
- Backend service deployed

### Installation Steps

**1. Prepare values file:**
```yaml
# values-prod.yaml
config:
  apiUrl: "http://backend-service:8001"

service:
  type: LoadBalancer  # For cloud deployment

replicaCount: 3

resources:
  requests:
    cpu: 200m
    memory: 256Mi
  limits:
    cpu: 1000m
    memory: 1Gi
```

**2. Install chart:**
```bash
helm install frontend ./helm/frontend -f values-prod.yaml
```

**3. Verify installation:**
```bash
helm status frontend
kubectl get pods -l app.kubernetes.io/name=frontend
```

### Installation Validation

**Success Criteria:**
- [ ] Chart installs without errors
- [ ] All pods reach Running state
- [ ] Health checks pass
- [ ] Service is created
- [ ] ConfigMap is created
- [ ] Deployment is ready

**Validation Commands:**
```bash
# Check release status
helm status frontend

# Check all resources
helm get manifest frontend | kubectl get -f -

# Test frontend health
kubectl run test --image=curlimages/curl --rm -it -- \
  curl http://frontend-service:3000/health

# Access frontend (Minikube)
minikube service frontend-service --url
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
helm upgrade frontend ./helm/frontend -f values-prod.yaml
```

**3. Monitor rollout:**
```bash
kubectl rollout status deployment/frontend-deployment
```

### Upgrade Guarantees

- Zero downtime during upgrade
- Rolling update strategy
- Automatic rollback on failure
- Revision history maintained

---

## Rollback Contract

### Rollback Process

**1. List revisions:**
```bash
helm history frontend
```

**2. Rollback to previous:**
```bash
helm rollback frontend
```

**3. Rollback to specific revision:**
```bash
helm rollback frontend 3
```

---

## Uninstall Contract

### Uninstall Process

```bash
# Uninstall release
helm uninstall frontend

# Verify cleanup
kubectl get all -l app.kubernetes.io/name=frontend
```

### Cleanup Guarantees

**Removed Resources:**
- Deployment
- Service
- ConfigMap
- Pods

---

## Customization Contract

### Common Customizations

#### 1. Change Service Type (Cloud Deployment)

```yaml
service:
  type: LoadBalancer
  port: 3000
  # nodePort not needed for LoadBalancer
```

#### 2. Change API URL

```yaml
config:
  apiUrl: "https://api.example.com"
```

#### 3. Add Ingress (Phase 5)

```yaml
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: todo.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: todo-tls
      hosts:
        - todo.example.com
```

#### 4. Configure Pod Anti-Affinity

```yaml
affinity:
  podAntiAffinity:
    preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
              - key: app.kubernetes.io/name
                operator: In
                values:
                  - frontend
          topologyKey: kubernetes.io/hostname
```

---

## Testing Contract

### Chart Linting

```bash
# Lint chart
helm lint ./helm/frontend

# Expected output:
# ==> Linting ./helm/frontend
# [INFO] Chart.yaml: icon is recommended
# 1 chart(s) linted, 0 chart(s) failed
```

### Template Rendering

```bash
# Render templates
helm template frontend ./helm/frontend -f values-prod.yaml

# Render specific template
helm template frontend ./helm/frontend -s templates/deployment.yaml

# Debug rendering
helm template frontend ./helm/frontend --debug
```

### Dry Run Installation

```bash
# Dry run install
helm install frontend ./helm/frontend -f values-prod.yaml --dry-run --debug
```

### Integration Testing

```bash
# Install to test namespace
helm install frontend-test ./helm/frontend \
  -f values-test.yaml \
  --namespace test \
  --create-namespace

# Test frontend
kubectl run test --image=curlimages/curl --rm -it --namespace test -- \
  curl http://frontend-service:3000/health

# Cleanup
helm uninstall frontend-test --namespace test
kubectl delete namespace test
```

---

## Security Contract

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
helm status frontend

# Get release history
helm history frontend

# Get release values
helm get values frontend
```

---

## Documentation Contract

### NOTES.txt Template

```yaml
Thank you for installing {{ .Chart.Name }}.

Your release is named {{ .Release.Name }}.

To learn more about the release, try:

  $ helm status {{ .Release.Name }}
  $ helm get all {{ .Release.Name }}

Frontend service is available at:

{{- if eq .Values.service.type "NodePort" }}

  Get the application URL by running:

  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "frontend.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT

{{- else if eq .Values.service.type "LoadBalancer" }}

  Get the application URL by running:

  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "frontend.fullname" . }} --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
  echo http://$SERVICE_IP:{{ .Values.service.port }}

{{- else if eq .Values.service.type "ClusterIP" }}

  Get the application URL by running:

  kubectl --namespace {{ .Release.Namespace }} port-forward svc/{{ include "frontend.fullname" . }} 3000:{{ .Values.service.port }}
  echo http://127.0.0.1:3000

{{- end }}
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

- Initial frontend Helm chart
- Deployment, Service, ConfigMap templates
- Configurable values
- Helper functions
- Documentation

---

## Approval

**Contract Owner:** Frontend Team
**Reviewed By:** DevOps Team, Platform Team
**Approved By:** Technical Lead
**Date:** 2026-02-18
**Status:** Approved

---

## References

- [Helm Chart](../../helm/frontend/)
- [Phase 4 Specification](../spec.md)
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)
- [Helm Documentation](https://helm.sh/docs/)
