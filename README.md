# FastSet BI Platform

Not usable yet - development in progress

A modern Business Intelligence platform built with Python, featuring a clean separation between frontend and backend services using uv workspaces.
![Login Screen](/images/login.png)


## Architecture

This project uses a monorepo structure with two main workspaces:

- **Frontend** - Web interface and user experience layer
- **Backend** - API services, data processing, and business logic

## Quick Start

### Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastset-bi-platform
```

2. Install dependencies for all workspaces:
```bash
uv sync
```

3. Start the development environment:
```bash
# Terminal 1 - Backend
cd backend
uv run uvicorn src.fastset_backend.main:app --reload --port 8000

# Terminal 2 - Frontend  
cd frontend
uv run uvicorn src.fastset_frontend.main:app --reload --port 8080
```

## Workspace Structure

```
fastset-bi-platform/
├── pyproject.toml          # Root workspace configuration
├── frontend/               # Frontend workspace
│   ├── pyproject.toml     # Frontend dependencies & config
│   ├── src/               # Frontend source code
│   └── dist/              # Frontend build output
├── backend/                # Backend workspace
│   ├── pyproject.toml     # Backend dependencies & config
│   ├── src/               # Backend source code
│   └── dist/              # Backend build output
└── README.md              # This file
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run frontend tests only
cd frontend && uv run pytest

# Run backend tests only
cd backend && uv run pytest
```

### Building

```bash
# Build all workspaces
uv build

# Build specific workspace
cd frontend && uv build
cd backend && uv build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

[Add your license here]