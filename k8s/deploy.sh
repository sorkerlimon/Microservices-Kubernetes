#!/bin/bash
# Comprehensive Deployment Script for Kub-Project

# Print commands and exit on errors
set -e

# Default namespace
NAMESPACE="kub-project"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -n|--namespace)
      NAMESPACE="$2"
      shift
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [-n|--namespace NAMESPACE] [--build-images] [--skip-build] [--debug]"
      echo "  -n, --namespace NAMESPACE   Kubernetes namespace to deploy to (default: kub-project)"
      echo "  --build-images             Build Docker images before deployment"
      echo "  --skip-build               Skip building Docker images"
      echo "  --debug                    Enable debug output"
      exit 0
      ;;
    --build-images)
      BUILD_IMAGES=true
      shift
      ;;
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    --debug)
      set -x
      shift
      ;;
    *)
      echo "Unknown option: $key"
      exit 1
      ;;
  esac
done

echo "========================================================="
echo "Kub-Project Deployment"
echo "========================================================="
echo "Namespace: $NAMESPACE"
echo "Current directory: $(pwd)"
echo "Kubernetes context: $(kubectl config current-context)"
echo "========================================================="

# Create namespace if it doesn't exist
echo "[1/9] Creating namespace $NAMESPACE if it doesn't exist..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Build Docker images if requested
if [ "$BUILD_IMAGES" = true ] && [ "$SKIP_BUILD" != true ]; then
  echo "[2/9] Building Docker images..."
  
  echo "Building backend image..."
  docker build -t fastapi-app:latest ../Backend/
  
  echo "Building frontend image..."
  docker build -t react-app:latest ../Frontend/
  
  echo "Images built successfully. Current images:"
  docker images | grep -E 'fastapi-app|react-app'
else
  echo "[2/9] Skipping Docker image build..."
fi

# Apply ConfigMaps and Secrets
echo "[3/9] Applying ConfigMaps and Secrets..."
kubectl apply -f mysql-configmap.yaml -n $NAMESPACE
kubectl apply -f mysql-secret.yaml -n $NAMESPACE
kubectl apply -f backend-configmap.yaml -n $NAMESPACE
kubectl apply -f backend-secret.yaml -n $NAMESPACE
kubectl apply -f frontend-configmap.yaml -n $NAMESPACE

# Check ConfigMaps and Secrets
echo "\nConfigMaps in namespace $NAMESPACE:"
kubectl get configmaps -n $NAMESPACE

echo "\nSecrets in namespace $NAMESPACE:"
kubectl get secrets -n $NAMESPACE

# Apply storage resources
echo "\n[4/9] Applying storage resources..."
kubectl apply -f mysql-pvc.yaml -n $NAMESPACE

echo "\nPersistent Volume Claims in namespace $NAMESPACE:"
kubectl get pvc -n $NAMESPACE

# Apply deployments
echo "\n[5/9] Applying deployments..."
kubectl apply -f mysql-deployment.yaml -n $NAMESPACE
kubectl apply -f backend-deployment.yaml -n $NAMESPACE
kubectl apply -f frontend-deployment.yaml -n $NAMESPACE

# Apply ingress
echo "\n[6/9] Applying ingress..."
kubectl apply -f ingress.yaml -n $NAMESPACE

# Wait for deployments to be ready
echo "\n[7/9] Waiting for deployments to be ready..."
kubectl rollout status deployment/mysql -n $NAMESPACE
kubectl rollout status deployment/backend -n $NAMESPACE
kubectl rollout status deployment/frontend -n $NAMESPACE

# Display deployment status
echo "\n[8/9] Deployment status:"
echo "\nPods:"
kubectl get pods -n $NAMESPACE

echo "\nServices:"
kubectl get services -n $NAMESPACE

echo "\nDeployments:"
kubectl get deployments -n $NAMESPACE

echo "\nIngress:"
kubectl get ingress -n $NAMESPACE

# Display access information
echo "\n[9/9] Access Information:"
echo "\nBackend API Documentation: http://kub-project.local/api/docs"
echo "Frontend Application: http://kub-project.local/"

MINIKUBE_IP=$(minikube ip 2>/dev/null || echo "<minikube-ip>")
NODEPORT_FRONTEND=$(kubectl get svc frontend-service -n $NAMESPACE -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null || echo "<port>")
NODEPORT_BACKEND=$(kubectl get svc backend-service -n $NAMESPACE -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null || echo "<port>")

echo "\nIf using NodePort (without Ingress):"
echo "Backend API: http://$MINIKUBE_IP:$NODEPORT_BACKEND"
echo "Frontend: http://$MINIKUBE_IP:$NODEPORT_FRONTEND"

echo "\n========================================================="
echo "Deployment Complete!"
echo "========================================================="
echo "\nUseful commands:"
echo "\n# Get all resources in the namespace"
echo "kubectl get all -n $NAMESPACE"

echo "\n# Check logs for a specific pod"
echo "kubectl logs -f <pod-name> -n $NAMESPACE"

echo "\n# Describe a resource for detailed information"
echo "kubectl describe <resource-type>/<resource-name> -n $NAMESPACE"

echo "\n# Port-forward to access a service directly"
echo "kubectl port-forward svc/backend-service 8000:8000 -n $NAMESPACE"
echo "kubectl port-forward svc/frontend-service 3000:3000 -n $NAMESPACE"

echo "\n# Check ConfigMaps and Secrets"
echo "kubectl get configmaps -n $NAMESPACE -o yaml"
echo "kubectl get secrets -n $NAMESPACE -o yaml"

echo "\n# Delete all resources in the namespace"
echo "kubectl delete namespace $NAMESPACE"

echo "\n# Restart a deployment"
echo "kubectl rollout restart deployment/<deployment-name> -n $NAMESPACE"

echo "\n# Scale a deployment"
echo "kubectl scale deployment/<deployment-name> --replicas=<count> -n $NAMESPACE"

