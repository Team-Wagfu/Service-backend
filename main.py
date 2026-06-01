"""Server Script"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes.v1.profile import router as profileRouter
from api.routes.v1.auth import router as authRouter
from db.engine import validate_engine
from exception_handler import attach_exception_handlers
from log import configure_logging

# configure logging
configure_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup initiated")

    try:
        logger.info("Verifying database connectivity")
        validate_engine()

        # already validated at config site
        logger.info("Verifying environment")

    except Exception as exc:
        logger.exception("Startup Failed")

        raise RuntimeError("Application Startup Failed") from exc

    yield


app = FastAPI(
    debug=True,
    title="Wagfu Service Backend",
    version="1.0.0",
    lifespan=lifespan,
)

# attach routers
app.include_router(authRouter, prefix="/api/v1")
app.include_router(profileRouter, prefix="/api/v1")
attach_exception_handlers(app)

# export to add middleware and exception handlers
__all__ = ["app"]
