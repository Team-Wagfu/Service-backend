"""
handle global exception handlers to app instance

functional notes for corresponding handling party:
    - presence of redirect header indicates need to redirect, and the path to which
    redirection should happen is the value of the response key 'redirect'
    - message is the madatory field in every response, which describes the error
    - status_code is another mandatory field in every response
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from main import app
from core.exceptions import (
    InvalidSignatureException,
    ExpiredTokenException,
    AuthenticationError,
)


# top level errors and exceptions
@app.exception_handler(AuthenticationError)
def handle_authentication_error(request: Request, exc: AuthenticationError):
    """send redirection to /login"""
    return JSONResponse(
        status_code=500,
        content={
            "message": "Failed to perform the specified operation",
            "redirect": "/login",
        },
    )


# token exceptions
@app.exception_handler(InvalidSignatureException)
def handle_invalid_signature_exception(
    request: Request, exc: InvalidSignatureException
):
    """send redirection to /login when the token is invalid ot obtain a new token"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Invalid Token, please Re-Authenticate",
            "redirect": "/login",
        },
    )


@app.exception_handler(ExpiredTokenException)
def handler_expired_token_exception(request: Request, exc: ExpiredTokenException):
    """send redirection to /login when the token has expired to obtain a new token"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Token expired, please re-authenticate",
            "redirect": "/login",
        },
    )


# handle programmatic errors gracefully
@app.exception_handler(SyntaxError)
def handle_syntax_error(req: Request, exc: SyntaxError):
    """handle syntactic error gracefully and send an unresponsive notice"""
    return JSONResponse(
        status_code=500, content={"message": "Unable to serve at the moment"}
    )


@app.exception_handler(RuntimeError)
def handle_runtime_error(req: Request, exc: RuntimeError):
    """handle runtime errors gracefully and send a server unresponsive message"""
    return JSONResponse(
        status_code=500, content={"message": "Unable to serve at the moment"}
    )


@app.exception_handler(ValidationError)
def handle_validation_error(req: Request, exc: ValidationError):
    """handle validation errors and block data leak"""
    return JSONResponse(
        status_code=500, content={"message": "Unable to serve at the moment"}
    )
