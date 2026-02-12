import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import api_router

# Setup standard Python logging
# In production, this pipes logs to your container's stdout, 
# which tools like Datadog or CloudWatch can pick up.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# LIFESPAN MANAGER (Startup & Shutdown)
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    The Life Cycle of the application.
    Code before 'yield' runs on startup.
    Code after 'yield' runs on shutdown.
    """
    # STARTUP LOGIC
    logger.info(f"🚀 Starting {settings.PROJECT_NAME}...")
    logger.info(f"🌍 Environment: Production")
    logger.info(f"🔗 Go Bouncer URL: {settings.GO_BOUNCER_URL}")

    # Optional: You could check Redis or DB connection health here
    # to fail fast if infrastructure is missing.

    yield  # The application serves requests here

    # SHUTDOWN LOGIC
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}...")
    # Clean up resources (e.g., close HTTP client sessions) if needed.

# ---------------------------------------------------------
# APP INITIALIZATION
# ---------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Enterprise Identity Verification & Proctoring API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc UI
    lifespan=lifespan,
)

# ---------------------------------------------------------
# SECURITY: CORS MIDDLEWARE
# ---------------------------------------------------------
# This allows your Next.js frontend (running on Vercel/Localhost)
# to communicate with this backend.
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ---------------------------------------------------------
# ROUTING
# ---------------------------------------------------------
# We mount the central API router under /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)

# ---------------------------------------------------------
# HEALTH CHECK (Root Endpoint)
# ---------------------------------------------------------
@app.get("/", tags=["System Status"])
def health_check():
    """
    Simple heartbeat endpoint for load balancers (AWS ALB / Nginx).
    """
    return {
        "status": "operational",
        "service": "verifai-backend",
        "version": "1.0.0",
        "documentation": "/docs"
    }

# For debugging in VS Code directly (Optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)