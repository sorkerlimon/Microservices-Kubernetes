"""
Main FastAPI application.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
import re

# Import DB models
from models.user import User
from models.user_details import UserDetail
from database import engine, Base

# Import Redis client for health check
from utils.cache import redis_client

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

# Create custom middleware to add source information headers
class DataSourceMiddleware:
    async def __call__(self, request: Request, call_next):
        # Process the request and get the response
        response = await call_next(request)
        
        # Try to determine the source from recent logs
        try:
            with open("app.log", "r") as f:
                logs = f.readlines()
                # Get the most recent 5 log lines
                recent_logs = logs[-5:]
                for log in reversed(recent_logs):
                    if "from Redis cache" in log:
                        response.headers["X-Data-Source"] = "redis_cache"
                        break
                    elif "from database" in log:
                        response.headers["X-Data-Source"] = "database"
                        break
        except Exception as e:
            logger.error(f"Error adding data source header: {e}")
            
        return response

# Create FastAPI app
app = FastAPI(
    title="Kub Project API",
    description="API for the Kub Project",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, change this to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add our custom middleware
app.middleware("http")(DataSourceMiddleware())

# Kafka config check
import os
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kub-kafka:9092")
logger.info(f"Kafka broker configured at: {KAFKA_BROKER}")

# Include routers
from routes import user_routes, user_details_routes
from routes.kafka_routes import router as kafka_router
from routes.auth_routes import router as auth_router

app.include_router(user_routes.router)
app.include_router(user_details_routes.router)
app.include_router(kafka_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Kub Project API"}

@app.get("/health")
async def health_check():
    health_status = {
        "database": "healthy",
        "redis": "healthy",
        "kafka": "checking"
    }
    
    # Check database
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception as e:
        health_status["database"] = f"unhealthy: {str(e)}"
    
    # Check Redis
    try:
        if not redis_client.ping():
            health_status["redis"] = "unhealthy: ping failed"
    except Exception as e:
        health_status["redis"] = f"unhealthy: {str(e)}"
    
    # Check Kafka
    try:
        import kafka_utils
        kafka_utils.list_topics()
        health_status["kafka"] = "healthy"
    except Exception as e:
        health_status["kafka"] = f"unhealthy: {str(e)}"
    
    # Overall status
    if all(status == "healthy" for status in health_status.values()):
        return {"status": "healthy", "services": health_status}
    else:
        return {"status": "degraded", "services": health_status}

@app.on_event("startup")
async def startup_event():
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Check if Kafka is available
        try:
            import kafka_utils
            topics = kafka_utils.list_topics()
            logger.info(f"Connected to Kafka. Available topics: {topics}")
        except Exception as e:
            logger.warning(f"Kafka connection failed on startup: {e}")
            logger.warning("Application will continue, but Kafka features may not work")
            
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        # We'll let the app start anyway, but log the error

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
