"""
ABAC Policy Decision Point (PDP) Engine
Evaluates policies against user, resource, action, and environment attributes
"""
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from backend.models.abac import User, Resource, Action, Attribute, Policy, AuditLog
from backend.schemas.abac import AuthorizationRequest, AuthorizationResponse, PolicyEffect, EvaluationContext

class ABACEngine:
    """ABAC Policy Decision Point for evaluating access requests"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def evaluate_access(self, request: AuthorizationRequest) -> AuthorizationResponse:
        """
        Main entry point for ABAC evaluation
        Returns ALLOW/DENY decision with reasoning
        """
        try:
            # Get entities
            user = self.db.query(User).filter(User.id == request.user_id).first()
            if not user or not user.is_active:
                return self._create_response(PolicyEffect.DENY, reason="User not found or inactive")
            
            resource = self.db.query(Resource).filter(Resource.resource_uri == request.resource_uri).first()
            if not resource:
                return self._create_response(PolicyEffect.DENY, reason="Resource not found")
            
            action = self.db.query(Action).filter(Action.name == request.action_name).first()
            if not action:
                return self._create_response(PolicyEffect.DENY, reason="Action not found")
            
            # Build evaluation context
            context = self._build_evaluation_context(user, resource, action, request.context or {})
            
            # Get applicable policies
            policies = self._get_applicable_policies(action.id)
            
            # Evaluate policies in priority order
            decision, policy_id, reason = self._evaluate_policies(policies, context)
            
            # Log the decision
            self._log_decision(user.id, resource.id, action.id, decision, policy_id, context, reason)
            
            return AuthorizationResponse(
                decision=decision,
                policy_id=policy_id,
                reason=reason
            )
            
        except Exception as e:
            # Default deny on any error
            self._log_decision(
                request.user_id, None, None, PolicyEffect.DENY, None, 
                {"error": str(e)}, f"System error: {str(e)}"
            )
            return self._create_response(PolicyEffect.DENY, reason=f"System error: {str(e)}")
    
    def _build_evaluation_context(
        self, 
        user: User, 
        resource: Resource, 
        action: Action, 
        environment: Dict[str, Any]
    ) -> EvaluationContext:
        """Build complete evaluation context with all attributes"""
        
        # Get user attributes
        user_attrs = {}
        for attr in user.attributes:
            if attr.is_active:
                user_attrs[attr.name] = self._parse_attribute_value(attr.value, attr.data_type)
        
        # Add built-in user attributes
        user_attrs.update({
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat()
        })
        
        # Get resource attributes
        resource_attrs = {}
        for attr in resource.attributes:
            if attr.is_active:
                resource_attrs[attr.name] = self._parse_attribute_value(attr.value, attr.data_type)
        
        # Add built-in resource attributes
        resource_attrs.update({
            "resource_id": resource.id,
            "resource_name": resource.name,
            "resource_type": resource.resource_type,
            "resource_uri": resource.resource_uri,
            "parent_id": resource.parent_id
        })
        
        # Action attributes
        action_attrs = {
            "action_id": action.id,
            "action_name": action.name,
            "action_category": action.category,
            "action_description": action.description
        }
        
        # Environment attributes (time, IP, etc.)
        env_attrs = environment.copy()
        env_attrs.update({
            "current_time": datetime.now(timezone.utc).isoformat(),
            "day_of_week": datetime.now(timezone.utc).weekday(),
            "hour": datetime.now(timezone.utc).hour
        })
        
        return EvaluationContext(
            user_attributes=user_attrs,
            resource_attributes=resource_attrs,
            action_attributes=action_attrs,
            environment_attributes=env_attrs
        )
    
    def _get_applicable_policies(self, action_id: Optional[int]) -> List[Policy]:
        """Get policies applicable to the action, sorted by priority"""
        query = self.db.query(Policy).filter(Policy.is_active == True)
        
        # Get policies for specific action or global policies
        if action_id:
            query = query.filter(or_(Policy.action_id == action_id, Policy.action_id.is_(None)))
        else:
            query = query.filter(Policy.action_id.is_(None))
        
        return query.order_by(Policy.priority.desc(), Policy.created_at.asc()).all()
    
    def _evaluate_policies(
        self, 
        policies: List[Policy], 
        context: EvaluationContext
    ) -> Tuple[PolicyEffect, Optional[int], str]:
        """Evaluate policies against context"""
        
        if not policies:
            return PolicyEffect.DENY, None, "No applicable policies found"
        
        for policy in policies:
            try:
                if self._evaluate_policy_conditions(policy.conditions, context):
                    effect = PolicyEffect.ALLOW if policy.effect == "ALLOW" else PolicyEffect.DENY
                    return effect, policy.id, f"Policy '{policy.name}' matched"
            except Exception as e:
                # Continue to next policy on evaluation error
                continue
        
        # Default deny if no policies match
        return PolicyEffect.DENY, None, "No matching policies"
    
    def _evaluate_policy_conditions(self, conditions: Dict[str, Any], context: EvaluationContext) -> bool:
        """Evaluate policy conditions against context"""
        
        # Convert context to flat dictionary for easier evaluation
        flat_context = {
            **{f"user.{k}": v for k, v in context.user_attributes.items()},
            **{f"resource.{k}": v for k, v in context.resource_attributes.items()},
            **{f"action.{k}": v for k, v in context.action_attributes.items()},
            **{f"environment.{k}": v for k, v in context.environment_attributes.items()}
        }
        
        return self._evaluate_condition_tree(conditions, flat_context)
    
    def _evaluate_condition_tree(self, condition: Any, context: Dict[str, Any]) -> bool:
        """Recursively evaluate condition tree"""
        
        if isinstance(condition, dict):
            # Handle logical operators
            if "and" in condition:
                return all(self._evaluate_condition_tree(c, context) for c in condition["and"])
            elif "or" in condition:
                return any(self._evaluate_condition_tree(c, context) for c in condition["or"])
            elif "not" in condition:
                return not self._evaluate_condition_tree(condition["not"], context)
            
            # Handle comparison operators
            elif "equals" in condition:
                attr = condition["equals"]["attribute"]
                value = condition["equals"]["value"]
                return context.get(attr) == value
            elif "in" in condition:
                attr = condition["in"]["attribute"]
                values = condition["in"]["values"]
                return context.get(attr) in values
            elif "contains" in condition:
                attr = condition["contains"]["attribute"]
                value = condition["contains"]["value"]
                attr_value = context.get(attr)
                return isinstance(attr_value, (list, str)) and value in attr_value
            elif "greater_than" in condition:
                attr = condition["greater_than"]["attribute"]
                value = condition["greater_than"]["value"]
                return context.get(attr, 0) > value
            elif "less_than" in condition:
                attr = condition["less_than"]["attribute"]
                value = condition["less_than"]["value"]
                return context.get(attr, 0) < value
            elif "regex" in condition:
                import re
                attr = condition["regex"]["attribute"]
                pattern = condition["regex"]["pattern"]
                attr_value = str(context.get(attr, ""))
                return bool(re.match(pattern, attr_value))
        
        # Default to False for unknown conditions
        return False
    
    def _parse_attribute_value(self, value: str, data_type: str) -> Any:
        """Parse attribute value based on data type"""
        try:
            if data_type == "integer":
                return int(value)
            elif data_type == "boolean":
                return value.lower() in ("true", "1", "yes")
            elif data_type == "datetime":
                return datetime.fromisoformat(value)
            elif data_type == "list":
                return json.loads(value)
            elif data_type == "json":
                return json.loads(value)
            else:  # string
                return value
        except (ValueError, json.JSONDecodeError):
            return value  # Return as string if parsing fails
    
    def _create_response(
        self, 
        decision: PolicyEffect, 
        policy_id: Optional[int] = None, 
        reason: Optional[str] = None
    ) -> AuthorizationResponse:
        """Create authorization response"""
        return AuthorizationResponse(
            decision=decision,
            policy_id=policy_id,
            reason=reason
        )
    
    def _log_decision(
        self,
        user_id: Optional[int],
        resource_id: Optional[int],
        action_id: Optional[int],
        decision: PolicyEffect,
        policy_id: Optional[int],
        context: Any,
        reason: str
    ):
        """Log access decision for audit trail"""
        try:
            audit_log = AuditLog(
                user_id=user_id,
                resource_id=resource_id,
                action_id=action_id,
                decision=decision.value,
                policy_id=policy_id,
                context=context if isinstance(context, dict) else {"context": str(context)},
                details=reason
            )
            self.db.add(audit_log)
            self.db.commit()
        except Exception:
            # Don't fail authorization on audit logging errors
            pass