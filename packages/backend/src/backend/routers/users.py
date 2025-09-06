"""
User management API endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.auth import AuthService
from backend.schemas.abac import User, UserCreate, UserUpdate
from backend.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of users to return"),
    search: Optional[str] = Query(None, description="Search by username or email"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get list of users with pagination and search"""
    # TODO: Add proper authorization check here
    users = AuthService.get_users(db, skip=skip, limit=limit, search=search)
    return users


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get user by ID"""
    # TODO: Add proper authorization check here
    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Create a new user"""
    # TODO: Add proper authorization check here (admin only)

    # Check if user already exists
    if AuthService.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    if AuthService.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    return AuthService.create_user(db, user)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update user by ID"""
    # TODO: Add proper authorization check here (admin or self)

    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Check if username is already taken
    if user_update.username is not None:
        existing_user = AuthService.get_user_by_username(db, user_update.username)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
            )
        user.username = user_update.username

    # Check if email is already taken
    if user_update.email is not None:
        existing_user = AuthService.get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken"
            )
        user.email = user_update.email

    # Update password if provided
    if user_update.password is not None:
        user.hashed_password = AuthService.get_password_hash(user_update.password)

    # Update active status if provided
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete user by ID"""
    # TODO: Add proper authorization check here (admin only)

    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Prevent self-deletion
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account",
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
