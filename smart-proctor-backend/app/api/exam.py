import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas, models
from app.api import deps
from app.core.config import settings
from app.models.integrity import IntegrityViolation

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/submit", response_model=schemas.ExamResult)
def submit_exam(
        submission: schemas.ExamSubmission,
        db: Session = Depends(deps.get_db),
        # Optional: Enable this to force students to be logged in
        # current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Analyzes submission for cheating traces and persists violations to the DB.
    """
    violation_detected = False
    remarks = []

    # 1. HONEYPOT CHECK (Bot Detection)
    if submission.hp_check:
        violation_detected = True
        remarks.append("Automated Tool Detected (Honeypot Triggered)")

        # PERSIST VIOLATION
        # In a real app, you'd use a CRUD method, but direct model access is fine here
        db_log = IntegrityViolation(
            student_id=int(submission.student_id), # Ensure ID matches DB type
            violation_type="BOT_DETECTED",
            evidence_score=1.0,
            metadata_log="Filled hidden field: phone_extension_secondary"
        )
        db.add(db_log)
        db.commit()

    # 2. LLM POISONING CHECK (AI Detection)
    if settings.HONEYPOT_TRAP_WORD.lower() in submission.answer_text.lower():
        violation_detected = True
        remarks.append("AI Generation Detected (Trap Word Found)")

        db_log = IntegrityViolation(
            student_id=int(submission.student_id),
            violation_type="AI_PLAGIARISM",
            evidence_score=0.99,
            metadata_log=f"Found trap word: {settings.HONEYPOT_TRAP_WORD}"
        )
        db.add(db_log)
        db.commit()

    # 3. SPEED CHECK
    if submission.time_taken_seconds < 60:
        remarks.append("Suspiciously Fast Submission")
        # We don't fail immediately, but flag it

    if violation_detected:
        return schemas.ExamResult(
            student_id=submission.student_id,
            exam_id=submission.exam_id,
            status="FLAGGED",
            security_remarks="; ".join(remarks),
            score=0
        )

    return schemas.ExamResult(
        student_id=submission.student_id,
        exam_id=submission.exam_id,
        status="PASSED",
        score=85, # In real app, this would call a Grading Service
        security_remarks="Integrity Verified"
    )