from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.lifespan import lifespan
from backend.database import create_tables
from backend.routers import auth, abac, users
from backend.middleware import AuthMiddleware
from backend.services.auth import SECRET_KEY, ALGORITHM
import os

# Create FastAPI app
app = FastAPI(
    title="FastSet BI Platform",
    description="Fastset Backend APIS",
    version="1.0.0",
    lifespan=lifespan
)

# Add Auth middleware (before CORS)
app.add_middleware(AuthMiddleware, secret_key=SECRET_KEY, algorithm=ALGORITHM)

# Add CORS middleware
cors_origins = os.environ.get("FASTSET_CORS_ORIGINS", "http://localhost:3000,http://localhost:8000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins.split(","),  # Split by comma, not slash
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/v1")
app.include_router(abac.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    create_tables()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "FastSet BI Platform - ABAC Backend",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}