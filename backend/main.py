import json
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from backend.schemas import UrlRequest, UrlResponse
from backend.gpt_service import ChatGPTService
from backend.email_service import send_verification_email, generate_jwt_token,decode_jwt_token, send_report_to_user
from dotenv import load_dotenv
from backend.screenshot_service import run_screenshot_subprocess
from logging_config import setup_logging
from backend.utils.helper import normalize_url, is_mobile
from backend.redis.cache_instance import cache as run_cache
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import jwt
import time

setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. You can restrict this for better security.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")


@app.post("/analyze-url")
async def analyze_url(requestUserAgent: Request, request: UrlRequest, background_tasks: BackgroundTasks):
    start_time = time.time()
    logger.info(f"Processing URL request: {request.url}")
    logger.info(f"⚙️ Received analyze-url request with report_type: {request.report_type}")

    user_agent_str = requestUserAgent.headers.get("User-Agent", "")
    

    request.url = normalize_url(request.url)

    jwt_data = {
        "url": request.url,
        "report_type": request.report_type,
        "email": request.email
    }

    jwt_token = generate_jwt_token(jwt_data)

    # before deploying, Uncomment the following lines. 
    # test it again with ngrok before deploying.

    # if request.report_type == "deep":
    #     background_tasks.add_task(send_verification_email, request.email, jwt_token)
    #     logger.info(f"Email verification initiated for {request.email}")
    #     return UrlResponse(output="Email verification sent, Please verify to proceed.")


    # Basic report directly generated
    try:
        gpt_instance = ChatGPTService()

        is_cached, output = await run_cache.run(
            url=request.url,
            report_type=request.report_type,
            email=request.email,
            gpt_func=lambda: gpt_instance.generate_gpt_report(
                request.url, request.report_type
            )
        )

        print(f"Is Cached: {is_cached}")

        # with open('output.json', 'w', encoding='utf-8') as f:
        #   json.dump(output, f, separators=(",", ":"), ensure_ascii=False)

        #print(f"Output: {output}")

        logger.info(f"GPT response generated for URL: {request.url}")

        if is_mobile(user_agent_str):
            screenshot_b64 = None  # ✅ Skip screenshot
        else:
            screenshot_b64 = run_screenshot_subprocess(request.url)

         # Measure time before returning
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken: {elapsed_time:.4f} seconds")

        return UrlResponse(
            output=output,
            screenshot_base64=screenshot_b64,
            is_cached=is_cached
        )

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

        logger.info(f"Email verified: {email}")

        gpt_instance = ChatGPTService()

        is_cached, output = await run_cache.run(
            url=url,
            report_type=report_type,
            email=email,
            gpt_func=lambda: gpt_instance.generate_gpt_report(
                url, report_type, email
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