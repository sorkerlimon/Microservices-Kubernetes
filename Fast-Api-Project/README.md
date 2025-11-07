# FastAPI Hello ArgoCD App

A simple FastAPI application that displays "Hello Argo CD" in the browser.

## Features

- Simple FastAPI app with HTML response
- Health check endpoint
- Dockerized application
- Ready for Kubernetes/ArgoCD deployment

## Running Locally

### With Python

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then visit `http://localhost:8000` in your browser.

### With Docker

```bash
# Build the image
docker build -t hello-argocd:latest .

# Run the container
docker run -p 8000:8000 hello-argocd:latest
```

Then visit `http://localhost:8000` in your browser.

## Endpoints

- `GET /` - Returns HTML page with "Hello Argo CD" message
- `GET /health` - Health check endpoint

## Docker Build

```bash
docker build -t hello-argocd:latest .
```

## Docker Run

```bash
docker run -p 8000:8000 hello-argocd:latest
```

## For Kubernetes/ArgoCD

This app is ready to be deployed to Kubernetes using ArgoCD. You can create Kubernetes manifests (deployment.yaml, service.yaml) and configure ArgoCD to sync from your Git repository.

