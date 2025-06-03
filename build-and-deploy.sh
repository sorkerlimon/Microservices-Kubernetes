#!/bin/bash

# Build Docker images
echo "Building Docker images..."
docker build -t kub-database ./Database
docker build -t kub-cache ./Cache
docker build -t kub-kafka ./Broker
docker build -t kub-backend ./Backend
docker build -t kub-frontend ./Frontend

# Create namespace
echo "Creating Kubernetes namespace..."
kubectl apply -f ./k8s/namespace.yaml

# Apply ConfigMap and Secrets
echo "Applying ConfigMap and Secrets..."
kubectl apply -f ./k8s/configmap.yaml
kubectl apply -f ./k8s/mysql-configmap.yaml
kubectl apply -f ./k8s/secrets.yaml

# Create persistent volumes and claims
echo "Creating persistent volumes and claims..."
kubectl apply -f ./k8s/database-pv.yaml
kubectl apply -f ./k8s/database-pvc.yaml
kubectl apply -f ./k8s/redis-pv.yaml
kubectl apply -f ./k8s/redis-pvc.yaml
kubectl apply -f ./k8s/kafka-pv.yaml
kubectl apply -f ./k8s/kafka-pvc.yaml

# Deploy database
echo "Deploying database..."
kubectl apply -f ./k8s/database-deployment.yaml
kubectl apply -f ./k8s/database-service.yaml

# Wait for database to be ready
echo "Waiting for database to be ready..."
kubectl wait --namespace=kub-project --for=condition=ready pod -l app=mysql --timeout=120s

# Deploy Redis cache
echo "Deploying Redis cache..."
kubectl apply -f ./k8s/redis-deployment.yaml
kubectl apply -f ./k8s/redis-service.yaml

# Wait for Redis to be ready
echo "Waiting for Redis to be ready..."
kubectl wait --namespace=kub-project --for=condition=ready pod -l app=redis --timeout=60s

# Deploy Kafka
echo "Deploying Kafka..."
kubectl apply -f ./k8s/kafka-deployment.yaml
kubectl apply -f ./k8s/kafka-service.yaml

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
kubectl wait --namespace=kub-project --for=condition=ready pod -l app=kafka --timeout=120s

# Deploy Kafdrop
echo "Deploying Kafdrop..."
kubectl apply -f ./k8s/kafdrop-deployment.yaml
kubectl apply -f ./k8s/kafdrop-service.yaml

# Deploy backend
echo "Deploying backend..."
kubectl apply -f ./k8s/backend-deployment.yaml
kubectl apply -f ./k8s/backend-service.yaml

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
kubectl wait --namespace=kub-project --for=condition=ready pod -l app=backend --timeout=60s

# Deploy frontend
echo "Deploying frontend..."
kubectl apply -f ./k8s/frontend-deployment.yaml
kubectl apply -f ./k8s/frontend-service.yaml

# Deploy ingress
echo "Deploying ingress..."
kubectl apply -f ./k8s/ingress.yaml

echo "Deployment complete!"
echo "You can access the application at:"
echo "Frontend: http://kub-project.local"
echo "Backend API: http://kub-project.local/api"
echo "Kafdrop: http://kafdrop.kub-project.local"
echo ""
echo "Note: You may need to add the following entries to your /etc/hosts file:"
echo "127.0.0.1 kub-project.local kafdrop.kub-project.local"
