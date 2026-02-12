from fastapi import APIRouter
from app.api import auth, exam, users, admin

# ---------------------------------------------------------
# CENTRAL API ROUTER (The "Main Switch")
# ---------------------------------------------------------
api_router = APIRouter()

# ---------------------------------------------------------
# 1. PUBLIC ROUTES (No Auth Required)
# ---------------------------------------------------------
# Authentication logic (Login, Refresh Token, Password Reset)
# These must be public so users can actually get into the system.
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# ---------------------------------------------------------
# 2. PROTECTED ROUTES (Student/User Access)
# ---------------------------------------------------------
# User Profile Management (Get current user, Update settings)
# Separation of concerns: 'Auth' handles tokens, 'Users' handles profile data.
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["User Management"]
)

# Exam Proctoring Engine (Submit, Heartbeat, Sync)
# This is the core business logic.
api_router.include_router(
    exam.router,
    prefix="/exam",
    tags=["Proctoring Engine"]
)

# ---------------------------------------------------------
# 3. ADMINISTRATIVE ROUTES (Staff Only)
# ---------------------------------------------------------
# Dashboard Analytics, Integrity Violation Logs, Ban Management.
# In main.py, we will attach a specific 'AdminDependency' to this entire router
# to ensure no student can ever access these endpoints.
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["System Administration"]
)

# ---------------------------------------------------------
# 4. SYSTEM UTILITIES
# ---------------------------------------------------------
# Health checks for Kubernetes/Docker orchestrators.
# Useful for load balancers to know if the pod is alive.
@api_router.get("/health", tags=["System Status"])
async def health_check():
    return {"status": "operational", "version": "1.0.0", "environment": "production"}