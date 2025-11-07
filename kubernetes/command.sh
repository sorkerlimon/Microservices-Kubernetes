# Apply namespace
kubectl apply -f kubernetes/1_namespace.yaml
# Set default namespace for current context
kubectl config set-context --current --namespace=fastapi-project
# Apply deployment
kubectl apply -f kubernetes/2_fast_api_deployment.yaml

kubectl logs -f deployment/fastapi-app -n fastapi-project


# Check status
kubectl get all -n fastapi-project

# Port forward to access the app
kubectl port-forward deployment/fastapi-app 8000:8000 -n fastapi-project