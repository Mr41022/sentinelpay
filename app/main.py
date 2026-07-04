import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as transactions_router

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(
    title="SentinelPay",
    description="Real-time fraud detection API",
    version="0.1.0",
    docs_url="/docs" if ENVIRONMENT != "production" else None,
    redoc_url=None,
)

# CORS
allow_origins = (
    ["https://your-frontend-domain.com"]
    if ENVIRONMENT == "production"
    else ["http://localhost:3000"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Static + templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

app.include_router(transactions_router)


@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard.html", {"request": request})


@app.get("/health")
async def health_check():
    return {"status": "ok"}  # CI-safe