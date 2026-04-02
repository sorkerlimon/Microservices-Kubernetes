# Backend (FastAPI)

## Local

```bash
cd application/backend
python -m venv .venv
```

**Windows**

```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Linux / macOS**

```bash
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open: `http://localhost:8000`

## Docker

```bash
cd application/backend
docker build -t backend-app .
# run without MySQL (in-memory) - only SECRET_KEY is needed
docker run --rm -p 8000:8000 --env SECRET_KEY=dev-change-me backend-app
```

Open: `http://localhost:8000`

## Docker (optional: use env file)

```bash
cd application/backend
docker build -t backend-app .
docker run --rm -p 8000:8000 --env-file .env backend-app
```

## Docker Hub (Build and Push)

```bash
cd application/backend

# Build with your Docker Hub username
docker build -t mdlimon/backend-app:latest .

# Or build with a specific version tag
docker build -t mdlimon/backend-app:v1.0.0 .

# Login to Docker Hub (if not already logged in)
docker login

# Push to Docker Hub
docker push mdlimon/backend-app:latest

# Push specific version tag
docker push mdlimon/backend-app:v1.0.0
```
