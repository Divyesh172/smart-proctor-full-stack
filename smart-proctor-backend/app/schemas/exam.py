from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

# ---------------------------------------------------------
# EXAM SUBMISSION (Input)
# ---------------------------------------------------------
class ExamSubmission(BaseModel):
    student_id: int
    exam_id: str
    question_id: str
    answer_text: str = Field(..., min_length=1, description="The student's answer")
    time_taken_seconds: int = Field(..., ge=0)

    # SECURITY: HONEYPOT FIELD
    # The frontend sends 'phone_extension_secondary' (hidden via CSS).
    # We map it to 'hp_check' internally.
    # If this field has ANY value, it's a bot.
    hp_check: Optional[str] = Field(
        None,
        validation_alias="phone_extension_secondary"
    )

    model_config = ConfigDict(populate_by_name=True)

# ---------------------------------------------------------
# INTEGRITY LOGS (Admin Dashboard)
# ---------------------------------------------------------
class IntegrityBase(BaseModel):
    violation_type: str
    evidence_score: float
    metadata_log: Optional[str] = None

class IntegrityCreate(IntegrityBase):
    student_id: int

class IntegrityUpdate(IntegrityBase):
    pass

class IntegrityLog(IntegrityBase):
    id: int
    student_id: int
    # Timestamps are handled by the DB, but useful to return to admin
    # We let Pydantic handle the datetime serialization automatically

    model_config = ConfigDict(from_attributes=True)

# ---------------------------------------------------------
# EXAM RESULT (Output)
# ---------------------------------------------------------
class ExamResult(BaseModel):
    student_id: int
    exam_id: str
    status: str = Field(..., description="PASSED, FLAGGED, or REVIEW_REQUIRED")
    score: Optional[int] = 0
    security_remarks: Optional[str] = None