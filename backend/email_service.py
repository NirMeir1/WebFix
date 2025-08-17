import jwt
import os
import boto3
import logging
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

logger = logging.getLogger(__name__)

# AWS SES Client initialization
ses_client = boto3.client(
    'ses',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)

JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
FRONTEND_VERIFY_URL = "https://355a-2a00-a040-1a3-aaa3-d991-de87-4dd2-ba77.ngrok-free.app/verify-email"

# Create JWT token
def generate_jwt_token(data: Dict) -> str:
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Decode JWT token
def decode_jwt_token(token: str) -> Dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

# Send Verification Email
def send_verification_email(email: str, jwt_token: str) -> None:
    logger.info("Sending verification email to %s", email)
    verify_link = f"{FRONTEND_VERIFY_URL}?token={jwt_token}"
    subject = "Verify your email address"
    body_text = f"Hello,\n\nPlease verify your email by clicking the following link:\n{verify_link}\n"

    from_email = "meirnir89@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        ses_client.send_raw_email(
            Source=from_email,
            Destinations=[email],
            RawMessage={'Data': msg.as_string()},
        )
        logger.info(f"Verification email sent to {email}")
    except ClientError as e:
        logger.error(f"Error sending verification email: {e}")
        raise

# Send Product Report Email
def send_report_to_user(email: str, report_content: str):
    subject = "Your Product Report"
    body_text = f"Hello,\n\nHere is your product report:\n\n{report_content}"

    from_email = "meirnir89@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        ses_client.send_raw_email(
            Source=from_email,
            Destinations=[email],
            RawMessage={'Data': msg.as_string()},
        )
        logger.info(f"Product report sent to {email}")
    except ClientError as e:
        logger.error(f"Error sending product report: {e}")
        raise
