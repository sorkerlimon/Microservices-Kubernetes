"""
Simple Login/Register API - Welcome Kubernetes
Backend: FastAPI. Database: MySQL (or in-memory if MYSQL_HOST not set).
"""
from fastapi import FastAPI, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pathlib import Path
import os

from database import (
    use_mysql,
    init_db,
    get_user_by_email,
    create_user as db_create_user,
    user_exists as db_user_exists,
)

# In-memory store when MYSQL_HOST is not set
users_db: dict[str, dict] = {}
password_hasher = PasswordHasher()
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Welcome Kubernetes App")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    if use_mysql():
        init_db()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class WelcomeResponse(BaseModel):
    message: str


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        password_hasher.verify(hashed, plain)
        return True
    except VerifyMismatchError:
        return False


def create_token(email: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_email_from_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def _user_exists(email: str) -> bool:
    if use_mysql():
        return get_user_by_email(email) is not None
    return email in users_db


def get_current_user(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.replace("Bearer ", "")
    email = get_email_from_token(token)
    if not email or not _user_exists(email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email


@app.post("/api/register", response_model=TokenResponse)
def register(data: RegisterRequest):
    if use_mysql():
        if db_user_exists(data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
    else:
        if data.email in users_db:
            raise HTTPException(status_code=400, detail="Email already registered")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    hashed = hash_password(data.password)
    if use_mysql():
        db_create_user(data.email, hashed)
    else:
        users_db[data.email] = {"password": hashed}
    token = create_token(data.email)
    return TokenResponse(access_token=token)


def _get_user_password(email: str) -> str | None:
    if use_mysql():
        row = get_user_by_email(email)
        return row["password"] if row else None
    if email not in users_db:
        return None
    return users_db[email]["password"]


@app.post("/api/login", response_model=TokenResponse)
def login(data: LoginRequest):
    stored = _get_user_password(data.email)
    if not stored or not verify_password(data.password, stored):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_token(data.email)
    return TokenResponse(access_token=token)


@app.get("/api/welcome", response_model=WelcomeResponse)
def welcome(authorization: str | None = Header(None)):
    get_current_user(authorization)
    return WelcomeResponse(message="Welcome Kubernetes")


# Serve frontend
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    def index():
        return FileResponse(static_dir / "index.html")
else:
    @app.get("/")
    def index():
        return {"info": "Frontend not built. Mount static files at /static and serve index.html at /"}
