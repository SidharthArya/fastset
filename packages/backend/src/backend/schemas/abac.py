"""
Pydantic schemas for ABAC system
"""
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from enum import Enum

class AttributeType(str, Enum):
    USER = "user"
    RESOURCE = "resource"
    ACTION = "action"
    ENVIRONMENT = "environment"

class DataType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    LIST = "list"
    JSON = "json"

class PolicyEffect(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"

# Base schemas
class AttributeBase(BaseModel):
    name: str = Field(..., max_length=100)
    attribute_type: AttributeType
    data_type: DataType
    value: str
    description: Optional[str] = Field(None, max_length=255)
    is_active: bool = True

class AttributeCreate(AttributeBase):
    pass

class AttributeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    value: Optional[str] = None
    description: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class Attribute(AttributeBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime

# User schemas
class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    attributes: List[Attribute] = []

class UserWithAttributes(User):
    attributes: List[Attribute]

# Resource schemas
class ResourceBase(BaseModel):
    name: str = Field(..., max_length=100)
    resource_type: str = Field(..., max_length=50)
    resource_uri: str = Field(..., max_length=255)
    parent_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    resource_type: Optional[str] = Field(None, max_length=50)
    resource_uri: Optional[str] = Field(None, max_length=255)
    parent_id: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class Resource(ResourceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    attributes: List[Attribute] = []

# Action schemas
class ActionBase(BaseModel):
    name: str = Field(..., max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)

class ActionCreate(ActionBase):
    pass

class ActionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    category: Optional[str] = Field(None, max_length=50)

class Action(ActionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

# Policy schemas
class PolicyBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    effect: PolicyEffect
    priority: int = Field(default=0, ge=0)
    conditions: Dict[str, Any]
    action_id: Optional[int] = None
    is_active: bool = True

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    effect: Optional[PolicyEffect] = None
    priority: Optional[int] = Field(None, ge=0)
    conditions: Optional[Dict[str, Any]] = None
    action_id: Optional[int] = None
    is_active: Optional[bool] = None

class Policy(PolicyBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: datetime
    updated_at: datetime
    action: Optional[Action] = None

# Authentication schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# Authorization schemas
class AuthorizationRequest(BaseModel):
    user_id: int
    resource_uri: str
    action_name: str
    context: Optional[Dict[str, Any]] = None

class AuthorizationResponse(BaseModel):
    decision: PolicyEffect
    policy_id: Optional[int] = None
    reason: Optional[str] = None

# Context schemas for ABAC evaluation
class EvaluationContext(BaseModel):
    user_attributes: Dict[str, Any]
    resource_attributes: Dict[str, Any]
    action_attributes: Dict[str, Any]
    environment_attributes: Dict[str, Any]

# Audit schemas
class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    resource_id: Optional[int] = None
    action_id: Optional[int] = None
    decision: PolicyEffect
    policy_id: Optional[int] = None
    context: Dict[str, Any]
    details: Optional[str] = None

class AuditLog(AuditLogBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    timestamp: datetime