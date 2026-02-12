from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class IntegrityViolation(Base):
    """
    Immutable log of a detected integrity event.
    Once written, these rows should ideally never be updated, only read.
    """
    __tablename__ = "integrity_violations"

    id = Column(Integer, primary_key=True, index=True)

    # ---------------------------------------------------------
    # FOREIGN KEYS
    # ---------------------------------------------------------
    # Links to the 'users' table.
    # nullable=False: A violation MUST belong to a student.
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # ---------------------------------------------------------
    # METADATA
    # ---------------------------------------------------------
    # Enum-like string: "BOT_DETECTED", "AI_PLAGIARISM", "TAB_SWITCH"
    # Indexed so we can quickly count "How many bots today?"
    violation_type = Column(String, index=True, nullable=False)

    # Confidence score (0.0 to 1.0) or Time Deviation (ms)
    evidence_score = Column(Float, nullable=True)

    # JSON Blob or Detailed text explaining the violation.
    # We use Text (instead of String) to allow unlimited length logs.
    metadata_log = Column(Text, nullable=True)

    # ---------------------------------------------------------
    # TIMESTAMPS
    # ---------------------------------------------------------
    # 'server_default=func.now()' ensures the DB sets the time
    # precisely when the row is inserted.
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # ---------------------------------------------------------
    # RELATIONSHIPS
    # ---------------------------------------------------------
    student = relationship("User", back_populates="violations")