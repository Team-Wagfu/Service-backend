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
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from main import app
from core.exceptions import (
    InvalidSignatureException,
    ExpiredTokenException,
    AuthenticationError,
    UserExistsError,
    PetError,
    PetNotFoundError,
    PetOwnerProfileError,
    PetAccessError,
    NotificationError,
    NotificationNotFoundError,
    NotificationAccessError,
    NotificationUserError,
    PetAddonError,
    PetAddonAccessError,
    VaccinationNotFoundError,
    MedicalRecordNotFoundError,
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


@app.exception_handler(UserExistsError)
def handle_user_exists_error(request: Request, exc: UserExistsError):
    """return no ok status"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": "Failed to register", "redirect": "/login"},
    )


@app.exception_handler(PetError)
def handle_pet_error(request: Request, exc: PetError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(PetNotFoundError)
def handle_pet_not_found_error(request: Request, exc: PetNotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(PetOwnerProfileError)
def handle_pet_owner_profile_error(request: Request, exc: PetOwnerProfileError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(PetAccessError)
def handle_pet_access_error(request: Request, exc: PetAccessError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(NotificationError)
def handle_notification_error(request: Request, exc: NotificationError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(NotificationNotFoundError)
def handle_notification_not_found_error(request: Request, exc: NotificationNotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(NotificationAccessError)
def handle_notification_access_error(request: Request, exc: NotificationAccessError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(NotificationUserError)
def handle_notification_user_error(request: Request, exc: NotificationUserError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(PetAddonError)
def handle_pet_addon_error(request: Request, exc: PetAddonError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(PetAddonAccessError)
def handle_pet_addon_access_error(request: Request, exc: PetAddonAccessError):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(VaccinationNotFoundError)
def handle_vaccination_not_found_error(
    request: Request, exc: VaccinationNotFoundError
):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


@app.exception_handler(MedicalRecordNotFoundError)
def handle_medical_record_not_found_error(
    request: Request, exc: MedicalRecordNotFoundError
):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.msg})


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


# data input error
@app.exception_handler(RequestValidationError)
def handle_request_validation_error(req: Request, exc: RequestValidationError):
    """handle validation error before request processing"""
    return JSONResponse(status_code=422, content={"message": "Unprocessable content"})


# unhandled exceptions
@app.exception_handler(Exception)
def handler_unknown_error(req: Request, exc: Exception):
    """handle unknown exception"""
    return JSONResponse(
        status_code=500, content={"message": "unable to serve at the moment"}
    )
