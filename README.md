# SentinelPay

A real-time fraud detection API built with FastAPI, SQLAlchemy, and async PostgreSQL.

## Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- uv (universal Python package manager)

### Local Development

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Start PostgreSQL:**
   ```bash
   docker-compose up -d postgres
   ```

3. **Run migrations:**
   ```bash
   uv run alembic upgrade head
   ```

4. **Start the dev server:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

   API docs: http://localhost:8000/docs

### Running Tests

```bash
# All tests
uv run pytest -v

# With coverage
uv run pytest --cov=app --cov-report=term-missing
```

## Project Structure

```
app/
├── api/          # HTTP routes & dependencies
├── domain/       # Pure business logic (fraud scoring)
├── infrastructure/  # Database & ORM models
├── schemas/      # Pydantic request/response models
└── main.py       # FastAPI app entry point

tests/            # Integration & unit tests
migrations/       # Alembic database migrations
```

## Architecture

- **Domain-Driven**: Business logic isolated in `app/domain/`
- **Async-First**: FastAPI + SQLAlchemy async for concurrent request handling
- **Tested**: Comprehensive unit & integration tests with testcontainers
- **Containerized**: Multi-stage Dockerfile for minimal image size

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection (default: localhost dev DB)
- `ENVIRONMENT` - `development` or `production` (affects CORS, `/docs` visibility)
- `LOG_LEVEL` - Python log level (default: INFO)

## Deployment

Deployed on Railway with automatic Docker builds. See `.github/workflows/ci.yml` for CI pipeline.
