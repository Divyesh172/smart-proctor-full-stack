from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class IntegrityViolation(Base):
    __tablename__ = "integrity_violations"

    id = Column(Integer, primary_key=True, index=True)

    # ---------------------------------------------------------
    # FOREIGN KEY
    # ---------------------------------------------------------
    # We link this violation to a specific student ID.
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # ---------------------------------------------------------
    # VIOLATION DETAILS
    # ---------------------------------------------------------
    # Type: "BOT_DETECTED", "TAB_SWITCH", "RHYTHM_MISMATCH"
    violation_type = Column(String, index=True, nullable=False)

    # Evidence: A simplified score (e.g., 0.99 confidence) or
    # specific metadata (e.g., "Flight time: 2ms")
    evidence_score = Column(Float, nullable=True)
    metadata_log = Column(String, nullable=True) # JSON string of details

    # Timestamp: When did the crime happen?
    # 'server_default=func.now()' lets the DB set the time automatically.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Reverse relationship to User
    student = relationship("User", back_populates="violations")