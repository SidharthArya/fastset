"""
Initialize sample data for ABAC system
Run this script to populate the database with sample users, resources, actions, attributes, and policies
"""
import json
from sqlalchemy.orm import Session
from backend.database import SessionLocal, create_tables
from backend.models.abac import User, Resource, Action, Attribute, Policy
from backend.services.auth import AuthService

def init_sample_data():
    """Initialize sample data for testing ABAC system"""
    
    # Create tables
    create_tables()
    
    db = SessionLocal()
    
    try:
        # Create sample users
        if not db.query(User).filter(User.username == "admin").first():
            admin_user = User(
                username="admin",
                email="admin@fastset.com",
                hashed_password=AuthService.get_password_hash("admin123"),
            )
            db.add(admin_user)
        
        if not db.query(User).filter(User.username == "analyst").first():
            analyst_user = User(
                username="analyst",
                email="analyst@fastset.com", 
                hashed_password=AuthService.get_password_hash("analyst123"),
            )
            db.add(analyst_user)
        
        if not db.query(User).filter(User.username == "viewer").first():
            viewer_user = User(
                username="viewer",
                email="viewer@fastset.com",
                hashed_password=AuthService.get_password_hash("viewer123"),
            )
            db.add(viewer_user)
        
        db.commit()
        
        # Get user IDs
        admin = db.query(User).filter(User.username == "admin").first()
        analyst = db.query(User).filter(User.username == "analyst").first()
        viewer = db.query(User).filter(User.username == "viewer").first()
        
        # Create sample actions
        actions_data = [
            {"name": "create", "description": "Create new resources", "category": "write"},
            {"name": "read", "description": "Read/view resources", "category": "read"},
            {"name": "update", "description": "Update existing resources", "category": "write"},
            {"name": "delete", "description": "Delete resources", "category": "write"},
            {"name": "admin", "description": "Administrative operations", "category": "admin"}
        ]
        
        for action_data in actions_data:
            if not db.query(Action).filter(Action.name == action_data["name"]).first():
                action = Action(**action_data)
                db.add(action)
        
        db.commit()
        
        # Create sample resources
        resources_data = [
            {"name": "Dashboard API", "resource_type": "api", "resource_uri": "/api/dashboard"},
            {"name": "User Management", "resource_type": "api", "resource_uri": "/api/users"},
            {"name": "Reports API", "resource_type": "api", "resource_uri": "/api/reports"},
            {"name": "ABAC Resources", "resource_type": "api", "resource_uri": "/abac/resources"},
            {"name": "ABAC Policies", "resource_type": "api", "resource_uri": "/abac/policies"},
            {"name": "Audit Logs", "resource_type": "api", "resource_uri": "/abac/audit-logs"}
        ]
        
        for resource_data in resources_data:
            if not db.query(Resource).filter(Resource.resource_uri == resource_data["resource_uri"]).first():
                resource = Resource(**resource_data)
                db.add(resource)
        
        db.commit()
        
        # Create sample attributes
        attributes_data = [
            # User attributes
            {"name": "role", "attribute_type": "user", "data_type": "string", "value": "admin", "description": "User role"},
            {"name": "department", "attribute_type": "user", "data_type": "string", "value": "IT", "description": "User department"},
            {"name": "clearance_level", "attribute_type": "user", "data_type": "integer", "value": "5", "description": "Security clearance level"},
            
            # Resource attributes  
            {"name": "sensitivity", "attribute_type": "resource", "data_type": "string", "value": "public", "description": "Data sensitivity level"},
            {"name": "owner", "attribute_type": "resource", "data_type": "string", "value": "system", "description": "Resource owner"},
            
            # Environment attributes
            {"name": "network", "attribute_type": "environment", "data_type": "string", "value": "internal", "description": "Network location"}
        ]
        
        for attr_data in attributes_data:
            attr = Attribute(**attr_data)
            db.add(attr)
        
        db.commit()
        
        # Assign attributes to users
        role_admin = db.query(Attribute).filter(Attribute.name == "role", Attribute.value == "admin").first()
        dept_it = db.query(Attribute).filter(Attribute.name == "department").first()
        clearance_5 = db.query(Attribute).filter(Attribute.name == "clearance_level").first()
        
        if role_admin:
            admin.attributes.append(role_admin)
            admin.attributes.append(dept_it)
            admin.attributes.append(clearance_5)
        
        # Create analyst role attribute
        analyst_role = Attribute(
            name="role", 
            attribute_type="user", 
            data_type="string", 
            value="analyst", 
            description="Analyst role"
        )
        db.add(analyst_role)
        db.commit()
        
        analyst.attributes.append(analyst_role)
        analyst.attributes.append(dept_it)
        
        # Create viewer role attribute
        viewer_role = Attribute(
            name="role",
            attribute_type="user", 
            data_type="string",
            value="viewer",
            description="Viewer role"
        )
        db.add(viewer_role)
        db.commit()
        
        viewer.attributes.append(viewer_role)
        
        db.commit()
        
        # Create sample policies
        read_action = db.query(Action).filter(Action.name == "read").first()
        create_action = db.query(Action).filter(Action.name == "create").first()
        admin_action = db.query(Action).filter(Action.name == "admin").first()
        
        policies_data = [
            {
                "name": "Admin Full Access",
                "description": "Administrators have full access to all resources",
                "effect": "ALLOW",
                "priority": 100,
                "conditions": {
                    "equals": {
                        "attribute": "user.role",
                        "value": "admin"
                    }
                },
                "action_id": None,  # Applies to all actions
            },
            {
                "name": "Analyst Read Access",
                "description": "Analysts can read most resources",
                "effect": "ALLOW", 
                "priority": 50,
                "conditions": {
                    "and": [
                        {
                            "equals": {
                                "attribute": "user.role",
                                "value": "analyst"
                            }
                        },
                        {
                            "in": {
                                "attribute": "action.action_name",
                                "values": ["read", "update"]
                            }
                        }
                    ]
                },
                "action_id": None,
            },
            {
                "name": "Viewer Read Only",
                "description": "Viewers can only read public resources",
                "effect": "ALLOW",
                "priority": 25,
                "conditions": {
                    "and": [
                        {
                            "equals": {
                                "attribute": "user.role", 
                                "value": "viewer"
                            }
                        },
                        {
                            "equals": {
                                "attribute": "action.action_name",
                                "value": "read"
                            }
                        }
                    ]
                },
                "action_id": read_action.id if read_action else None,
            },
            {
                "name": "Deny Admin Actions for Non-Admins",
                "description": "Only admins can perform administrative actions",
                "effect": "DENY",
                "priority": 75,
                "conditions": {
                    "and": [
                        {
                            "not": {
                                "equals": {
                                    "attribute": "user.role",
                                    "value": "admin"
                                }
                            }
                        },
                        {
                            "equals": {
                                "attribute": "action.action_name",
                                "value": "admin"
                            }
                        }
                    ]
                },
                "action_id": admin_action.id if admin_action else None,
            }
        ]
        
        for policy_data in policies_data:
            if not db.query(Policy).filter(Policy.name == policy_data["name"]).first():
                policy = Policy(**policy_data)
                db.add(policy)
        
        db.commit()
        
        print("✅ Sample data initialized successfully!")
        print("\nSample users created:")
        print("- admin@fastset.com / admin123 (Full access)")
        print("- analyst@fastset.com / analyst123 (Read/Update access)")
        print("- viewer@fastset.com / viewer123 (Read-only access)")
        print("\nYou can now test the ABAC system with these users.")
        
    except Exception as e:
        print(f"❌ Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_sample_data()