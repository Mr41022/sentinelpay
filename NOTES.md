# SentinelPay — Learning Journal

## Architecture
- Domain-driven layering: api/ -> domain/ <- infrastructure/, imports only flow inward
- Three representations of one concept: schema (HTTP), domain (logic), ORM (database row)

## Python / async
- Decimal not float for money
- frozen dataclasses for audit-trail immutability
- async/await lets one process serve many concurrent requests during I/O waits
- connection pooling avoids reopening a DB connection per request

## Testing
- AAA pattern: Arrange, Act, Assert
- testcontainers boots a real disposable Postgres for integration tests
- dependency_overrides swaps real DB for test DB without touching route code

## Docker
- multi-stage build keeps the final image small
- non-root user is a security baseline
- HEALTHCHECK lets orchestrators know the container actually works

## CI/CD
- CI runs lint + tests on every push, on a clean machine
- service containers in GitHub Actions give CI a real Postgres
- needs: sequences jobs so broken code never reaches a Docker build

## Deployment
- managed Postgres URLs need a driver prefix swap (postgresql:// -> postgresql+asyncpg://)
- disable /docs in production — it leaks your schema
- environment variables drive config differences, never hardcoded branches
