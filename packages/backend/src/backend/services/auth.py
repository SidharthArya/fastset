"""
Authentication service for ABAC system
"""
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.models.abac import User, UserSession
from backend.schemas.abac import UserCreate, TokenResponse

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = secrets.token_urlsafe(32)  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class AuthService:
    """Authentication service handling login, tokens, and sessions"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token() -> str:
        """Create secure refresh token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """Create new user"""
        hashed_password = AuthService.get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username/password"""
        user = AuthService.get_user_by_username(db, username)
        if not user:
            return None
        if not AuthService.verify_password(password, user.hashed_password):
            return None
        if user.deleted_at is not None:
            return None
        return user
    
    @staticmethod
    def create_user_session(
        db: Session, 
        user: User, 
        context: Optional[Dict[str, Any]] = None
    ) -> UserSession:
        """Create new user session"""
        # Invalidate existing sessions
        db.query(UserSession).filter(
            and_(UserSession.user_id == user.id, UserSession.is_active == True)
        ).update({"is_active": False})
        
        # Create tokens
        access_token = AuthService.create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        refresh_token = AuthService.create_refresh_token()
        
        # Create session
        session = UserSession(
            user_id=user.id,
            session_token=access_token,
            refresh_token=refresh_token,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            context=context or {}
        )
        
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_current_user_from_token(db: Session, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        payload = AuthService.verify_token(token)
        if payload is None:
            return None
        
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        # Check if session is still active
        session = db.query(UserSession).filter(
            and_(
                UserSession.session_token == token,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.now(timezone.utc)
            )
        ).first()
        
        if not session:
            return None
        
        return db.query(User).filter(User.id == int(user_id)).first()
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> Optional[TokenResponse]:
        """Refresh access token using refresh token"""
        session = db.query(UserSession).filter(
            and_(
                UserSession.refresh_token == refresh_token,
                UserSession.is_active == True
            )
        ).first()
        
        if not session:
            return None
        
        user = db.query(User).filter(User.id == session.user_id).first()
        if not user or user.deleted_at is not None:
            return None
        
        # Create new tokens
        new_access_token = AuthService.create_access_token(
            data={"sub": str(user.id), "username": user.username}
        )
        new_refresh_token = AuthService.create_refresh_token()
        
        # Update session
        session.session_token = new_access_token
        session.refresh_token = new_refresh_token
        session.expires_at = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        db.commit()
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
    
    @staticmethod
    def logout_user(db: Session, token: str) -> bool:
        """Logout user by invalidating session"""
        session = db.query(UserSession).filter(
            UserSession.session_token == token
        ).first()
        
        if session:
            session.is_active = False
            db.commit()
            return True
        return False