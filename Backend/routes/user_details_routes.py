"""
User details management routes.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from models.user import User
from models.user_details import UserDetail
from database import get_db
from schema.user import UserDetailCreate, UserDetailResponse
from utils.cache import cache_get, cache_set, cache_invalidate_pattern, cache_delete

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/user-details",
    tags=["user details"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[UserDetailResponse])
def read_user_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get a list of all user details."""
    # Try to get from cache
    cache_key = f"user-details:all:skip{skip}:limit{limit}"
    cached_data = cache_get(cache_key)
    
    if cached_data:
        logger.info(f"Retrieved user details list from Redis cache with key: {cache_key}")
        return cached_data
        
    # If not in cache, get from database
    details = db.query(UserDetail).offset(skip).limit(limit).all()
    
    # Cache the result for 5 minutes
    details_data = [{
        "id": detail.id,
        "user_id": detail.user_id,
        "name": detail.name,
        "email": detail.email,
        "phone": detail.phone
    } for detail in details]
    cache_set(cache_key, details_data, 300)
    
    logger.info(f"Retrieved user details list directly from database and cached with key: {cache_key}")
    return details

@router.get("/{detail_id}", response_model=UserDetailResponse)
def read_user_detail(detail_id: int, db: Session = Depends(get_db)):
    """Get details for a specific user detail ID."""
    # Try to get from cache
    cache_key = f"user-details:{detail_id}"
    cached_detail = cache_get(cache_key)
    
    if cached_detail:
        logger.info(f"Retrieved user detail ID {detail_id} from Redis cache")
        return cached_detail
        
    # If not in cache, get from database
    db_detail = db.query(UserDetail).filter(UserDetail.id == detail_id).first()
    if db_detail is None:
        raise HTTPException(status_code=404, detail="User detail not found")
        
    # Cache the result for 5 minutes
    detail_data = {
        "id": db_detail.id,
        "user_id": db_detail.user_id,
        "name": db_detail.name,
        "email": db_detail.email,
        "phone": db_detail.phone
    }
    cache_set(cache_key, detail_data, 300)
    
    logger.info(f"Retrieved user detail ID {detail_id} directly from database and cached")
    return db_detail 