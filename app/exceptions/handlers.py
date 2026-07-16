from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.exceptions.auth import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(EmailAlreadyExistsException)
    async def email_exists(_, __):
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Email already registered"
            },
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials(_, __):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid email or password"
            },
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token(_, __):
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Invalid token"
            },
        )