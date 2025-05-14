"""
Authentication routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from models.user import User
from database import get_db
from schema.user import UserLogin
from utils.cache import cache_get, cache_set
from auth import verify_password

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)

@router.post("/login/")
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login a user and return session data."""
    # Find user by email
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(user_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Check if there's a cached session
    session_key = f"session:user:{db_user.id}"
    session_data = cache_get(session_key)
    
    # If no valid session, create a new one
    if not session_data:
        # Get user with details
        user_with_details = db.query(User).filter(User.id == db_user.id).first()
        
        # Format response similar to UserWithDetails model
        session_data = {
            "id": user_with_details.id,
            "email": user_with_details.email,
            "details": {
                "name": user_with_details.details.name if user_with_details.details else None,
                "email": user_with_details.details.email if user_with_details.details else None,
                "phone": user_with_details.details.phone if user_with_details.details else None
            } if user_with_details.details else None,
            "last_login": str(datetime.now())
        }
        
        # Cache session for 24 hours
        cache_set(session_key, session_data, 86400)
        logger.info(f"Created new session for user ID {db_user.id} directly from database")
        return session_data
    
    logger.info(f"Retrieved existing session for user ID {db_user.id} from Redis cache")
    return session_data 