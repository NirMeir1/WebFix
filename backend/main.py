from fastapi import FastAPI, HTTPException, BackgroundTasks
from backend.schemas import UrlRequest, EmailVerificationRequest, UrlResponse
from backend.gpt_service import ChatGPTService
from backend.cache import (
    initialize_caches,
    get_cached_response,
    save_response,
    is_recent_response
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
        
        save_response(request.url, request.report_type, output)
        logger.info(f"Deep report user data saved for the url: {request.url}")
        
        # Send verification email if not verified yet
        # Assuming 'verify_email_token' will return False if the email isn't verified yet
        token = generate_verification_code(request.email)  # Generate a unique token
        background_tasks.add_task(send_verification_email(request.email, token))
        logger.info(f"Email verification initiated for {request.email}")
        return UrlResponse(output="Email verification sent. Please verify to proceed.", message="Type B: Awaiting verification")

    # Generate GPT response (reuse the helper function)
    try:
        gpt_instance = ChatGPTService()
        output = await gpt_instance.generate_gpt_report(
            request.url,
            request.report_type,
            request.industry,
            request.email
        )
        logger.info(f"GPT response generated for URL: {request.url}")

        # Save to appropriate cache
        save_response(request.url, request.report_type, output)

        message_type = "Type Z: New URL request" if request.report_type == "basic" else "Type B: Deep report generated"
        return UrlResponse(output=output, message=message_type)
    except Exception as e:
        logger.error(f"Error generating GPT response for {request.url}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generating product report.")


@app.post("/verify-email")
async def email_verification(request: EmailVerificationRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to verify email by the token sent via the verification email.
    After successful verification, generate a product report and send it to the user.
    """
    if verify_email_token(request.email, request.token):
        logger.info(f"Email successfully verified: {request.email}")

        # Generate GPT response
        try:
            gpt_instance = ChatGPTService()
            output = await gpt_instance.generate_gpt_report(
                request.url,
                request.report_type,
                request.industry,
                request.email
            )
            logger.info(f"GPT report generated for {request.email}: {output[:100]}...")

            # Send the product report in the background
            report_content = output
            background_tasks.add_task(send_report_to_user(request.email, report_content))

            return {"message": "Email successfully verified, product report will be sent shortly."}

        except Exception as e:
            logger.error(f"Error generating GPT report for {request.email}: {str(e)}")
            raise HTTPException(status_code=500, detail="Error generating product report.")
    else:
        logger.error(f"Invalid verification attempt for email: {request.email}")
        raise HTTPException(status_code=400, detail="Invalid or expired verification token.")