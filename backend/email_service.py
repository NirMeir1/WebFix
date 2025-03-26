import os
import boto3
import logging
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import uuid

load_dotenv()

logger = logging.getLogger(__name__)

# Load AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

# Initialize SES client
ses_client = boto3.client(
    'ses',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION
)

# A dictionary to store email-verification code mapping (simplified for example purposes)
# In a production environment, you should use a database or more persistent storage.
email_tokens = {}

def send_verification_email(email: str, verification_code: str):
    """
    Send the verification email containing the verification code.
    """
    subject = "Verify your email address"
    body_text = f"Hello,\n\nPlease verify your email by using the code: {verification_code}\n"
    
    from_email = "meirnir89@gmail.com"  # Replace with your verified SES email
    #in the future it will be - bottomline-ai.com(email)

    # Prepare the email content
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        # Send the email using SES
        response = ses_client.send_raw_email(
            Source=from_email,
            Destinations=[email],
            RawMessage={'Data': msg.as_string()},
        )
        logger.info(f"Verification email sent to {email}. Message ID: {response['MessageId']}")
    except ClientError as e:
        logger.error(f"Error sending verification email to {email}: {e}")
        return None
    return True

def generate_verification_code(email: str):
    """
    Generate a unique verification code (token) and store it in email_tokens dictionary.
    """
    token = str(uuid.uuid4())  # Generates a unique UUID as the verification code
    email_tokens[email] = token  # Store the token with email as key
    return token

def verify_email_token(email: str, token: str) -> bool:
    """
    Verify the email address using the token provided by the user.
    """
    stored_token = email_tokens.get(email)  # Retrieve the stored token for the email
    if stored_token == token:
        logger.info(f"Email verified: {email}")
        # After successful verification, remove the token to prevent re-use
        del email_tokens[email]
        return True
    else:
        logger.warning(f"Failed email verification attempt: {email}")
        return False

def send_report_to_user(email: str, report_content: str):
    """
    Send the product report to the user after successful email verification.
    """
    subject = "Your Product Report"
    body_text = f"Hello,\n\nPlease find your requested product report below:\n\n{report_content}"
    
    from_email = "meirnir89@gmail.com"  # Replace with your verified SES email

    # Prepare the email content
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain'))

    try:
        # Send the report using SES
        response = ses_client.send_raw_email(
            Source=from_email,
            Destinations=[email],
            RawMessage={'Data': msg.as_string()},
        )
        logger.info(f"Product report sent to {email}. Message ID: {response['MessageId']}")
    except ClientError as e:
        logger.error(f"Error sending product report to {email}: {e}")
        return None
    return True