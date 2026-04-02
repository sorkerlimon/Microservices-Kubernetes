# First run and downlaod kind and move to c drive and and create environment variable for kind
kind create cluster --name helm-cluster1
kind get clusters
kubectl get nodes
kind delete cluster --name helm-cluster1
kind create cluster --name helm-cluster1 --config cluster_create.yml
kubectl cluster-info --context kind-helm-cluster1
kubectl config get-contexts
kubectl config use-context kind-helm-cluster1

# Delete contexts
kubectl config delete-context kind-helm-cluster1

# Delete clusters
kubectl config delete-cluster kind-weather-cluster1

# Delete users
kubectl config unset users.kind-weather-cluster1



kubectl config use-context kind-weather-cluster2
# ## Namespace Management
# ```bash
# # Create a namespace
# kubectl create namespace kub-project

# # Set default namespace for current context
# kubectl config set-context --current --namespace=kub-project

# # List all namespaces
# kubectl get namespaces
# ```

# ## Building and Managing Docker Images
# ```bash
# # Build Docker images
# docker build -t fastapi-app:latest ../Backend/
# docker build -t react-app:latest ../Frontend/

# # List images
# docker images | grep -E 'fastapi-app|react-app'

# # Tag images for a registry
# docker tag fastapi-app:latest username/fastapi-app:latest
# docker tag react-app:latest username/react-app:latest

# # Push images to registry
# docker push username/fastapi-app:latest
# docker push username/react-app:latest
# ```

# ## Deployment Management
# ```bash
# # Apply all resources in a directory
# kubectl apply -f . -n kub-project

# # Apply specific resources
# kubectl apply -f backend-deployment.yaml -n kub-project
# kubectl apply -f frontend-deployment.yaml -n kub-project
# kubectl apply -f mysql-deployment.yaml -n kub-project

# # Check deployment status
# kubectl rollout status deployment/backend -n kub-project
# kubectl rollout status deployment/frontend -n kub-project
# kubectl rollout status deployment/mysql -n kub-project

# # Restart a deployment
# kubectl rollout restart deployment/backend -n kub-project

# # Scale a deployment
# kubectl scale deployment/backend --replicas=3 -n kub-project
# ```

# ## Pod Management
# ```bash
# # List all pods
# kubectl get pods -n kub-project

# # Get detailed pod information
# kubectl get pods -o wide -n kub-project

# # Watch pods (real-time updates)
# kubectl get pods -n kub-project -w

# # Get pod details
# kubectl describe pod <pod-name> -n kub-project

# # Get pod logs
# kubectl logs <pod-name> -n kub-project

# # Get logs continuously
# kubectl logs -f <pod-name> -n kub-project

# # Get logs from a specific container in a pod
# kubectl logs <pod-name> -c <container-name> -n kub-project

# # Execute command in a pod
# kubectl exec -it <pod-name> -n kub-project -- /bin/bash

# # Delete a pod
# kubectl delete pod <pod-name> -n kub-project
# ```

# ## Service Management
# ```bash
# # List all services
# kubectl get services -n kub-project

# # Get detailed service information
# kubectl get services -o wide -n kub-project

# # Describe a service
# kubectl describe service <service-name> -n kub-project

# # Port forward to a service
# kubectl port-forward svc/<service-name> <local-port>:<service-port> -n kub-project
# # Examples:
# kubectl port-forward svc/backend-service 8000:8000 -n kub-project
# kubectl port-forward svc/frontend-service 3000:3000 -n kub-project
# kubectl port-forward svc/mysql-service 3306:3306 -n kub-project
# ```

# ## ConfigMap and Secret Management
# ```bash
# # List all ConfigMaps
# kubectl get configmaps -n kub-project

# # View ConfigMap details
# kubectl describe configmap <configmap-name> -n kub-project

# # Get ConfigMap YAML
# kubectl get configmap <configmap-name> -o yaml -n kub-project

# # List all Secrets
# kubectl get secrets -n kub-project

# # View Secret details (metadata only)
# kubectl describe secret <secret-name> -n kub-project

# # Get Secret YAML (values will be base64 encoded)
# kubectl get secret <secret-name> -o yaml -n kub-project

# # Decode a Secret value
# kubectl get secret <secret-name> -o jsonpath="{.data.<key>}" -n kub-project | base64 --decode
# ```

# ## Ingress Management
# ```bash
# # List all ingresses
# kubectl get ingress -n kub-project

# # Get detailed ingress information
# kubectl describe ingress <ingress-name> -n kub-project

# # Get ingress YAML
# kubectl get ingress <ingress-name> -o yaml -n kub-project
# ```

# ## Storage Management
# ```bash
# # List all PersistentVolumeClaims
# kubectl get pvc -n kub-project

# # Get PVC details
# kubectl describe pvc <pvc-name> -n kub-project

# # List all PersistentVolumes
# kubectl get pv
# ```

# ## Resource Monitoring
# ```bash
# # Get resource usage for nodes
# kubectl top nodes

# # Get resource usage for pods
# kubectl top pods -n kub-project

# # Get resource usage for a specific pod
# kubectl top pod <pod-name> -n kub-project
# ```

# ## Troubleshooting
# ```bash
# # Check events (sorted by time)
# kubectl get events --sort-by=.metadata.creationTimestamp -n kub-project

# # Check pod status with reason
# kubectl get pods -n kub-project -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,REASON:.status.reason

# # Check container status within a pod
# kubectl get pod <pod-name> -n kub-project -o jsonpath='{.status.containerStatuses[*].state}'

# # Check readiness and liveness probe status
# kubectl describe pod <pod-name> -n kub-project | grep -A 10 "Liveness\|Readiness"
# ```

# ## Cleanup
# ```bash
# # Delete all resources in a namespace
# kubectl delete all --all -n kub-project

# # Delete specific resources
# kubectl delete deployment <deployment-name> -n kub-project
# kubectl delete service <service-name> -n kub-project
# kubectl delete configmap <configmap-name> -n kub-project
# kubectl delete secret <secret-name> -n kub-project

# # Delete a namespace and all its resources
# kubectl delete namespace kub-project
# ```

# ## Using the Provided Scripts
# ```bash
# # Make scripts executable
# chmod +x deploy.sh manage.sh

# # Deploy with custom namespace
# ./deploy.sh -n custom-namespace

# # Build images and deploy
# ./deploy.sh --build-images

# # Check status with management script
# ./manage.sh -n kub-project status

# # Get logs for a specific pod
# ./manage.sh -n kub-project logs <pod-name>

# # Restart a deployment
# ./manage.sh -n kub-project restart backend
# ```

# ## Complete Application Deployment
# ```bash
# # 1. Create namespace
# kubectl create namespace kub-project

# # 2. Build Docker images
# docker build -t fastapi-app:latest ../Backend/
# docker build -t react-app:latest ../Frontend/

# # 3. Apply ConfigMaps and Secrets
# kubectl apply -f mysql-configmap.yaml -n kub-project
# kubectl apply -f mysql-secret.yaml -n kub-project
# kubectl apply -f backend-configmap.yaml -n kub-project
# kubectl apply -f backend-secret.yaml -n kub-project
# kubectl apply -f frontend-configmap.yaml -n kub-project

# # 4. Apply storage resources
# kubectl apply -f mysql-pvc.yaml -n kub-project

# # 5. Apply deployments
# kubectl apply -f mysql-deployment.yaml -n kub-project
# kubectl apply -f backend-deployment.yaml -n kub-project
# kubectl apply -f frontend-deployment.yaml -n kub-project

# # 6. Apply ingress
# kubectl apply -f ingress.yaml -n kub-project

# # 7. Check deployment status
# kubectl get all -n kub-project
# ```



# --- Helm: Run / Install ---

# Add Argo Helm repo and update
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update

# Create argocd namespace and install Argo CD
kubectl create namespace argocd
helm install argocd argo/argo-cd -n argocd

# Optional: install argocd-apps (Application definitions; use with values for apps)
# helm install my-argocd-apps argo/argocd-apps --version 2.0.4 -n default

# List all Helm releases (all namespaces)
helm list -A

# List releases in argocd namespace
helm list -n argocd

# Check release status and get manifest/values
helm status argocd -n argocd
helm get manifest argocd -n argocd
helm get values argocd -n argocd

# Argo CD UI: get admin password, then port-forward
# kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
# kubectl port-forward svc/argocd-server -n argocd 8080:443

# --- Helm: Delete / Uninstall ---

# Uninstall Helm releases (order: apps first, then Argo CD)
helm uninstall my-argocd-apps -n default
helm uninstall argocd -n argocd

# Optional: remove argocd namespace after uninstall
# kubectl delete namespace argocd

# Verify no Helm releases left
helm list -A