from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

# We import 'Base' from app.db.base_class
# (I will provide base_class.py below to ensure you have the parent class)
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # ---------------------------------------------------------
    # RELATIONSHIPS (The "Foreign Keys")
    # ---------------------------------------------------------
    # This connects the User to their Cheating Logs.
    # 'cascade="all, delete-orphan"' means if you delete a user,
    # their cheating logs are also deleted (Cleanup).
    violations = relationship("IntegrityViolation", back_populates="student", cascade="all, delete-orphan")