from fastapi import FastAPI, Depends, HTTPException, status
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import List, Optional
from pydantic import BaseModel

# Get configuration from environment variables
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql-service")
MYSQL_USER = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "appdb")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://frontend-service:3000")
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "info")
JWT_SECRET = os.getenv("JWT_SECRET", "default-secret-key")

# Define app with optional documentation URLs
app = FastAPI(
    title="Kub Project API",
    description="API for Kub Project Microservices Demo",
    version="1.0.0",
    docs_url=os.getenv("DOCS_URL", "/docs"),
    redoc_url=os.getenv("REDOC_URL", "/redoc")
)

# Add CORS middleware to allow frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if APP_ENV == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not connect to database"
        )

@app.get("/")
def read_root():
    return {"msg": "Hello from FastAPI"}

@app.get("/db")
def db_test():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 'Hello from MySQL!'")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"msg": result[0]}

# User model
class User(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

@app.get("/users", response_model=List[User])
def get_users():
    try:
        # Connect to the database
        conn = get_db_connection()
        
        # Create a cursor and execute the query
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, email, phone FROM users")
        
        # Fetch all results
        users = cursor.fetchall()
        
        # Close cursor and connection
        cursor.close()
        conn.close()
        
        return users
    except Exception as e:
        # If there's an error, return mock data as fallback
        print(f"Database error: {str(e)}")
        return [
            {"name": "John Doe", "email": "john@example.com", "phone": "555-1234"},
            {"name": "Jane Smith", "email": "jane@example.com", "phone": "555-5678"},
            {"name": "Bob Johnson", "email": "bob@example.com", "phone": "555-9012"}
        ]

@app.get("/health")
def health_check():
    """Health check endpoint for Kubernetes probes"""
    try:
        # Test database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )
