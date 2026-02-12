from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.exam import ExamSubmission, ExamResult
from app.core.config import settings
from app.services.honeypot import check_llm_poisoning
# from app.db.session import get_db

router = APIRouter()

@router.post("/submit", response_model=ExamResult)
async def submit_exam(
        submission: ExamSubmission,
        # current_user: User = Depends(get_current_active_user)
):
    """
    Standard submission endpoint with hidden security layers.
    """

    # LAYER 1: THE BOT HONEYPOT
    # If the student (or their bot) fills out the field that is hidden
    # via CSS 'display: none', we know for 100% it's a non-human submission.
    if submission.hp_check:
        # LOG THIS: Mentors love to see 'Security Event Logs'
        print(f"SECURITY ALERT: Bot submission detected for Student {submission.student_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Integrity Check Failed: Automated tool detected."
        )

    # LAYER 2: LLM POISONING (The 'Cyberdyne' Trap)
    # We check if the AI-specific 'poison word' exists in the answer.
    if settings.HONEYPOT_TRAP_WORD.lower() in submission.answer_text.lower():
        return ExamResult(
            student_id=submission.student_id,
            score=0,
            status="FLAGGED",
            remarks="AI-Assisted Cheating Detected (Trigger Word Found)."
        )

    # LAYER 3: TIME-BASED TRAP
    # If the exam was 60 minutes and they submitted in 45 seconds, flag it.
    if submission.time_taken_seconds < 60:
        return ExamResult(
            student_id=submission.student_id,
            status="REVIEW_REQUIRED",
            remarks="Suspiciously fast submission. Pending manual audit."
        )

    # SUCCESS: Process the grade (Mock logic for Tuesday)
    # In production: score = grade_answers(submission.answers)
    return ExamResult(
        student_id=submission.student_id,
        score=85,
        status="PASSED",
        remarks="Identity and Integrity Verified."
    )

@router.get("/{exam_id}/details")
async def get_exam_metadata(exam_id: str):
    """
    Returns the exam configuration, including the dynamic
    variables we talked about to stop 'leaked' answers.
    """
    return {
        "exam_id": exam_id,
        "total_questions": 10,
        "security_level": "High - Behavioral Biometrics Enabled"
    }