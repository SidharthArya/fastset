from contextlib import asynccontextmanager
from backend.database import create_tables, SessionLocal
from backend.services.auth import AuthService
from backend.schemas.abac import UserCreate

def create_default_user():
    """Create default admin user if it doesn't exist"""
    db = SessionLocal()
    try:
        # Check if admin user exists
        existing_user = AuthService.get_user_by_username(db, "admin")
        if not existing_user:
            # Create default admin user
            admin_user = UserCreate(
                username="admin",
                email="admin@fastset.com",
                password="admin123"
            )
            AuthService.create_user(db, admin_user)
            print("Created default admin user: admin/admin123")
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app):
    create_tables()
    create_default_user()
    yield