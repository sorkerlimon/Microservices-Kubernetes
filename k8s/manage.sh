#!/bin/bash
# Kubernetes Management Script for Kub-Project

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
      echo "Usage: $0 [-n|--namespace NAMESPACE] [command]"
      echo ""
      echo "Commands:"
      echo "  status              Show status of all resources"
      echo "  pods                Show all pods"
      echo "  services            Show all services"
      echo "  deployments         Show all deployments"
      echo "  configmaps          Show all configmaps"
      echo "  secrets             Show all secrets"
      echo "  ingress             Show all ingress resources"
      echo "  pvc                 Show all persistent volume claims"
      echo "  logs <pod-name>     Show logs for a specific pod"
      echo "  describe <resource-type> <name>  Describe a specific resource"
      echo "  restart <deployment-name>  Restart a specific deployment"
      echo "  scale <deployment-name> <count>  Scale a deployment to <count> replicas"
      echo "  port-forward <service-name> <local-port>:<service-port>  Forward a local port to a service"
      echo "  delete-all          Delete all resources in the namespace"
      echo "  build-images        Build Docker images"
      echo ""
      echo "Options:"
      echo "  -n, --namespace NAMESPACE   Kubernetes namespace (default: kub-project)"
      exit 0
      ;;
    *)
      COMMAND="$1"
      shift
      break
      ;;
  esac
done

# Check if command is provided
if [ -z "$COMMAND" ]; then
  echo "No command provided. Use -h or --help for usage information."
  exit 1
fi

# Execute command
case $COMMAND in
  status)
    echo "=== Kub-Project Status in namespace $NAMESPACE ==="
    echo ""
    echo "Pods:"
    kubectl get pods -n $NAMESPACE
    echo ""
    echo "Services:"
    kubectl get services -n $NAMESPACE
    echo ""
    echo "Deployments:"
    kubectl get deployments -n $NAMESPACE
    echo ""
    echo "ConfigMaps:"
    kubectl get configmaps -n $NAMESPACE
    echo ""
    echo "Secrets:"
    kubectl get secrets -n $NAMESPACE
    echo ""
    echo "Ingress:"
    kubectl get ingress -n $NAMESPACE
    echo ""
    echo "PVCs:"
    kubectl get pvc -n $NAMESPACE
    ;;
    
  pods)
    kubectl get pods -n $NAMESPACE -o wide
    ;;
    
  services)
    kubectl get services -n $NAMESPACE -o wide
    ;;
    
  deployments)
    kubectl get deployments -n $NAMESPACE -o wide
    ;;
    
  configmaps)
    if [ -n "$1" ]; then
      kubectl get configmap "$1" -n $NAMESPACE -o yaml
    else
      kubectl get configmaps -n $NAMESPACE
    fi
    ;;
    
  secrets)
    if [ -n "$1" ]; then
      kubectl get secret "$1" -n $NAMESPACE -o yaml
    else
      kubectl get secrets -n $NAMESPACE
    fi
    ;;
    
  ingress)
    kubectl get ingress -n $NAMESPACE -o wide
    ;;
    
  pvc)
    kubectl get pvc -n $NAMESPACE -o wide
    ;;
    
  logs)
    if [ -z "$1" ]; then
      echo "Error: Pod name required"
      exit 1
    fi
    
    if [ -n "$2" ] && [ "$2" = "-f" ]; then
      kubectl logs -f "$1" -n $NAMESPACE
    else
      kubectl logs "$1" -n $NAMESPACE
    fi
    ;;
    
  describe)
    if [ -z "$1" ] || [ -z "$2" ]; then
      echo "Error: Resource type and name required"
      echo "Usage: $0 describe <resource-type> <name>"
      exit 1
    fi
    
    kubectl describe "$1" "$2" -n $NAMESPACE
    ;;
    
  restart)
    if [ -z "$1" ]; then
      echo "Error: Deployment name required"
      exit 1
    fi
    
    kubectl rollout restart deployment/"$1" -n $NAMESPACE
    kubectl rollout status deployment/"$1" -n $NAMESPACE
    ;;
    
  scale)
    if [ -z "$1" ] || [ -z "$2" ]; then
      echo "Error: Deployment name and replica count required"
      echo "Usage: $0 scale <deployment-name> <count>"
      exit 1
    fi
    
    kubectl scale deployment/"$1" --replicas="$2" -n $NAMESPACE
    kubectl get deployment "$1" -n $NAMESPACE
    ;;
    
  port-forward)
    if [ -z "$1" ] || [ -z "$2" ]; then
      echo "Error: Service name and port mapping required"
      echo "Usage: $0 port-forward <service-name> <local-port>:<service-port>"
      exit 1
    fi
    
    echo "Starting port forwarding for $1 ($2)..."
    echo "Press Ctrl+C to stop"
    kubectl port-forward svc/"$1" "$2" -n $NAMESPACE
    ;;
    
  delete-all)
    read -p "Are you sure you want to delete all resources in namespace $NAMESPACE? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      kubectl delete all --all -n $NAMESPACE
      echo "All resources deleted from namespace $NAMESPACE"
    else
      echo "Operation cancelled"
    fi
    ;;
    
  build-images)
    echo "Building backend image..."
    docker build -t fastapi-app:latest ../Backend/
    
    echo "Building frontend image..."
    docker build -t react-app:latest ../Frontend/
    
    echo "Images built successfully. Current images:"
    docker images | grep -E 'fastapi-app|react-app'
    ;;
    
  *)
    echo "Unknown command: $COMMAND"
    echo "Use -h or --help for usage information."
    exit 1
    ;;
esac
