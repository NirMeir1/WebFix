# ─── 1. Standard library ───────────────────────────────────────────────────────
import logging, time, os
from typing import Dict

# ─── 2. Third-party libraries ─────────────────────────────────────────────────
from dotenv import load_dotenv

from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi import Depends, FastAPI, BackgroundTasks, Request

import jwt

# ─── 3. Application modules ───────────────────────────────────────────────────
from backend.security import configure_security_and_rate_limit
from logging_config import setup_logging

from backend.exception_handlers import register_exception_handlers
from backend.schemas import UrlRequest, UrlResponse
from backend.gpt_service import ChatGPTService
from backend.email_service import send_verification_email, generate_jwt_token,decode_jwt_token, send_report_to_user
from backend.screenshot_service import run_screenshot_subprocess
from backend.utils.helper import normalize_url, is_mobile
from backend.redis.cache_instance import cache as run_cache

# ─── Bootstrap ───────────────────────────────────────────────────────────
load_dotenv()

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()
register_exception_handlers(app)

# Apply security & rate-limit setup and grab limiter + limits
limiter, BURST_LIMIT, DAILY_LIMIT = configure_security_and_rate_limit(app)

# ─── Dependencies ──────────────────────────────────────────────────────────────

def get_chat_service() -> ChatGPTService:
    return ChatGPTService()

def get_cache():
    return run_cache

# ─── Healthcheck ──────────────────────────────────────────────────────────────

@app.get("/", response_model=Dict[str, str])
def root() -> Dict[str, str]:
    logger.info("Root endpoint accessed")
    return {"message": "CRO Audit API is running"}


# ─── Analyze URL Endpoint ─────────────────────────────────────────────────────

@app.post("/analyze-url", response_model=UrlResponse)
@limiter.limit(f"{BURST_LIMIT};{DAILY_LIMIT}")
async def analyze_url(
    request: Request,
    payload: UrlRequest,
    background_tasks: BackgroundTasks,
    chat_service: ChatGPTService = Depends(get_chat_service),
    cache = Depends(get_cache),
) -> UrlResponse:
    start = time.time()
    logger.info("Received analyze-url request for %s (type=%s)",
                payload.url, payload.report_type)

    # Normalize and reassign
    normalized_url = normalize_url(payload.url)
    payload.url = normalized_url

    # Always generate a JWT for potential deep reports
    token = generate_jwt_token({
        "url": normalized_url,
        "report_type": payload.report_type,
        "email": payload.email,
    })

    # before deploying, Uncomment the following lines. 
    # test it again with ngrok before deploying.

    # if payload.report_type == "deep":
    #     background_tasks.add_task(send_verification_email,
    #                               payload.email, token)
    #     logger.info("Email verification initiated for %s", payload.email)
    #     return UrlResponse(output="Email verification sent, Please verify to proceed.")


    # Basic report path
    is_cached, report = await cache.run(
        url=normalized_url,
        report_type=payload.report_type,
        email=payload.email,
        gpt_func=lambda: chat_service.generate_gpt_report(
            normalized_url, payload.report_type
        ),
    )
    logger.info("GPT report generated for %s", normalized_url)

    ua = request.headers.get("User-Agent", "")
    screenshot = None if is_mobile(ua) else run_screenshot_subprocess(normalized_url)

    elapsed = time.time() - start
    logger.info("analyze-url processed in %.3f seconds", elapsed)

    # final response + HttpOnly Secure cookie
    resp = JSONResponse(
        content=UrlResponse
        (output=report, screenshot_base64=screenshot, is_cached=is_cached).model_dump()
    )
    resp.set_cookie(
        "access_token",
        token,
        httponly=True,
        secure=(os.getenv("ENVIRONMENT") == "production"),
        samesite="lax"
    )
    return resp


# ─── Email Verification Endpoint ───────────────────────────────────────────────

@app.get("/verify-email", response_model=Dict[str, str])
async def verify_email(
    token: str,
    background_tasks: BackgroundTasks,
    chat_service: ChatGPTService = Depends(get_chat_service),
    cache = Depends(get_cache),
) -> Dict[str, str]:
    decoded = decode_jwt_token(token)
    email = decoded["email"]
    url = decoded["url"]
    report_type = decoded["report_type"]

    logger.info("Email verified for %s; generating deep report", email)

    is_cached, report = await cache.run(
        url=url,
        report_type=report_type,
        email=email,
        gpt_func=lambda: chat_service.generate_gpt_report(
            url, report_type, email
        ),
    )

    background_tasks.add_task(send_report_to_user, email, report)
    return {"message": "Email verified successfully. Report will be sent shortly."}