#!/bin/bash
# Quick Start Script for Phase 4 Deployment
# This script automates the deployment process to Minikube

set -e

echo "🚀 Phase 4 - Todo App Kubernetes Deployment"
echo "============================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed"
    exit 1
fi
print_success "Docker is installed"

if ! command -v minikube &> /dev/null; then
    print_error "Minikube is not installed"
    exit 1
fi
print_success "Minikube is installed"

if ! command -v kubectl &> /dev/null; then
    print_error "kubectl is not installed"
    exit 1
fi
print_success "kubectl is installed"

if ! command -v helm &> /dev/null; then
    print_error "Helm is not installed"
    exit 1
fi
print_success "Helm is installed"

echo ""

# Start Minikube
echo "🔧 Starting Minikube..."
if minikube status | grep -q "Running"; then
    print_success "Minikube is already running"
else
    minikube start --cpus=4 --memory=8192 --disk-size=40g --driver=docker
    print_success "Minikube started"
fi

echo ""

# Point Docker to Minikube
echo "🔗 Configuring Docker to use Minikube's daemon..."
eval $(minikube docker-env)
print_success "Docker configured"

echo ""

# Build images
echo "🏗️  Building Docker images..."

echo "  Building backend image..."
docker build -t todo-backend:latest \
    -f backend/Dockerfile \
    backend
print_success "Backend image built"

echo "  Building frontend image..."
docker build -t todo-frontend:latest \
    -f frontend/Dockerfile \
    frontend
print_success "Frontend image built"

echo ""

# Verify images
echo "📦 Verifying images..."
docker images | grep todo
echo ""

# Deploy with Helm
echo "🚢 Deploying with Helm..."

# Check if secrets are provided
if [ -z "$DATABASE_URL" ] || [ -z "$BETTER_AUTH_SECRET" ] || [ -z "$GROQ_API_KEY" ]; then
    print_warning "Environment variables not set. Using example values."
    print_warning "Set DATABASE_URL, BETTER_AUTH_SECRET, and GROQ_API_KEY for production."

    DATABASE_URL="postgresql://user:password@host:5432/database"
    BETTER_AUTH_SECRET="example-secret-key-min-32-characters-long"
    GROQ_API_KEY="example-groq-api-key"
fi

# Install backend
echo "  Installing backend..."
helm upgrade --install backend helm/backend \
    --set secrets.databaseUrl="$DATABASE_URL" \
    --set secrets.betterAuthSecret="$BETTER_AUTH_SECRET" \
    --set secrets.groqApiKey="$GROQ_API_KEY" \
    --wait
print_success "Backend deployed"

# Install frontend
echo "  Installing frontend..."
helm upgrade --install frontend helm/frontend --wait
print_success "Frontend deployed"

echo ""

# Wait for pods to be ready
echo "⏳ Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-backend --timeout=120s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-frontend --timeout=120s
print_success "All pods are ready"

echo ""

# Show status
echo "📊 Deployment Status:"
echo ""
kubectl get pods
echo ""
kubectl get services
echo ""

# Get frontend URL
echo "🌐 Access Information:"
echo ""
FRONTEND_URL=$(minikube service frontend-todo-frontend --url)
echo "Frontend URL: $FRONTEND_URL"
echo "Backend API: http://localhost:8001 (via port-forward)"
echo ""

print_success "Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "  1. Access frontend: $FRONTEND_URL"
echo "  2. Port-forward backend: kubectl port-forward service/backend-todo-backend 8001:8001"
echo "  3. View logs: kubectl logs -f <pod-name>"
echo "  4. Check health: curl $FRONTEND_URL/health"
echo ""
