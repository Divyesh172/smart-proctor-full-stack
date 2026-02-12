from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

# We import 'Base' from app.db.base_class
# This class automatically handles __tablename__ generation
from app.db.base_class import Base

class User(Base):
    """
    Represents a registered user (Student, Proctor, or Admin) in the system.
    """
    # ---------------------------------------------------------
    # COLUMNS
    # ---------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # Indexed for faster search in the Admin Dashboard
    full_name = Column(String, index=True)

    # Unique Index is CRITICAL here. It prevents two users from
    # registering with the same email at the database level.
    email = Column(String, unique=True, index=True, nullable=False)

    # We never store plain passwords. This holds the BCrypt hash.
    hashed_password = Column(String, nullable=False)

    # Soft Delete / Ban flags
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # ---------------------------------------------------------
    # RELATIONSHIPS
    # ---------------------------------------------------------
    # This connects the User to their Integrity Logs.
    # 'cascade="all, delete-orphan"' means if you delete a user,
    # all their violations are automatically deleted by SQLAlchemy.
    # This keeps your database clean.
    violations = relationship(
        "IntegrityViolation",
        back_populates="student",
        cascade="all, delete-orphan"
    )