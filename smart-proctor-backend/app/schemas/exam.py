from typing import Optional, List
from pydantic import BaseModel, Field, conlist

# ---------------------------------------------------------
# 1. Input Schema: What the Frontend sends us
# ---------------------------------------------------------
class ExamSubmission(BaseModel):
    # Core Data
    student_id: str = Field(..., description="The unique ID of the student taking the exam.")
    exam_id: str = Field(..., description="The unique ID of the exam session.")
    question_id: str = Field(..., description="Which question is being answered.")

    # The Answer
    answer_text: str = Field(..., min_length=1, description="The actual text submitted by the student.")

    # --- SECURITY LAYER 1: BEHAVIORAL BIOMETRICS ---
    # We expect a list of flight times (milliseconds between key presses).
    # If this list is empty or uniform (e.g., all 0s), it's a copy-paste.
    keystroke_fingerprint: List[float] = Field(
        default_factory=list,
        description="Array of flight-times between keystrokes for identity verification."
    )

    # --- SECURITY LAYER 2: SPEED TRAP ---
    # Time spent on this specific question.
    time_taken_seconds: int = Field(..., gt=0, description="Time spent on the question page.")

    # --- SECURITY LAYER 3: HONEYPOT (The Trap) ---
    # In the HTML/JSON, this field is named 'phone_extension_secondary'.
    # If a bot fills it, 'hp_check' will have a value, triggering a ban.
    hp_check: Optional[str] = Field(
        None,
        validation_alias="phone_extension_secondary",
        description="Hidden field for bot detection. MUST BE EMPTY."
    )

    class Config:
        # Pydantic V2 config to allow population by alias
        populate_by_name = True

# ---------------------------------------------------------
# 2. Output Schema: What we send back
# ---------------------------------------------------------
class ExamResult(BaseModel):
    student_id: str
    exam_id: str
    status: str = Field(..., pattern="^(PASSED|FLAGGED|REVIEW_REQUIRED)$")

    # If flagged, we return the specific reason (e.g., "Bot Detected")
    # If passed, this might be null or a generic success message.
    security_remarks: Optional[str] = None

    # Mock score for immediate feedback (optional)
    preliminary_score: Optional[int] = 0