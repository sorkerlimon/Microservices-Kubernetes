"""
User-related Pydantic schemas.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any, Union

# User schemas
class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True

# User detail schemas
class UserDetailBase(BaseModel):
    name: str
    email: str
    phone: str

class UserDetailCreate(UserDetailBase):
    pass

class UserDetailResponse(UserDetailBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True

# Combined schemas
class UserWithDetails(UserResponse):
    details: Optional[UserDetailResponse] = None
    
    class Config:
        orm_mode = True

# Authentication schemas
class UserLogin(BaseModel):
    email: str
    password: str

# Cache response schemas
class CacheSourceResponse(BaseModel):
    source: str
    data: Any

    class Config:
        orm_mode = True

class UserListCacheResponse(CacheSourceResponse):
    data: Union[List[UserResponse], List[Dict[str, Any]]]

class UserDetailCacheResponse(CacheSourceResponse):
    data: Union[UserWithDetails, Dict[str, Any]]

class UserDetailsListCacheResponse(CacheSourceResponse):
    data: Union[List[UserDetailResponse], List[Dict[str, Any]]]

class UserDetailSingleCacheResponse(CacheSourceResponse):
    data: Union[UserDetailResponse, Dict[str, Any]]

class SessionCacheResponse(CacheSourceResponse):
    data: Dict[str, Any] 