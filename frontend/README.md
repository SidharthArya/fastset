# FastSet BI Platform - Frontend

The frontend workspace provides the web interface and user experience layer for the FastSet BI Platform.

## Features

- Modern web interface built with FastAPI and Jinja2 templates
- Responsive design for desktop and mobile devices
- Interactive dashboards and data visualizations
- User authentication and authorization
- Real-time data updates

## Technology Stack

- **FastAPI** - Modern web framework for building APIs
- **Jinja2** - Template engine for HTML rendering
- **Uvicorn** - ASGI server for running the application
- **Python 3.8+** - Programming language

## Development Setup

### Prerequisites

- Python 3.8+
- uv package manager

### Installation

From the frontend directory:

```bash
cd frontend
uv sync
```

### Running the Development Server

```bash
uv run uvicorn src.fastset_frontend.main:app --reload --port 8080
```

The frontend will be available at `http://localhost:8080`

### Project Structure

```
frontend/
├── src/
│   └── fastset_frontend/
│       ├── __init__.py
│       ├── main.py          # FastAPI application
│       ├── routers/         # API route handlers
│       ├── templates/       # Jinja2 HTML templates
│       ├── static/          # CSS, JS, images
│       └── models/          # Data models
├── tests/                   # Test files
├── dist/                    # Build output
├── pyproject.toml          # Dependencies and configuration
└── README.md               # This file
```

## API Endpoints

- `GET /` - Main dashboard
- `GET /health` - Health check endpoint
- `GET /api/data` - Data API endpoints
- `GET /static/*` - Static file serving

## Testing

Run the test suite:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src/fastset_frontend
```

## Building

Build the frontend for production:

```bash
uv build
```

The build output will be in the `dist/` directory.

## Configuration

Environment variables:

- `BACKEND_URL` - URL of the backend API (default: http://localhost:8000)
- `DEBUG` - Enable debug mode (default: False)
- `SECRET_KEY` - Secret key for session management

## Contributing

See the main project README for contribution guidelines.