import logging
import re
from typing import Optional
from app.core.config import settings

# Configure module-level logger
logger = logging.getLogger(__name__)

class HoneypotService:
    """
    Service responsible for detecting non-human actors and AI interference.
    """

    @staticmethod
    def verify_honeypot_field(hidden_field_value: Optional[str]) -> bool:
        """
        Checks if the 'invisible' CSS-hidden form field was filled out.
        
        Args:
            hidden_field_value: The raw string from the 'phone_extension_secondary' field.
            
        Returns:
            True if bot detected (field has content), False if clean.
        """
        # If the field is None, it might mean the frontend didn't send it.
        # We treat None as 'Safe' (human didn't see it), but empty string "" is also safe.
        # Any other content implies a bot filled it.
        if hidden_field_value and len(hidden_field_value.strip()) > 0:
            logger.warning(f"SECURITY EVENT: Honeypot field triggered. Value: '{hidden_field_value}'")
            return True
        return False

    @staticmethod
    def check_llm_poisoning(answer_text: str) -> bool:
        """
        Scans the answer for the specific trigger word injected into the 
        student's question prompt (e.g., 'Cyberdyne', 'Project 2501').
        
        This detects if the student copied the invisible prompt text 
        and pasted it into ChatGPT.
        """
        if not answer_text:
            return False

        trap_word = settings.HONEYPOT_TRAP_WORD.lower()
        if trap_word in answer_text.lower():
            logger.warning(f"SECURITY EVENT: AI Poisoning detected. Found trap word: '{trap_word}'")
            return True

        return False

    @staticmethod
    def detect_watermark(text: str) -> Optional[int]:
        """
        Advanced: Scans for Zero-Width Characters (\u200B) to detect
        if the text contains a hidden binary watermark.
        
        Used to track which student leaked the question.
        """
        # In a full implementation, you would decode the binary sequence 
        # of zero-width spaces back into an Integer ID.
        # For now, we detect the presence of the marker.
        if "\u200B" in text:
            logger.info("Watermark detected in submission text.")
            return True
        return False

# Instantiate for easy import
honeypot_service = HoneypotService()