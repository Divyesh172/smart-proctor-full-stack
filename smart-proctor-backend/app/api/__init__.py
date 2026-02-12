from fastapi import APIRouter
from app.api import auth, exam, users, admin

api_router = APIRouter()

# 1. AUTHENTICATION (Public)
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

# 2. USER MANAGEMENT (Protected)
api_router.include_router(users.router, prefix="/users", tags=["User Management"])

# 3. EXAM PROCTORING (Protected + High Integrity)
api_router.include_router(exam.router, prefix="/exam", tags=["Proctoring Engine"])

# 4. ADMINISTRATION (Superuser Only)
api_router.include_router(admin.router, prefix="/admin", tags=["System Administration"])

# 5. SYSTEM HEALTH
@api_router.get("/health", tags=["System"])
def health_check():
    return {"status": "operational", "mode": "production"}