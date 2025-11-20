
kind create cluster --name weather-cluster1
kubectl config use-context kind-weather-cluster1

# Apply namespace
kubectl apply -f Deploy/1_namespace.yaml
# Set default namespace for current context
kubectl config set-context --current --namespace=weather-project
# Apply deployment
kubectl apply -f Deploy/2_weather_deployment.yaml

kubectl logs -f deployment/weather-app -n weather-project


# Check status
kubectl get all -n weather-project

# Port forward to access the app
kubectl port-forward deployment/weather-app 5000:5000 -n weather-project

# --- Argo CD Local Deployment ---

# Create argocd namespace
kubectl create namespace argocd
#kubectl config set-context --current --namespace=argocd

kubectl get namespaces

kubectl get pods -n argocd

kubectl get deployments -n argocd

kubectl get statefulsets -n argocd

kubectl get services -n argocd


# Alternative: Install Argo CD (using remote URL)
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Install Argo CD (using local YAML file) - MUST BE DONE FIRST to install CRDs
kubectl apply -n argocd -f Deploy/3_argocd_application.yaml


# Wait for Argo CD components to be ready
kubectl get pods -n argocd

# Check if all pods are running (should show all pods as Running)
kubectl get pods -n argocd

# Check detailed pod status
kubectl get pods -n argocd -o wide

# Optionally watch until all pods are ready
kubectl get pods -n argocd -w

# Check Argo CD services
kubectl get svc -n argocd

# Check Argo CD deployments
kubectl get deployments -n argocd

# Check Argo CD statefulsets
kubectl get statefulsets -n argocd

# Verify Argo CD CRDs are installed
kubectl get crd | grep argoproj.io

# Expose Argo CD API server via port-forward (access UI at https://localhost:8080)
kubectl port-forward svc/argocd-server -n argocd 8080:443

# Retrieve initial admin password powershell command
powershell -Command "$pwd = kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath='{.data.password}'; [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($pwd))"

# Login to Argo CD CLI (optional, requires argocd CLI installed)
argocd login localhost:8080 --username admin --password <password> --insecure

# Apply Argo CD Application (AFTER Argo CD is installed and running)
kubectl apply -f Deploy/3_argocd_application.yaml

# Check Argo CD Application status
kubectl get applications -n argocd

# Get detailed Application status
kubectl get application weather-app -n argocd -o yaml

# Check Application sync status
kubectl describe application weather-app -n argocd

# Check Argo CD Application Controller logs (shows sync operations)
kubectl logs -f statefulset/argocd-application-controller -n argocd

# Check Argo CD Repo Server logs (shows Git operations)
kubectl logs -f deployment/argocd-repo-server -n argocd

# Check Argo CD Server logs (shows API/UI operations)
kubectl logs -f deployment/argocd-server -n argocd

# Check if FastAPI app pods are created
kubectl get pods -n weather-project

# Check FastAPI app logs
kubectl logs -f deployment/weather-app -n weather-project

# Watch Application status in real-time
kubectl get applications -n argocd -w

# --- Redeploy/Resync Argo CD Application ---

# Method 1: Force sync (if automated sync is enabled, it should sync automatically)
# If you updated Git repo, Argo CD will auto-sync (if automated sync is enabled)

# Method 2: Manual sync via kubectl (patch to trigger sync)
kubectl patch application weather-app -n argocd --type merge -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"argocd"}}}'

# Method 3: Delete and recreate Application (forces full resync)
# kubectl delete application weather-app -n argocd
# kubectl apply -f Deploy/3_argocd_application.yaml

# Method 4: Restart Argo CD Application Controller (forces resync of all apps)
# kubectl rollout restart statefulset/argocd-application-controller -n argocd

# Method 5: Using Argo CD CLI (if installed)
# argocd app sync weather-app
# argocd app sync weather-app --force

# Check sync status after redeploy
kubectl get application weather-app -n argocd
kubectl describe application weather-app -n argocd

# Check if pods are being recreated
kubectl get pods -n weather-project -w

# Or create Argo CD Application via CLI (if you have Git repo)
# argocd app create weather-app \
#   --repo https://github.com/your-username/your-repo.git \
#   --path kubernetes \
#   --dest-server https://kubernetes.default.svc \
#   --dest-namespace weather-project \
#   --sync-policy automated \
#   --auto-prune \
#   --self-heal





# local deployment command 
docker build -t mdlimon/weather-app:latest ./weather
docker push mdlimon/weather-app:latest

kubectl rollout restart deployment/weather-app -n weather-project
kubectl rollout status deployment/weather-app -n weather-project

# Build, tag with git SHA, push, and update deployment (recommended for automatic updates)
# WINDOWS POWERSHELL EXAMPLE:
# $sha = git rev-parse --short HEAD
# docker build -t mdlimon/fastapi-app:sha-$sha ./Fast-Api-Project
# docker push mdlimon/fastapi-app:sha-$sha
# kubectl set image deployment/weather-app weather=mdlimon/weather-app:sha-$sha -n weather-project
# kubectl rollout status deployment/fastapi-app -n fastapi-project

# BASH EXAMPLE:
# SHA=$(git rev-parse --short HEAD)
# docker build -t mdlimon/fastapi-app:sha-$SHA ./Fast-Api-Project
# docker push mdlimon/fastapi-app:sha-$SHA
# kubectl set image deployment/fastapi-app fastapi=mdlimon/fastapi-app:sha-$SHA -n fastapi-project
# kubectl rollout status deployment/fastapi-app -n fastapi-project