Railway deployment instructions

This project provides a Dockerfile and can be deployed to Railway using either:

1) Railway CLI (recommended):
   - Install Railway CLI: https://railway.app/
   - From project root run:
     railway init
     # when prompted, choose "Deploy from Dockerfile" or create a new project
     railway up --detach
   - Set environment variables in the Railway project settings (see `railway.env.example`).

2) GitHub integration:
   - Connect the repository to Railway from the Railway dashboard and select "Deploy from Dockerfile".
   - Configure the `Dockerfile` path (`./Dockerfile`) and any build args.

Required environment variables (add to Railway project settings):
- `DATABASE_URL` — e.g. `postgresql+asyncpg://sentinel:<password>@<host>:5432/sentinelpay`
- `ENVIRONMENT` — optional, e.g. `production`
- `LOG_LEVEL` — optional, e.g. `info`

Notes:
- The `Dockerfile` in the repository builds a self-contained image and runs Uvicorn.
- Railway offers managed Postgres; if you use Railway's Postgres, set `DATABASE_URL` accordingly.

Example quick deploy using Docker (Railway or other hosts):

```bash
# build locally
docker build -t sentinelpay-api:prod .
# run with a managed postgres
docker run -e DATABASE_URL='postgresql+asyncpg://user:pass@host:5432/sentinelpay' -p 8000:8000 sentinelpay-api:prod
```
