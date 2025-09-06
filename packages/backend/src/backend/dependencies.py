"""
FastAPI dependencies for authentication and authorization
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.services.auth import AuthService
from backend.services.abac_engine import ABACEngine
from backend.models.abac import User
from backend.schemas.abac import AuthorizationRequest, PolicyEffect
from backend.middleware import get_jwt_claims, get_current_user_id, get_access_token

# Security scheme
security = HTTPBearer()

# New middleware-based dependencies
def get_current_user_from_middleware(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get current user using middleware-extracted claims"""
    user_id = get_current_user_id(request)
    if not user_id:
        return None
    
    # Get token to validate session is still active
    token = get_access_token(request)
    if not token:
        return None
    
    return AuthService.get_current_user_from_token(db, token)

def require_auth_middleware(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """Require authentication using middleware-extracted claims"""
    user = get_current_user_from_middleware(request, db)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user_middleware(
    user: User = Depends(require_auth_middleware)
) -> User:
    """Get current active user using middleware"""
    if user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    user = AuthService.get_current_user_from_token(db, token)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if current_user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_abac_engine(db: Session = Depends(get_db)) -> ABACEngine:
    """Get ABAC engine instance"""
    return ABACEngine(db)

def require_permission(resource_uri: str, action_name: str):
    """
    Dependency factory for ABAC authorization
    Usage: @app.get("/protected", dependencies=[Depends(require_permission("/api/users", "read"))])
    """
    def check_permission(
        current_user: User = Depends(get_current_active_user),
        abac_engine: ABACEngine = Depends(get_abac_engine)
    ):
        request = AuthorizationRequest(
            user_id=current_user.id,
            resource_uri=resource_uri,
            action_name=action_name
        )
        
        response = abac_engine.evaluate_access(request)
        
        if response.decision == PolicyEffect.DENY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {response.reason}"
            )
        
        return True
    
    return check_permission

class PermissionChecker:
    """Class-based permission checker for more complex scenarios"""
    
    def __init__(self, resource_uri: str, action_name: str):
        self.resource_uri = resource_uri
        self.action_name = action_name
    
    def __call__(
        self,
        current_user: User = Depends(get_current_active_user),
        abac_engine: ABACEngine = Depends(get_abac_engine)
    ):
        request = AuthorizationRequest(
            user_id=current_user.id,
            resource_uri=self.resource_uri,
            action_name=self.action_name
        )
        
        response = abac_engine.evaluate_access(request)
        
        if response.decision == PolicyEffect.DENY:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: {response.reason}"
            )
        
        return response