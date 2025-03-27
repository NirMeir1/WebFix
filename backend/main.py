from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from backend.schemas import UrlRequest, UrlResponse
from backend.gpt_service import ChatGPTService
from backend.cache import (
    initialize_caches,
    get_cached_response,
    save_response,
    is_recent_response,
    is_basic_cached,
)
from backend.email_service import send_verification_email, generate_verification_code, verify_email_token, send_report_to_user
from dotenv import load_dotenv
from logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI(on_startup=[initialize_caches])


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Backend is running"}


@app.post("/analyze-url", response_model=UrlResponse)
async def analyze_url(request: UrlRequest, background_tasks: BackgroundTasks):
    # Validate that industry and report_type are correct
    logger.info(f"Processing URL request: {request.url}")

    # URL normalization and cache check
    if is_recent_response(request.url, request.report_type):
        output = get_cached_response(request.url, request.report_type)
        logger.info(f"Returning cached response for {request.url} (Type: {request.report_type})")
        return UrlResponse(output=output, message="Type A: Cached response")

    # Email verification for "deep" report
    if request.report_type == "deep":
        if not request.email:
            logger.warning("Email required but not provided for deep report")
            raise HTTPException(status_code=400, detail="Email required for deep reports")
        
        # Send verification email if not verified yet
        # Assuming 'verify_email_token' will return False if the email isn't verified yet
        token = generate_verification_code(request.email)  # Generate a unique token
        background_tasks.add_task(send_verification_email(request.email, token))
        logger.info(f"Email verification initiated for {request.email}")

    # Generate GPT response
    gpt = ChatGPTService()
    output = await gpt.generate_response(request.url, request.report_type, request.industry, request.email)
    logger.info(f"GPT response generated for URL: {request.url}")

    # Save to appropriate cache
    save_response(request.url, request.report_type, output)

    message_type = "Type Z: New URL request" if request.report_type == "basic" else "Type B: Deep report generated"

    return UrlResponse(output=output, message=message_type)


@app.get("/verify-email")
def email_verification(email: str, token: str):
    """
    Endpoint to verify email by the token sent via the verification email.
    """
    if verify_email_token(email, token):
        logger.info(f"Email successfully verified: {email}")
        return {"message": "Email successfully verified."}
    else:
        logger.error(f"Invalid verification attempt for email: {email}")
        raise HTTPException(status_code=400, detail="Invalid or expired verification token.")