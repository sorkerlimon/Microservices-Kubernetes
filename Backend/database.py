"""
Database connection and session management.
"""

import os
import sys
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

# Database connection
# Get the database URL from environment variable or use default for local development
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://kubuser:kubpassword@kub-database:3306/kubdb")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    sys.exit(1)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 