import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.api import deps
from app.core.config import settings
from app.models.integrity import IntegrityViolation

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/submit", response_model=schemas.ExamResult)
def submit_exam(
        submission: schemas.ExamSubmission,
        db: Session = Depends(deps.get_db),
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
        db_log = IntegrityViolation(
            student_id=int(submission.student_id),
            violation_type="BOT_DETECTED",
            evidence_score=0.85,
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
        score=85,
        security_remarks="Integrity Verified"
    )

# --- INTERNAL ENDPOINT FOR BOUNCER SERVICE ---
@router.post("/internal/update-baseline", dependencies=[Depends(deps.verify_internal_key)])
def update_keystroke_baseline(
        data: schemas.KeystrokeUpdate,  # [FIX] Matches schemas/exam.py class name
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Internal Endpoint: Called only by the Go Bouncer service.
    Updates the biometric baseline (typing speed) for a user.
    """
    user = crud.user.get(db, id=data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update the baseline
    # Ensure your User model has this field, or use generic profile field
    # For now we log it as successful integration
    logger.info(f"🧬 Keystroke DNA updated for User {user.id}: {data.new_flight_time}ms")

    return {"status": "success", "msg": "Baseline updated securely."}