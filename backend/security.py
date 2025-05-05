import os
import logging
from typing import Tuple

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from slowapi import Limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

logger = logging.getLogger(__name__)

def _split_clean(env_val: str, to_upper: bool = False) -> list[str]:
    parts = [p.strip() for p in env_val.split(",")]
    if to_upper:
        parts = [p.upper() for p in parts]
    return [p for p in parts if p]


def configure_security_and_rate_limit(app: FastAPI) -> Tuple[Limiter, str, str]:
    """
    Apply HTTPS redirect, trusted hosts, CORS, and rate-limiting middleware to the FastAPI app.
    Configuration values are read from environment variables.

    Required ENV vars:
    - ENABLE_HTTPS_REDIRECT: 'true' to enable HTTPS redirect
    - ALLOWED_HOSTS: comma-separated list of allowed hostnames
    - CORS_ORIGINS: comma-separated list of allowed CORS origins
    - CORS_METHODS: comma-separated list of allowed HTTP methods
    - CORS_HEADERS: comma-separated list of allowed HTTP headers
    - BURST_LIMIT: e.g. '1/minute'
    - DAILY_LIMIT: e.g. '10/day'
    """
    # HTTPS redirect
    if os.getenv("ENABLE_HTTPS_REDIRECT", "false").lower() == "true":
        app.add_middleware(HTTPSRedirectMiddleware)
        logger.info("HTTPS redirect enabled")

    # Trusted hosts
    hosts = os.getenv("ALLOWED_HOSTS")
    if not hosts:
        raise RuntimeError("ALLOWED_HOSTS must be set in environment")
    allowed_hosts = _split_clean(hosts)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
    logger.info("Trusted hosts: %s", allowed_hosts)

    # CORS
    origins = os.getenv("CORS_ORIGINS")
    if not origins:
        raise RuntimeError("CORS_ORIGINS must be set in environment")
    cors_origins = _split_clean(origins)
    methods = _split_clean(os.getenv("CORS_METHODS", "GET,POST,OPTIONS"), to_upper=True)
    headers = _split_clean(os.getenv("CORS_HEADERS", "Content-Type"))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=methods,
        allow_headers=headers,
    )
    logger.info(
        "CORS config → origins: %s; methods: %s; headers: %s",
        cors_origins, methods, headers
    )

    # Rate limiting
    burst = os.getenv("BURST_LIMIT")
    daily = os.getenv("DAILY_LIMIT")
    if not burst or not daily:
        raise RuntimeError("BURST_LIMIT and DAILY_LIMIT must be set in environment")

    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    async def _rate_limit_handler(request: Request, exc):
        return JSONResponse(
            {"detail": "Too many requests — please slow down."},
            status_code=429
        )

    logger.info("Rate limits → burst: %s; daily: %s", burst, daily)

    return limiter, burst, daily