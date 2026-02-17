# Phase 4: Local Kubernetes Deployment - Data Models & Schemas

## Overview

**Phase:** IV - Local Kubernetes Deployment
**Status:** Planning
**Date:** 2026-02-18
**Purpose:** Document data models, configuration schemas, and resource specifications for Phase 4

---

## Table of Contents

1. [Application Data Models](#application-data-models)
2. [Configuration Schemas](#configuration-schemas)
3. [Kubernetes Resource Schemas](#kubernetes-resource-schemas)
4. [Helm Values Schemas](#helm-values-schemas)
5. [Environment Variable Schemas](#environment-variable-schemas)
6. [Health Check Schemas](#health-check-schemas)

---

## Application Data Models

### Overview

Phase 4 uses the same data models as Phase 3 (no changes to database schema). This section documents how these models are accessed in the containerized environment.

### Database Models (From Phase 3)

#### User Model
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
    conversations: list["Conversation"] = Relationship(back_populates="user")
```

#### Task Model
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    user: "User" = Relationship(back_populates="tasks")
```

#### Conversation Model
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: Optional[str] = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="conversations")
    messages: list["Message"] = Relationship(back_populates="conversation")
```

#### Message Model
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    conversation: "Conversation" = Relationship(back_populates="messages")
```

### Database Connection in Containers

**Connection String Format:**
```
postgresql://<user>:<password>@<host>:<port>/<database>?ssl=require
```

**Environment Variable:**
```bash
DATABASE_URL=postgresql://neondb_owner:password@ep-host.neon.tech/neondb?ssl=require
```

**Container Considerations:**
- Connection string provided via Kubernetes Secret
- SSL/TLS required for Neon connection
- Connection pooling handled by SQLModel/asyncpg
- No changes to connection logic from Phase 3

---

## Configuration Schemas

### Frontend Configuration Schema

#### Environment Variables
```typescript
interface FrontendConfig {
  // API Configuration
  NEXT_PUBLIC_API_URL: string;           // Backend API URL

  // Build Configuration
  NODE_ENV: 'development' | 'production'; // Environment mode

  // Optional Configuration
  NEXT_PUBLIC_ENABLE_ANALYTICS?: boolean; // Analytics flag
  NEXT_PUBLIC_LOG_LEVEL?: string;        // Logging level
}
```

#### Example Configuration
```bash
# Development (docker-compose)
NEXT_PUBLIC_API_URL=http://localhost:8001

# Kubernetes (Minikube)
NEXT_PUBLIC_API_URL=http://backend-service:8001

# Production (Phase 5)
NEXT_PUBLIC_API_URL=https://api.example.com
```

#### Validation Rules
- `NEXT_PUBLIC_API_URL`: Required, must be valid HTTP/HTTPS URL
- `NODE_ENV`: Required, must be 'development' or 'production'

---

### Backend Configuration Schema

#### Environment Variables
```python
class Settings(BaseSettings):
    # Database
    DATABASE_URL: str                    # PostgreSQL connection string

    # Authentication
    BETTER_AUTH_SECRET: str              # JWT signing secret
    JWT_ALGORITHM: str = "HS256"         # JWT algorithm
    JWT_EXPIRATION_DAYS: int = 7         # JWT expiration

    # CORS
    FRONTEND_URL: str                    # Frontend URL for CORS

    # LLM Provider
    LLM_PROVIDER: str = "GROQ"           # OPENROUTER or GROQ

    # Groq Configuration
    GROQ_API_KEY: str                    # Groq API key
    GROQ_BASE_URL: str                   # Groq API base URL
    GROQ_MODEL: str                      # Groq model name

    # OpenRouter Configuration (optional)
    OPENROUTER_API_KEY: str = ""         # OpenRouter API key
    OPENROUTER_BASE_URL: str = ""        # OpenRouter base URL
    OPENROUTER_MODEL: str = ""           # OpenRouter model

    # Agent Configuration
    AGENT_NAME: str = "TodoAssistant"    # Agent name
    AGENT_INSTRUCTIONS: str              # Agent instructions
    MAX_TOKENS: int = 2000               # Max tokens
    TEMPERATURE: float = 0.7             # Temperature
```

#### Configuration Sources
1. **Kubernetes ConfigMap** (non-sensitive):
   - LLM_PROVIDER
   - FRONTEND_URL
   - GROQ_BASE_URL
   - GROQ_MODEL
   - AGENT_NAME
   - AGENT_INSTRUCTIONS
   - MAX_TOKENS
   - TEMPERATURE

2. **Kubernetes Secret** (sensitive):
   - DATABASE_URL
   - BETTER_AUTH_SECRET
   - GROQ_API_KEY
   - JWT_ALGORITHM
   - JWT_EXPIRATION_DAYS

#### Validation Rules
- `DATABASE_URL`: Required, must be valid PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Required, minimum 32 characters
- `GROQ_API_KEY`: Required if LLM_PROVIDER=GROQ
- `FRONTEND_URL`: Required, must be valid HTTP/HTTPS URL

---

## Kubernetes Resource Schemas

### Deployment Schema

#### Frontend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  labels:
    app: frontend
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: frontend
        version: v1
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
          name: http
          protocol: TCP
        env:
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: frontend-config
              key: NEXT_PUBLIC_API_URL
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
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
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          runAsGroup: 1001
          allowPrivilegeEscalation: false
```

#### Backend Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend-deployment
  labels:
    app: backend
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: backend
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: backend
        version: v1
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8001
          name: http
          protocol: TCP
        envFrom:
        - configMapRef:
            name: backend-config
        - secretRef:
            name: backend-secret
        resources:
          requests:
            cpu: 200m
            memory: 256Mi
          limits:
            cpu: 1000m
            memory: 1Gi
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
        securityContext:
          runAsNonRoot: true
          runAsUser: 1001
          runAsGroup: 1001
          allowPrivilegeEscalation: false
```

### Service Schema

#### Frontend Service (NodePort)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  labels:
    app: frontend
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30000
    protocol: TCP
    name: http
```

#### Backend Service (ClusterIP)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  labels:
    app: backend
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - port: 8001
    targetPort: 8001
    protocol: TCP
    name: http
```

### ConfigMap Schema

#### Frontend ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-config
  labels:
    app: frontend
data:
  NEXT_PUBLIC_API_URL: "http://backend-service:8001"
```

#### Backend ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: backend-config
  labels:
    app: backend
data:
  LLM_PROVIDER: "GROQ"
  FRONTEND_URL: "http://frontend-service:3000"
  GROQ_BASE_URL: "https://api.groq.com"
  GROQ_MODEL: "openai/gpt-oss-20b"
  AGENT_NAME: "TodoAssistant"
  AGENT_INSTRUCTIONS: "You are a helpful AI assistant for managing todo tasks."
  MAX_TOKENS: "2000"
  TEMPERATURE: "0.7"
```

### Secret Schema

#### Backend Secret
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: backend-secret
  labels:
    app: backend
type: Opaque
data:
  DATABASE_URL: <base64-encoded-value>
  BETTER_AUTH_SECRET: <base64-encoded-value>
  GROQ_API_KEY: <base64-encoded-value>
  JWT_ALGORITHM: <base64-encoded-value>
  JWT_EXPIRATION_DAYS: <base64-encoded-value>
```

---

## Helm Values Schemas

### Frontend Helm Values

```yaml
# Default values for frontend chart

# Replica count
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

# Pod annotations
podAnnotations: {}

# Node selector
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity: {}
```

### Backend Helm Values

```yaml
# Default values for backend chart

# Replica count
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

# Application configuration
config:
  llmProvider: "GROQ"
  frontendUrl: "http://frontend-service:3000"
  groqBaseUrl: "https://api.groq.com"
  groqModel: "openai/gpt-oss-20b"
  agentName: "TodoAssistant"
  agentInstructions: "You are a helpful AI assistant for managing todo tasks."
  maxTokens: 2000
  temperature: 0.7

# Secrets (must be provided at install time)
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

# Pod annotations
podAnnotations: {}

# Node selector
nodeSelector: {}

# Tolerations
tolerations: []

# Affinity
affinity: {}
```

---

## Environment Variable Schemas

### Frontend Environment Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| NEXT_PUBLIC_API_URL | string | Yes | - | Backend API URL |
| NODE_ENV | string | Yes | production | Environment mode |
| NEXT_PUBLIC_ENABLE_ANALYTICS | boolean | No | false | Enable analytics |
| NEXT_PUBLIC_LOG_LEVEL | string | No | info | Logging level |

### Backend Environment Variables

| Variable | Type | Required | Default | Source | Description |
|----------|------|----------|---------|--------|-------------|
| DATABASE_URL | string | Yes | - | Secret | PostgreSQL connection string |
| BETTER_AUTH_SECRET | string | Yes | - | Secret | JWT signing secret |
| JWT_ALGORITHM | string | Yes | HS256 | Secret | JWT algorithm |
| JWT_EXPIRATION_DAYS | integer | Yes | 7 | Secret | JWT expiration days |
| FRONTEND_URL | string | Yes | - | ConfigMap | Frontend URL for CORS |
| LLM_PROVIDER | string | Yes | GROQ | ConfigMap | LLM provider selection |
| GROQ_API_KEY | string | Yes* | - | Secret | Groq API key (*if GROQ) |
| GROQ_BASE_URL | string | Yes* | - | ConfigMap | Groq API base URL |
| GROQ_MODEL | string | Yes* | - | ConfigMap | Groq model name |
| AGENT_NAME | string | No | TodoAssistant | ConfigMap | Agent name |
| AGENT_INSTRUCTIONS | string | No | - | ConfigMap | Agent instructions |
| MAX_TOKENS | integer | No | 2000 | ConfigMap | Max tokens |
| TEMPERATURE | float | No | 0.7 | ConfigMap | Temperature |

---

## Health Check Schemas

### Frontend Health Check

#### Endpoint: GET /health

**Response Schema:**
```typescript
interface HealthResponse {
  status: 'healthy' | 'unhealthy';
  timestamp?: string;
}
```

**Success Response (200 OK):**
```json
{
  "status": "healthy"
}
```

**Failure Response (503 Service Unavailable):**
```json
{
  "status": "unhealthy"
}
```

**Kubernetes Configuration:**
```yaml
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
```

---

### Backend Health Checks

#### Endpoint: GET /health

**Response Schema:**
```python
class HealthResponse(BaseModel):
    status: Literal["healthy", "unhealthy"]
    timestamp: Optional[str] = None
```

**Success Response (200 OK):**
```json
{
  "status": "healthy"
}
```

**Kubernetes Configuration:**
```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8001
  initialDelaySeconds: 30
  periodSeconds: 10
  timeoutSeconds: 3
  failureThreshold: 3
```

---

#### Endpoint: GET /ready

**Response Schema:**
```python
class ReadinessResponse(BaseModel):
    status: Literal["ready", "not_ready"]
    database: Literal["connected", "disconnected"]
    timestamp: Optional[str] = None
```

**Success Response (200 OK):**
```json
{
  "status": "ready",
  "database": "connected"
}
```

**Failure Response (503 Service Unavailable):**
```json
{
  "status": "not_ready",
  "database": "disconnected"
}
```

**Kubernetes Configuration:**
```yaml
readinessProbe:
  httpGet:
    path: /ready
    port: 8001
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  failureThreshold: 3
```

---

## Docker Image Metadata

### Frontend Image

**Image Name:** `todo-frontend:latest`

**Labels:**
```dockerfile
LABEL maintainer="team@example.com"
LABEL version="1.0.0"
LABEL description="Todo App Frontend - Next.js"
LABEL org.opencontainers.image.source="https://github.com/user/repo"
```

**Exposed Ports:**
- 3000 (HTTP)

**User:** nextjs (UID: 1001)

**Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

---

### Backend Image

**Image Name:** `todo-backend:latest`

**Labels:**
```dockerfile
LABEL maintainer="team@example.com"
LABEL version="1.0.0"
LABEL description="Todo App Backend - FastAPI"
LABEL org.opencontainers.image.source="https://github.com/user/repo"
```

**Exposed Ports:**
- 8001 (HTTP)

**User:** appuser (UID: 1001)

**Health Check:**
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8001/health')"
```

---

## Resource Limits Schema

### Frontend Resource Limits

```yaml
resources:
  requests:
    cpu: "100m"      # 0.1 CPU cores
    memory: "128Mi"  # 128 MiB
  limits:
    cpu: "500m"      # 0.5 CPU cores
    memory: "512Mi"  # 512 MiB
```

**Rationale:**
- Lightweight Next.js application
- Mostly serving static content
- Minimal CPU requirements
- Moderate memory for Node.js runtime

---

### Backend Resource Limits

```yaml
resources:
  requests:
    cpu: "200m"      # 0.2 CPU cores
    memory: "256Mi"  # 256 MiB
  limits:
    cpu: "1000m"     # 1 CPU core
    memory: "1Gi"    # 1 GiB
```

**Rationale:**
- Python runtime overhead
- MCP tool execution
- LLM API calls
- Database connections
- Higher CPU for processing

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-18 | Claude Sonnet 4.5 | Initial data model documentation |
