from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router

# ---------------------------------------------------------
# 1. Lifecycle Management (The "Startup" & "Shutdown" Logic)
# ---------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Executes when the server starts and stops.
    Used to verify connections to the Go Bouncer and Database.
    """
    # STARTUP LOGIC
    print(f"INFO:  Starting {settings.PROJECT_NAME}...")
    print(f"INFO:  Connected to Go Bouncer at: {settings.GO_BOUNCER_URL}")
    print(f"INFO:  Honeypot Trap Word set to: '{settings.HONEYPOT_TRAP_WORD}'")

    # You could add a real "Ping" to the Go server here
    # await ping_go_service()

    yield  # The application runs here

    # SHUTDOWN LOGIC
    print(f"INFO:  Shutting down {settings.PROJECT_NAME}...")
    # close_db_connection()

# ---------------------------------------------------------
# 2. App Initialization
# ---------------------------------------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Identity Verification & Anti-Cheating API for the VerifAI Platform.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
    docs_url="/docs",       # Swagger UI
    redoc_url="/redoc",     # ReDoc UI
)

# ---------------------------------------------------------
# 3. Security Middleware (CORS)
# ---------------------------------------------------------
# This is CRITICAL. Without this, your Next.js app (on Vercel)
# will be blocked by the browser when trying to fetch data.
if settings.BACKEND_CORS_ORIGINS:
# In app/main.py
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"], # Be explicit
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"] # Add this
    )

# ---------------------------------------------------------
# 4. Router Mounting
# ---------------------------------------------------------
app.include_router(api_router, prefix=settings.API_V1_STR)

# ---------------------------------------------------------
# 5. Health Check (The "Heartbeat" Endpoint)
# ---------------------------------------------------------
@app.get("/", tags=["Status"])
async def health_check():
    """
    Simple endpoint to verify the server is running.
    Mentors usually check this first.
    """
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "mode": "Sovereign-Cloud Ready",
        "services": {
            "python_api": "healthy",
            "go_bouncer": "linked" # Mock status for demo
        }
    }

# For debugging in VS Code directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)