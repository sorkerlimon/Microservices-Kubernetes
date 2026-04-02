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
docker run -p 8000:8000 backend-app
```

Open: `http://localhost:8000`
