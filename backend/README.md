# FastSet BI Platform - Backend

The backend workspace provides API services, data processing, and business logic for the FastSet BI Platform.

## Features

- RESTful API built with FastAPI
- Database management with SQLAlchemy and Alembic
- User authentication and authorization with JWT
- Data processing and analytics capabilities
- Comprehensive API documentation with OpenAPI/Swagger

## Technology Stack

- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Alembic** - Database migration tool
- **Pydantic** - Data validation using Python type annotations
- **python-jose** - JWT token handling
- **Passlib** - Password hashing utilities
- **Uvicorn** - ASGI server for running the application

## Development Setup

### Prerequisites

- Python 3.8+
- uv package manager
- PostgreSQL or SQLite database

### Installation

From the backend directory:

```bash
cd backend
uv sync
```

### Database Setup

1. Create database migrations:
```bash
uv run alembic revision --autogenerate -m "Initial migration"
```

2. Apply migrations:
```bash
uv run alembic upgrade head
```

### Running the Development Server

```bash
uv run uvicorn src.fastset_backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Project Structure

```
backend/
├── src/
│   └── fastset_backend/
│       ├── __init__.py
│       ├── main.py          # FastAPI application
│       ├── api/             # API route handlers
│       ├── core/            # Core functionality
│       ├── db/              # Database models and utilities
│       ├── schemas/         # Pydantic models
│       ├── services/        # Business logic
│       └── utils/           # Utility functions
├── alembic/                 # Database migrations
├── tests/                   # Test files
├── dist/                    # Build output
├── pyproject.toml          # Dependencies and configuration
└── README.md               # This file
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Refresh JWT token

### Data Management
- `GET /api/v1/data` - Retrieve data
- `POST /api/v1/data` - Create new data
- `PUT /api/v1/data/{id}` - Update data
- `DELETE /api/v1/data/{id}` - Delete data

### Analytics
- `GET /api/v1/analytics/dashboard` - Dashboard data
- `GET /api/v1/analytics/reports` - Generate reports
- `POST /api/v1/analytics/query` - Custom data queries

### Health & Monitoring
- `GET /health` - Health check endpoint
- `GET /metrics` - Application metrics

## Testing

Run the test suite:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src/fastset_backend --cov-report=html
```

## Database Migrations

Create a new migration:

```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Rollback migration:

```bash
uv run alembic downgrade -1
```

## Building

Build the backend for production:

```bash
uv build
```

The build output will be in the `dist/` directory.

## Configuration

Environment variables:

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - Secret key for JWT tokens
- `DEBUG` - Enable debug mode (default: False)
- `CORS_ORIGINS` - Allowed CORS origins
- `JWT_EXPIRATION_HOURS` - JWT token expiration time

Example `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/fastset_bi
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=["http://localhost:8080"]
JWT_EXPIRATION_HOURS=24
```

## Contributing

See the main project README for contribution guidelines.