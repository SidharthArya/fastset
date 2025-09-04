"""
ABAC management API endpoints
"""
from typing import List, Optional
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from backend.database import get_db
from backend.dependencies import get_current_active_user, require_permission
from backend.models.abac import User, Resource, Action, Attribute, Policy, AuditLog
from backend.schemas.abac import (
    ResourceCreate, ResourceUpdate, Resource as ResourceSchema,
    ActionCreate, ActionUpdate, Action as ActionSchema,
    AttributeCreate, AttributeUpdate, Attribute as AttributeSchema,
    PolicyCreate, PolicyUpdate, Policy as PolicySchema,
    AuthorizationRequest, AuthorizationResponse,
    AuditLog as AuditLogSchema
)
from backend.services.abac_engine import ABACEngine

router = APIRouter(prefix="/abac", tags=["abac"])

# Resource management
@router.post("/resources", response_model=ResourceSchema, status_code=status.HTTP_201_CREATED)
def create_resource(
    resource: ResourceCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/resources", "create"))
):
    """Create a new resource"""
    db_resource = Resource(**resource.model_dump())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.get("/resources", response_model=List[ResourceSchema])
def list_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    resource_type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/resources", "read"))
):
    """List resources with optional filtering"""
    query = db.query(Resource)
    
    if resource_type:
        query = query.filter(Resource.resource_type == resource_type)
    
    return query.offset(skip).limit(limit).all()

@router.get("/resources/{resource_id}", response_model=ResourceSchema)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/resources", "read"))
):
    """Get resource by ID"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.put("/resources/{resource_id}", response_model=ResourceSchema)
def update_resource(
    resource_id: int,
    resource_update: ResourceUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/resources", "update"))
):
    """Update resource"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    update_data = resource_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(resource, field, value)
    
    db.commit()
    db.refresh(resource)
    return resource

@router.delete("/resources/{resource_id}")
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/resources", "delete"))
):
    """Delete resource"""
    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    db.delete(resource)
    db.commit()
    return {"message": "Resource deleted successfully"}

# Action management
@router.post("/actions", response_model=ActionSchema, status_code=status.HTTP_201_CREATED)
def create_action(
    action: ActionCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/actions", "create"))
):
    """Create a new action"""
    # Check if action already exists
    existing = db.query(Action).filter(Action.name == action.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Action already exists")
    
    db_action = Action(**action.model_dump())
    db.add(db_action)
    db.commit()
    db.refresh(db_action)
    return db_action

@router.get("/actions", response_model=List[ActionSchema])
def list_actions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/actions", "read"))
):
    """List actions with optional filtering"""
    query = db.query(Action)
    
    if category:
        query = query.filter(Action.category == category)
    
    return query.offset(skip).limit(limit).all()

# Attribute management
@router.post("/attributes", response_model=AttributeSchema, status_code=status.HTTP_201_CREATED)
def create_attribute(
    attribute: AttributeCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/attributes", "create"))
):
    """Create a new attribute"""
    db_attribute = Attribute(**attribute.model_dump())
    db.add(db_attribute)
    db.commit()
    db.refresh(db_attribute)
    return db_attribute

@router.get("/attributes", response_model=List[AttributeSchema])
def list_attributes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    attribute_type: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/attributes", "read"))
):
    """List attributes with optional filtering"""
    query = db.query(Attribute)
    
    if attribute_type:
        query = query.filter(Attribute.attribute_type == attribute_type)
    
    if is_active is not None:
        query = query.filter(Attribute.is_active == is_active)
    
    return query.offset(skip).limit(limit).all()

# Policy management
@router.post("/policies", response_model=PolicySchema, status_code=status.HTTP_201_CREATED)
def create_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/policies", "create"))
):
    """Create a new policy"""
    db_policy = Policy(**policy.model_dump())
    db.add(db_policy)
    db.commit()
    db.refresh(db_policy)
    return db_policy

@router.get("/policies", response_model=List[PolicySchema])
def list_policies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = Query(None),
    effect: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/policies", "read"))
):
    """List policies with optional filtering"""
    query = db.query(Policy)
    
    if is_active is not None:
        query = query.filter(Policy.is_active == is_active)
    
    if effect:
        query = query.filter(Policy.effect == effect)
    
    return query.order_by(Policy.priority.desc()).offset(skip).limit(limit).all()

@router.put("/policies/{policy_id}", response_model=PolicySchema)
def update_policy(
    policy_id: int,
    policy_update: PolicyUpdate,
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/policies", "update"))
):
    """Update policy"""
    policy = db.query(Policy).filter(Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    update_data = policy_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(policy, field, value)
    
    db.commit()
    db.refresh(policy)
    return policy

# Authorization endpoint
@router.post("/authorize", response_model=AuthorizationResponse)
def authorize_access(
    request: AuthorizationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Evaluate access request using ABAC engine"""
    abac_engine = ABACEngine(db)
    return abac_engine.evaluate_access(request)

# Audit logs
@router.get("/audit-logs", response_model=List[AuditLogSchema])
def get_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: Optional[int] = Query(None),
    resource_id: Optional[int] = Query(None),
    decision: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    _: bool = Depends(require_permission("/abac/audit-logs", "read"))
):
    """Get audit logs with optional filtering"""
    query = db.query(AuditLog)
    
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    if resource_id:
        query = query.filter(AuditLog.resource_id == resource_id)
    
    if decision:
        query = query.filter(AuditLog.decision == decision)
    
    return query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()