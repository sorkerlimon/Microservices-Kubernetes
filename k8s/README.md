# Kubernetes Deployment Guide for Kub Project

This guide explains how to deploy the Kub Project microservices application on Kubernetes.

## Prerequisites

- Kubernetes cluster (local like Minikube, Docker Desktop, or cloud-based)
- kubectl CLI tool installed and configured
- Docker installed (for building images)

## Architecture Overview

The Kub Project consists of the following components deployed as Kubernetes resources:

1. **Database (MySQL)**: Persistent storage with StatefulSet
2. **Cache (Redis)**: In-memory cache with Deployment
3. **Message Broker (Kafka)**: Event streaming platform with Deployment
4. **Kafdrop**: Kafka monitoring UI with Deployment
5. **Backend (FastAPI)**: REST API service with Deployment
6. **Frontend (React)**: Web UI with Deployment
7. **Ingress**: For external access to the services

## Deployment Steps

### 1. Create Kubernetes Namespace

```bash
kubectl apply -f namespace.yaml
```

### 2. Apply ConfigMap and Secrets

```bash
kubectl apply -f configmap.yaml
kubectl apply -f secrets.yaml
```

### 3. Create Persistent Volumes and Claims

```bash
kubectl apply -f database-pv.yaml
kubectl apply -f database-pvc.yaml
kubectl apply -f redis-pv.yaml
kubectl apply -f redis-pvc.yaml
kubectl apply -f kafka-pv.yaml
kubectl apply -f kafka-pvc.yaml
```

### 4. Deploy Database

```bash
kubectl apply -f database-deployment.yaml
kubectl apply -f database-service.yaml
```

### 5. Deploy Redis Cache

```bash
kubectl apply -f redis-deployment.yaml
kubectl apply -f redis-service.yaml
```

### 6. Deploy Kafka Broker

```bash
kubectl apply -f kafka-deployment.yaml
kubectl apply -f kafka-service.yaml
```

### 7. Deploy Kafdrop (Kafka UI)

```bash
kubectl apply -f kafdrop-deployment.yaml
kubectl apply -f kafdrop-service.yaml
```

### 8. Deploy Backend Service

```bash
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml
```

### 9. Deploy Frontend Service

```bash
kubectl apply -f frontend-deployment.yaml
kubectl apply -f frontend-service.yaml
```

### 10. Deploy Ingress

```bash
kubectl apply -f ingress.yaml
```

## Automated Deployment

For convenience, you can use the provided script to build and deploy all components:

```bash
chmod +x build-and-deploy.sh
./build-and-deploy.sh
```

## Accessing the Application

After deployment, you can access the application at:

- Frontend: http://kub-project.local
- Backend API: http://kub-project.local/api
- API Documentation: http://kub-project.local/api/docs
- Kafdrop: http://kafdrop.kub-project.local

**Note**: You may need to add the following entries to your `/etc/hosts` file:
```
127.0.0.1 kub-project.local kafdrop.kub-project.local
```

## Verifying Deployment

Check if all pods are running:

```bash
kubectl get pods -n kub-project
```

Check services:

```bash
kubectl get services -n kub-project
```

Check ingress:

```bash
kubectl get ingress -n kub-project
```

## Scaling the Application

You can scale the frontend and backend deployments:

```bash
kubectl scale deployment frontend --replicas=3 -n kub-project
kubectl scale deployment backend --replicas=3 -n kub-project
```

## Cleaning Up

To remove all resources:

```bash
kubectl delete namespace kub-project
```

## Troubleshooting

If pods are not starting, check the logs:

```bash
kubectl logs <pod-name> -n kub-project
```

For persistent volume issues:

```bash
kubectl get pv
kubectl get pvc -n kub-project
```
