"""
Authentication API endpoints
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.auth import AuthService
from backend.schemas.abac import (
    LoginRequest, TokenResponse,
    UserCreate, User, UserUpdate
)
from backend.dependencies import get_current_active_user_middleware

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    # Check if user already exists
    if AuthService.get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    if AuthService.get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return AuthService.create_user(db, user)

@router.post("/login", response_model=TokenResponse)
def login(
    login_request: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Authenticate user and return tokens"""
    user = AuthService.authenticate_user(db, login_request.username, login_request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create session context
    context = {
        "ip_address": request.client.host if request.client else None,
        "user_agent": request.headers.get("user-agent"),
        "login_time": str(request.state.__dict__.get("request_time", ""))
    }
    
    session = AuthService.create_user_session(db, user, context)
    
    token = TokenResponse(
        access_token=session.session_token,
        refresh_token=session.refresh_token,
        expires_in=30 * 60  # 30 minutes
    )
    response.set_cookie("access_token", token.access_token)
    response.set_cookie("refresh_token", token.refresh_token)
    return token

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token"""
    if 'refresh_token' not in request.cookies:
        return 404
    refresh_token = request.cookies['refresh_token']
    token_response = AuthService.refresh_access_token(db, refresh_token)
    
    if not token_response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    return token_response

@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user_middleware),
    db: Session = Depends(get_db)
):
    """Logout current user"""
    # Get the access token from cookies
    access_token = request.cookies.get("access_token")
    
    if access_token:
        # Invalidate the session in the database
        AuthService.logout_user(db, access_token)
    
    # Clear the cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_active_user_middleware)):
    """Get current user information"""
    return current_user

@router.put("/me", response_model=User)
def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user_middleware),
    db: Session = Depends(get_db)
):
    """Update current user information"""
    # Update user fields
    if user_update.username is not None:
        # Check if username is already taken
        existing_user = AuthService.get_user_by_username(db, user_update.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = user_update.username
    
    if user_update.email is not None:
        # Check if email is already taken
        existing_user = AuthService.get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken"
            )
        current_user.email = user_update.email
    
    if user_update.password is not None:
        current_user.hashed_password = AuthService.get_password_hash(user_update.password)
    
    if user_update.is_active is not None:
        current_user.is_active = user_update.is_active
    
    db.commit()
    db.refresh(current_user)
    return current_user