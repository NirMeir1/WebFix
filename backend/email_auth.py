import uuid
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

email_tokens: Dict[str, str] = {}
verified_emails: Set[str] = set()

def send_verification_email(email: str, url: str):
    token = str(uuid.uuid4())
    email_tokens[email] = token
    verification_link = f"http://yourdomain.com/verify-email?email={email}&token={token}"
    logger.info(f"Verification email sent to {email}. Verification link: {verification_link}")
    # Integrate actual email sending logic here.

def verify_email(email: str, token: str) -> bool:
    if email_tokens.get(email) == token:
        verified_emails.add(email)
        del email_tokens[email]
        logger.info(f"Email verified: {email}")
        return True
    logger.warning(f"Failed email verification attempt: {email}")
    return False

def is_email_verified(email: str) -> bool:
    verified = email in verified_emails
    logger.info(f"Email verification status checked for {email}: {verified}")
    return verified