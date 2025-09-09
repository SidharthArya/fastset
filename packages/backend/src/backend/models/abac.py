"""
ABAC (Attribute-Based Access Control) Models
Provides flexible, attribute-driven authorization system
"""
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column

from backend.models.base import DeclaredBase
from backend.models.types import AttributeType, DataType

# Association classes for many-to-many relationships
class UserAttribute(DeclaredBase):
    """Association table for User-Attribute many-to-many relationship"""
    __tablename__ = 'user_attributes'
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), primary_key=True)
    attribute_id: Mapped[int] = mapped_column(Integer, ForeignKey('attributes.id'), primary_key=True)

class ResourceAttribute(DeclaredBase):
    """Association table for Resource-Attribute many-to-many relationship"""
    __tablename__ = 'resource_attributes'
    
    resource_id: Mapped[int] = mapped_column(Integer, ForeignKey('resources.id'), primary_key=True)
    attribute_id: Mapped[int] = mapped_column(Integer, ForeignKey('attributes.id'), primary_key=True)


class User(DeclaredBase):
    """User entity with core identity information"""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    # Relationships
    attributes: Mapped[List["Attribute"]] = relationship("Attribute", secondary="user_attributes", back_populates="users")
    sessions: Mapped[List["UserSession"]] = relationship("UserSession", back_populates="user")

class Resource(DeclaredBase):
    """Resource entity representing protected objects"""
    __tablename__ = "resources"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    resource_uri: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("resources.id"), nullable=True)
    metadata_: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    # Relationships
    attributes: Mapped[List["Attribute"]] = relationship("Attribute", secondary="resource_attributes", back_populates="resources")
    parent: Mapped[Optional["Resource"]] = relationship("Resource", remote_side=[id])
    children: Mapped[List["Resource"]] = relationship("Resource")

class Action(DeclaredBase):
    """Action entity representing operations that can be performed"""
    __tablename__ = "actions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    # Relationships
    policies: Mapped[List["Policy"]] = relationship("Policy", back_populates="action")

class Attribute(DeclaredBase):
    """Flexible attribute system for ABAC"""
    __tablename__ = "attributes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    attribute_type: Mapped[AttributeType] = mapped_column(String(20), nullable=False, index=True)
    data_type: Mapped[DataType] = mapped_column(String(20), nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)  # Stored as string, parsed based on data_type
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    # Relationships
    users: Mapped[List[User]] = relationship("User", secondary="user_attributes", back_populates="attributes")
    resources: Mapped[List[Resource]] = relationship("Resource", secondary="resource_attributes", back_populates="attributes")

class Policy(DeclaredBase):
    """ABAC Policy definitions"""
    __tablename__ = "policies"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    effect: Mapped[str] = mapped_column(String(10), nullable=False)  # ALLOW or DENY
    priority: Mapped[int] = mapped_column(Integer, default=0)  # Higher number = higher priority
    
    # Policy conditions (stored as JSON for flexibility)
    conditions: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    # Optional specific action (if None, applies to all actions)
    action_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("actions.id"), nullable=True)
    
    
    # Relationships
    action: Mapped[Optional[Action]] = relationship("Action", back_populates="policies")

class UserSession(DeclaredBase):
    """User session management for authentication"""
    __tablename__ = "user_sessions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    session_token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    # Session context attributes (IP, user agent, etc.)
    context: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    # Relationships
    user: Mapped[User] = relationship("User", back_populates="sessions")

class AuditLog(DeclaredBase):
    """Audit trail for access decisions and actions"""
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    resource_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("resources.id"), nullable=True)
    action_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("actions.id"), nullable=True)
    
    decision: Mapped[str] = mapped_column(String(10), nullable=False)  # ALLOW or DENY
    policy_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("policies.id"), nullable=True)
    
    # Context at time of decision
    context: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), index=True)
    
    # Optional additional details
    details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)