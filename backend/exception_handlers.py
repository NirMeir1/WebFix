import logging
import jwt
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request: Request, exc: HTTPException):
        logger.error(f"HTTPException: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(jwt.ExpiredSignatureError)
    async def handle_jwt_expired(request: Request, exc: jwt.ExpiredSignatureError):
        logger.error("JWT ExpiredSignatureError: token expired")
        return JSONResponse(
            status_code=400,
            content={"detail": "Token expired"},
        )

    @app.exception_handler(jwt.InvalidTokenError)
    async def handle_jwt_invalid(request: Request, exc: jwt.InvalidTokenError):
        logger.error("JWT InvalidTokenError: invalid token")
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid token"},
        )

    @app.exception_handler(Exception)
    async def handle_general_exception(request: Request, exc: Exception):
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )
