"""
Authentication middleware for extracting JWT claims
"""
from typing import Optional, Dict, Any
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt

from backend.services.auth import AuthService

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware to extract JWT claims from cookies or Authorization header"""
    
    def __init__(self, app, secret_key: str, algorithm: str = "HS256"):
        super().__init__(app)
        self.secret_key = secret_key
        self.algorithm = algorithm
    
    async def dispatch(self, request: Request, call_next):
        """Extract JWT claims and add to request state"""
        token = self._extract_token(request)
        claims = None
        
        if token:
            try:
                # Decode JWT token to get claims
                claims = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
                
                # Add claims to request state
                request.state.jwt_claims = claims
                request.state.access_token = token
                
                # Add user info for convenience
                if "sub" in claims:
                    request.state.user_id = int(claims["sub"])
                if "username" in claims:
                    request.state.username = claims["username"]
                    
            except (JWTError, ValueError) as e:
                # Invalid token - don't set claims but don't block request
                # Let the endpoint handle authentication as needed
                request.state.jwt_claims = None
                request.state.access_token = None
        else:
            # No token found
            request.state.jwt_claims = None
            request.state.access_token = None
        
        response = await call_next(request)
        return response
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from cookies or Authorization header"""
        # First, try to get token from cookies
        token = request.cookies.get("access_token")
        if token:
            return token
        
        # If not in cookies, try Authorization header
        authorization = request.headers.get("Authorization")
        if authorization and authorization.startswith("Bearer "):
            return authorization[7:]  # Remove "Bearer " prefix
        
        return None


def get_jwt_claims(request: Request) -> Optional[Dict[str, Any]]:
    """Helper function to get JWT claims from request state"""
    return getattr(request.state, 'jwt_claims', None)


def get_current_user_id(request: Request) -> Optional[int]:
    """Helper function to get current user ID from request state"""
    return getattr(request.state, 'user_id', None)


def get_current_username(request: Request) -> Optional[str]:
    """Helper function to get current username from request state"""
    return getattr(request.state, 'username', None)


def get_access_token(request: Request) -> Optional[str]:
    """Helper function to get access token from request state"""
    return getattr(request.state, 'access_token', None)


def require_auth(request: Request) -> Dict[str, Any]:
    """Helper function that requires authentication and returns claims"""
    claims = get_jwt_claims(request)
    if not claims:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return claims