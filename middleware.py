"""
create and bind the middleware
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from api.routes.v1.auth import router as authRouter
from main import app

# need to dynamically fetch routes
PROTECTED_PATHS = [""]


@app.middleware("http")
async def token_verification_middleware(request: Request, call_next):
    pass
