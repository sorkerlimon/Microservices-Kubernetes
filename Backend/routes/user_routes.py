"""
User management routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from models.user import User
from models.user_details import UserDetail
from database import get_db
from schema.user import UserCreate, UserResponse, UserLogin, UserWithDetails, UserDetailCreate, UserDetailResponse
from utils.cache import cache_get, cache_set, cache_invalidate_pattern, cache_delete
from auth import hash_password, verify_password
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# User endpoints
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(user.password)
    db_user = User(email=user.email, password=hashed_password)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Invalidate users cache
    cache_invalidate_pattern("users:all:*")
    
    logger.info(f"Created new user with ID {db_user.id} directly in database")
    return db_user

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Try to get from cache
    cache_key = f"users:all:skip{skip}:limit{limit}"
    cached_data = cache_get(cache_key)
    
    if cached_data:
        # Convert cached data to User objects
        logger.info(f"Retrieved users list from Redis cache with key: {cache_key}")
        return cached_data
    
    # If not in cache, get from database
    users = db.query(User).offset(skip).limit(limit).all()
    
    # Cache the result for 5 minutes
    user_data = [{"id": user.id, "email": user.email} for user in users]
    cache_set(cache_key, user_data, 300)
    
    logger.info(f"Retrieved users list directly from database and cached with key: {cache_key}")
    return users

@router.get("/{user_id}", response_model=UserWithDetails)
def read_user(user_id: int, db: Session = Depends(get_db)):
    # Try to get from cache
    cache_key = f"users:{user_id}"
    cached_user = cache_get(cache_key)
    
    if cached_user:
        logger.info(f"Retrieved user ID {user_id} from Redis cache")
        return cached_user
    
    # If not in cache, get from database
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prepare response data
    response_data = {
        "id": db_user.id,
        "email": db_user.email,
        "details": None
    }
    
    if db_user.details:
        response_data["details"] = {
            "id": db_user.details.id,
            "user_id": db_user.details.user_id,
            "name": db_user.details.name,
            "email": db_user.details.email,
            "phone": db_user.details.phone
        }
    
    # Cache the result for 5 minutes
    cache_set(cache_key, response_data, 300)
    
    logger.info(f"Retrieved user ID {user_id} directly from database and cached")
    return db_user

@router.post("/{user_id}/details/", response_model=UserDetailResponse)
def create_user_detail(user_id: int, detail: UserDetailCreate, db: Session = Depends(get_db)):
    """Create details for a specific user."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    # Check if details already exist
    existing_detail = db.query(UserDetail).filter(UserDetail.user_id == user_id).first()
    if existing_detail:
        raise HTTPException(status_code=400, detail="User details already exist")
        
    # Check if email is already registered
    email_check = db.query(UserDetail).filter(UserDetail.email == detail.email).first()
    if email_check:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Check if phone is already registered
    phone_check = db.query(UserDetail).filter(UserDetail.phone == detail.phone).first()
    if phone_check:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    db_detail = UserDetail(
        user_id=user_id,
        name=detail.name,
        email=detail.email,
        phone=detail.phone
    )
    
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    
    # Invalidate cache
    cache_delete(f"users:{user_id}")
    cache_invalidate_pattern("users:all:*")
    cache_invalidate_pattern("user-details:*")
    
    logger.info(f"Created user details for user ID {user_id} directly in database")
    return db_detail 