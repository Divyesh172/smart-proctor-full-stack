import logging
import sys
import os

# Ensure we can import 'app'
sys.path.append(os.getcwd())

from app.db.session import SessionLocal
from app import crud, schemas
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
    db = SessionLocal()

    # In production, use environment variables!
    # Fallback to "admin@verifai.com" if not set (only for first deploy convenience)
    superuser_email = os.getenv("FIRST_SUPERUSER", "admin@verifai.com")
    superuser_pass = os.getenv("FIRST_SUPERUSER_PASSWORD", "adminpassword123")

    user = crud.user.get_by_email(db, email=superuser_email)
    if not user:
        user_in = schemas.UserCreate(
            email=superuser_email,
            password=superuser_pass,
            full_name="System Administrator",
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info(f"Superuser created: {superuser_email}")
    else:
        logger.info("Superuser already exists. Skipping.")

    db.close()

if __name__ == "__main__":
    logger.info("Creating initial data...")
    init()
    logger.info("Initial data created.")