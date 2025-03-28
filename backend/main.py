from fastapi import FastAPI, HTTPException, BackgroundTasks
from backend.schemas import UrlRequest, UrlResponse
from backend.gpt_service import ChatGPTService
from backend.email_service import send_verification_email, generate_jwt_token,decode_jwt_token, send_report_to_user
from dotenv import load_dotenv
from logging_config import setup_logging
from backend.helper import normalize_url
from backend.redis.cache_instance import cache as run_cache
import logging
import jwt

setup_logging()
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI()

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Backend is running"}

# Debug endpoint to get all keys in the cache
# This is useful for debugging and monitoring the cache
@app.get("/debug-keys")
def get_all_keys():
    keys = run_cache.cache.client.keys("*")
    return {"keys": keys}


@app.post("/analyze-url", response_model=UrlResponse)
async def analyze_url(request: UrlRequest, background_tasks: BackgroundTasks):
    logger.info(f"Processing URL request: {request.url}")

    request.url = normalize_url(request.url)
    
    jwt_data = {
        "url": request.url,
        "report_type": request.report_type,
        "industry": request.industry,
        "email": request.email
    }

    jwt_token = generate_jwt_token(jwt_data)

    if request.report_type == "deep":
        if not request.email:
            logger.warning("Email required but not provided for deep report")
            raise HTTPException(status_code=400, detail="Email required for deep reports")

        background_tasks.add_task(send_verification_email, request.email, jwt_token)
        logger.info(f"Email verification initiated for {request.email}")
        return UrlResponse(output="Email verification sent. Please verify to proceed.", message="Type B: Awaiting verification")

    # Basic report directly generated
    try:
        gpt_instance = ChatGPTService()

         # "_", output is used to ignore the message type for now
        # it will return the message type in the future
        # message is the msg type (A, B, Z) and output is the actual response.
        _, output = await run_cache.run(
            url=request.url,
            report_type=request.report_type,
            industry=request.industry,
            email=request.email,
            gpt_func=lambda: gpt_instance.generate_gpt_report(
                request.url, request.report_type, request.industry
            )
        )

        logger.info(f"GPT response generated for URL: {request.url}")
        return UrlResponse(output=output, message="Type Z: Basic report generated")
    
    except Exception as e:
        logger.error(f"Error generating GPT response: {e}")
        raise HTTPException(status_code=500, detail="Error generating product report.")


@app.get("/verify-email")
async def email_verification(token: str, background_tasks: BackgroundTasks):
    try:
        decoded = decode_jwt_token(token)
        email = decoded['email']
        url = decoded['url']
        report_type = decoded['report_type']
        industry = decoded['industry']

        logger.info(f"Email verified: {email}")

        gpt_instance = ChatGPTService()

        # "_", output is used to ignore the message type for now
        # it will return the message type in the future
        # message is the msg type (A, B, Z) and output is the actual response.
        _, output = await run_cache.run(
            url=url,
            report_type=report_type,
            industry=industry,
            email=email,
            gpt_func=lambda: gpt_instance.generate_gpt_report(
                url, report_type, industry, email
            )
        )


        background_tasks.add_task(send_report_to_user, email, output)

        return {"message": "Email verified successfully. Report will be sent shortly."}

    except jwt.ExpiredSignatureError:
        logger.error("JWT Token expired.")
        raise HTTPException(status_code=400, detail="Token expired.")
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT Token.")
        raise HTTPException(status_code=400, detail="Invalid token.")
    except Exception as e:
        logger.error(f"Error processing verification: {e}")
        raise HTTPException(status_code=500, detail="Error processing verification.")