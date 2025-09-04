# Entity Relationship Diagram

This ERD shows the database schema for the ABAC (Attribute-Based Access Control) system.

```mermaid
erDiagram
    %% Core entities
    users {
        int id PK
        string username UK
        string email UK
        string hashed_password
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    resources {
        int id PK
        string name
        string resource_type
        string resource_uri
        int parent_id FK
        json metadata
        datetime created_at
    }

    actions {
        int id PK
        string name UK
        string description
        string category
    }

    attributes {
        int id PK
        string name
        string attribute_type
        string data_type
        text value
        string description
        boolean is_active
        datetime created_at
    }

    policies {
        int id PK
        string name
        string description
        string effect
        int priority
        json conditions
        int action_id FK
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    user_sessions {
        int id PK
        int user_id FK
        string session_token UK
        string refresh_token UK
        datetime expires_at
        datetime created_at
        boolean is_active
        json context
    }

    audit_logs {
        int id PK
        int user_id FK
        int resource_id FK
        int action_id FK
        string decision
        int policy_id FK
        json context
        datetime timestamp
        text details
    }

    %% Junction tables for many-to-many relationships
    user_attributes {
        int user_id FK
        int attribute_id FK
    }

    resource_attributes {
        int resource_id FK
        int attribute_id FK
    }

    %% Relationships
    users ||--o{ user_sessions : "has"
    users ||--o{ user_attributes : "has"
    users ||--o{ audit_logs : "performs"

    resources ||--o{ resource_attributes : "has"
    resources ||--o{ resources : "parent_child"
    resources ||--o{ audit_logs : "accessed"

    actions ||--o{ policies : "governs"
    actions ||--o{ audit_logs : "performed"

    attributes ||--o{ user_attributes : "assigned_to"
    attributes ||--o{ resource_attributes : "assigned_to"

    policies ||--o{ audit_logs : "applied"

    %% Attribute types and data types (enums)
    AttributeType {
        string USER
        string RESOURCE
        string ACTION
        string ENVIRONMENT
    }

    DataType {
        string STRING
        string INTEGER
        string BOOLEAN
        string DATETIME
        string LIST
        string JSON
    }

    PolicyEffect {
        string ALLOW
        string DENY
    }
```

## Key Relationships

### Core ABAC Components
- **Users**: Identity entities with attributes
- **Resources**: Protected objects with hierarchical structure
- **Actions**: Operations that can be performed
- **Attributes**: Flexible key-value pairs for all entities
- **Policies**: Rules that define access control logic

### Many-to-Many Relationships
- Users ↔ Attributes (via user_attributes junction table)
- Resources ↔ Attributes (via resource_attributes junction table)

### One-to-Many Relationships
- Users → UserSessions (authentication tracking)
- Actions → Policies (action-specific policies)
- Resources → Resources (hierarchical resources)

### Audit Trail
- All access decisions are logged in audit_logs with references to:
  - User making the request
  - Resource being accessed
  - Action being performed
  - Policy that was applied
  - Decision context and result

## Attribute System
The flexible attribute system allows for:
- **User attributes**: roles, departments, clearance levels
- **Resource attributes**: classification, owner, sensitivity
- **Action attributes**: operation type, risk level
- **Environment attributes**: time, location, network context

## Policy Engine
Policies contain JSON conditions that are evaluated against the attribute context to make ALLOW/DENY decisions with configurable priority levels.