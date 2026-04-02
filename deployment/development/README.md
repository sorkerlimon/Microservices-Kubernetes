# Development (Kind)

## Required env vars (used by the backend code)
- `SECRET_KEY` (Argo backend FastAPI reads this from env)

## MySQL (optional)
- To use MySQL, set `MYSQL_HOST` and `MYSQL_PASSWORD` in the Kubernetes `ConfigMap` / `Secret` under this folder.
- If `MYSQL_HOST` is empty, the app uses in-memory storage.

## Important note about MySQL
- MySQL connection values are now read from env vars in `application/backend/database.py`.

## Run (manual)
Run these commands from repo root: `D:\Limon\Kub-Project`



 Build backend image and load into Kind (no Docker Hub)
```bash
docker build -t backend-app:latest application/backend
kind load docker-image backend-app:latest --name helm-dev-cluster1
```

1. Create Kind cluster
```bash
kind delete cluster --name helm-dev-cluster1 2>/dev/null || true
kind create cluster --name helm-dev-cluster1 --config deployment/development/cluster_create.yml
kubectl config use-context kind-helm-dev-cluster1
```

Check cluster
```bash
kind get clusters
kubectl config current-context
kubectl cluster-info --context kind-helm-dev-cluster1
kubectl cluster-info

kubectl get nodes -o wide
```

2. Install ingress-nginx (Helm)
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm upgrade --install ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --create-namespace --set controller.hostPort.enabled=true --set controller.hostPort.ports.http=80 --set controller.hostPort.ports.https=443 --set controller.service.type=ClusterIP
kubectl wait -n ingress-nginx --for=condition=ready pod -l app.kubernetes.io/component=controller --timeout=180s
```

Check ingress-nginx
```bash
helm list -n ingress-nginx
helm status ingress-nginx -n ingress-nginx
kubectl get pods -n ingress-nginx -o wide
kubectl get svc -n ingress-nginx -o wide
kubectl logs -n ingress-nginx -l app.kubernetes.io/component=controller --tail=100
```

3. Build backend image and load into Kind
```bash
docker build -t backend-app:latest application/backend
kind load docker-image backend-app:latest --name helm-dev-cluster1
```

Check image loaded in Kind
```bash
docker images backend-app
docker exec -it helm-dev-cluster1-control-plane crictl images | grep backend-app
```

4. Apply Kubernetes resources (in order)
```bash
kubectl apply -f deployment/development/namespace.yaml
kubectl apply -f deployment/development/configmap-backend.yaml
kubectl apply -f deployment/development/secret-backend.yaml
kubectl apply -f deployment/development/deployment-backend.yaml
kubectl apply -f deployment/development/service-backend.yaml
kubectl apply -f deployment/development/ingress-backend.yaml
```

Check applied resources (step by step)

After `namespace.yaml`
```bash
kubectl get ns dev-project
```

After `configmap-backend.yaml`
```bash
kubectl get configmap -n dev-project
kubectl describe configmap backend-config -n dev-project
```

After `secret-backend.yaml`
```bash
kubectl get secret -n dev-project
kubectl describe secret backend-secret -n dev-project
```

After `deployment-backend.yaml`
```bash
kubectl get deploy -n dev-project
kubectl rollout status deploy/backend -n dev-project
kubectl get pods -n dev-project -o wide
```

After `service-backend.yaml`
```bash
kubectl get svc -n dev-project -o wide
kubectl get endpoints backend-svc -n dev-project
```

After `ingress-backend.yaml`
```bash
kubectl get ingress -n dev-project
kubectl describe ingress backend-ingress -n dev-project
```

## Verify
```bash
kubectl rollout status deployment/backend -n dev-project
kubectl get pods -n dev-project
kubectl get ingress -n dev-project
```

## Ingress URL
- http://localhost:8080/

## 5. Argo CD (GitOps Deployment)

### Install Argo CD
```bash
kubectl apply -f deployment/development/argocd-namespace.yaml
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl wait -n argocd --for=condition=ready pod -l app.kubernetes.io/name=argocd-server --timeout=180s
```

### Check Argo CD
```bash
kubectl get pods -n argocd
kubectl get svc -n argocd
```

### Access Argo CD UI (Port Forward)
```bash
kubectl port-forward svc/argocd-server -n argocd 8081:443
```
Open: https://localhost:8081

### Get Argo CD Admin Password
```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

### Create Argo CD Application
```bash
kubectl apply -f deployment/development/argocd-application.yaml
```

### Check Application Status
```bash
kubectl get application -n argocd
kubectl describe application backend-dev -n argocd
```

### Sync Application (if needed)
```bash
argocd app sync backend-dev
```

## Argo CD Application Details
- **Name:** backend-dev
- **Source:** GitHub repo (auto-sync enabled)
- **Path:** deployment/development
- **Destination:** dev-project namespace
- **Auto-sync:** Enabled with self-heal

# Restart all Argo CD deployments
kubectl rollout restart deployment -n argocd

# Or restart specific components
kubectl rollout restart deployment/argocd-server -n argocd
kubectl rollout restart deployment/argocd-repo-server -n argocd
kubectl rollout restart statefulset/argocd-application-controller -n argocd

# Delete and recreate the application
kubectl delete application backend-dev -n argocd
kubectl apply -f deployment/development/argocd-application.yaml

# Or hard refresh via kubectl patch
kubectl patch application backend-dev -n argocd --type merge -p '{"metadata":{"annotations":{"argocd.argoproj.io/refresh":"hard"}}}'