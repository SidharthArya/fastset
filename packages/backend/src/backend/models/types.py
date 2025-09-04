
from enum import Enum 

class AttributeType(str, Enum):
    """Types of attributes in the ABAC system"""
    USER = "user"
    RESOURCE = "resource" 
    ACTION = "action"
    ENVIRONMENT = "environment"

class DataType(str, Enum):
    """Data types for attribute values"""
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    DATETIME = "datetime"
    LIST = "list"
    JSON = "json"