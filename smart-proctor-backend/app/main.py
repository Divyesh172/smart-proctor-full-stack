import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import api_router

# Setup standard Python logging
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

    yield  # The application serves requests here

    # SHUTDOWN LOGIC
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}...")

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
# SECURITY: CORS MIDDLEWARE (THE FIX)
# ---------------------------------------------------------
# We explicitly allow localhost ports to prevent CORS blocking.
origins = [
    "http://localhost:3000",    # Next.js Frontend
    "http://127.0.0.1:3000",    # Alternative Localhost
    "http://localhost:8080",    # Go Bouncer
    "http://127.0.0.1:8080",    # Alternative Bouncer
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
    Simple heartbeat endpoint for load balancers.
    """
    return {
        "status": "operational",
        "service": "verifai-backend",
        "version": "1.0.0",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)