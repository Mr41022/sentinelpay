import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router as transactions_router

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(
    title="SentinelPay",
    description="Real-time fraud detection API",
    version="0.1.0",
    docs_url="/docs" if ENVIRONMENT != "production" else None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"] if ENVIRONMENT == "production"
                  else ["http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(transactions_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
