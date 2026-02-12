# app/services/honeypot.py
import re
from typing import Optional, List
from app.core.config import settings

def verify_honeypot(hidden_field_value: Optional[str]) -> bool:
    """
    Checks if the 'invisible' form field was filled out.

    Args:
        hidden_field_value: The value from the 'phone_extension_secondary' field.

    Returns:
        True if bot detected (field has content), False if clean.
    """
    # If the field has ANY content, it's a bot.
    # Humans can't see this field because of CSS 'display: none'.
    if hidden_field_value and len(hidden_field_value.strip()) > 0:
        return True
    return False

def check_llm_poisoning(answer_text: str) -> bool:
    """
    Scans the answer for the specific trigger word we injected
    into the prompt (e.g., 'Cyberdyne').

    Returns:
        True if the trigger word is found (Cheating detected).
    """
    if not answer_text:
        return False

    # Case-insensitive check for the trap word
    trap_word = settings.HONEYPOT_TRAP_WORD.lower()
    return trap_word in answer_text.lower()

def check_watermark(question_text: str) -> Optional[int]:
    """
    Advanced: Scans for Zero-Width Characters (\u200B) to detect
    if the question was copied from a specific student's screen.

    Returns:
        Student ID (int) if a watermark is found, None otherwise.
    """
    # This regex looks for a sequence of Zero-Width Spaces
    # In a real app, you'd decode binary from this.
    # For the demo, we just check presence.
    if "\u200B" in question_text:
        # Mock decoding logic
        return 12345
    return None