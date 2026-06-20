
## SentinelPay
Banks lose over $40 billion a year to payment fraud globally. Every bank has fraud detection, but almost all of it is either a rigid rules engine ("flag any transaction over £500 abroad") or a black-box vendor model they can't explain. The gap nobody has filled well is: a transparent, real-time system that explains why it flagged a transaction, adapts to new fraud patterns without retraining, and is observable enough that an ops team can actually trust and debug it.
A real-time fraud detection API built with **FastAPI**, **SQLAlchemy**, and **async PostgreSQL**.


## Quick Start

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- uv (Python package manager)

---

## Local Development

### 1. Install dependencies
```bash
uv sync
````

---

### 2. Start PostgreSQL

```bash
docker-compose up -d postgres
```

---

### 3. Run database migrations

```bash
uv run alembic upgrade head
```

---

### 4. Start development server

```bash
uv run uvicorn app.main:app --reload
```

API docs available at:

```
http://localhost:8000/docs
```
![image](https://github.com/Mr41022/sentinelpay/blob/528d9d59d223986be73db54b50a10acd1f7f3312/Screenshot%202026-06-20%20211111.png)
![image](https://github.com/Mr41022/sentinelpay/blob/528d9d59d223986be73db54b50a10acd1f7f3312/Screenshot%202026-06-20%20211130.png)
![image](https://github.com/Mr41022/sentinelpay/blob/528d9d59d223986be73db54b50a10acd1f7f3312/Screenshot%202026-06-20%20211141.png)
Dashboard UI:

```
http://localhost:8000/
```
![image](https://github.com/Mr41022/sentinelpay/blob/7bc20e5ae0f1cf455618f3f7fdf7d98553afc592/Screenshot%202026-06-20%20211212.png)
![image]https://github.com/Mr41022/sentinelpay/blob/7bc20e5ae0f1cf455618f3f7fdf7d98553afc592/Screenshot%202026-06-20%20211229.png)

---

## Running Tests

### Run all tests

```bash
uv run pytest -v
```

### Run with coverage

```bash
uv run pytest --cov=app --cov-report=term-missing
```

---

## Project Structure

```
app/
├── api/               # HTTP routes & dependencies
├── domain/           # Business logic (fraud scoring)
├── infrastructure/   # Database models & setup
├── schemas/          # Pydantic request/response models
└── main.py           # FastAPI entry point

tests/                # Unit & integration tests
migrations/           # Alembic migrations
```

---

## Architecture

* **Domain-driven design**: business logic isolated in `domain/`
* **Async-first**: FastAPI + async SQLAlchemy for high performance
* **Tested**: unit + integration tests included
* **Containerized**: Docker-ready setup for deployment

---

## Environment Variables

| Variable     | Description                  | Default     |
| ------------ | ---------------------------- | ----------- |
| DATABASE_URL | PostgreSQL connection string | localhost   |
| ENVIRONMENT  | development / production     | development |
| LOG_LEVEL    | Logging level                | INFO        |

---

## API Endpoints

| Method | Endpoint    | Description         |
| ------ | ----------- | ------------------- |
| GET    | `/`         | Dashboard UI        |
| GET    | `/health`   | Health check        |
| POST   | `/api/v1/*` | Fraud detection API |

---

## Example Response

```json
{
  "transaction_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "score": 0.92,
  "decision": "fraud",
  "top_reasons": [
    "high amount",
    "unusual location"
  ],
  "model_version": "v1.0"
}
```

---

## Deployment

Deployed using Docker with CI/CD pipeline.

See `.github/workflows/ci.yml` for build and deployment workflow.

---


