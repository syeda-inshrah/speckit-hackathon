#!/bin/bash
# Cleanup Script for Phase 4 Deployment
# This script removes all deployed resources

set -e

echo "🧹 Phase 4 - Cleanup Script"
echo "==========================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Uninstall Helm releases
echo "📦 Uninstalling Helm releases..."

if helm list | grep -q "frontend"; then
    helm uninstall frontend
    print_success "Frontend uninstalled"
else
    print_warning "Frontend not found"
fi

if helm list | grep -q "backend"; then
    helm uninstall backend
    print_success "Backend uninstalled"
else
    print_warning "Backend not found"
fi

echo ""

# Delete any remaining resources
echo "🗑️  Deleting remaining resources..."

kubectl delete deployment --all 2>/dev/null || true
kubectl delete service --all 2>/dev/null || true
kubectl delete configmap --all 2>/dev/null || true
kubectl delete secret --all 2>/dev/null || true

print_success "Resources cleaned up"

echo ""

# Show status
echo "📊 Current Status:"
kubectl get all

echo ""
print_success "Cleanup complete!"
echo ""
echo "To stop Minikube: minikube stop"
echo "To delete Minikube: minikube delete"
