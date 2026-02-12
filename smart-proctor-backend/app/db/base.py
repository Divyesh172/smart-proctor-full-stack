# Import the declarative base
from app.db.base_class import Base

# Import all models here so Alembic can detect them
from app.models.user import User
from app.models.integrity import IntegrityViolation