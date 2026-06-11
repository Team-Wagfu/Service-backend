"""Server Script"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes.v1.profile import router as profileRouter
from api.routes.v1.auth import router as authRouter
from api.routes.v1.pets import router as petRouter
from api.routes.v1.polling import router as pollRouter
from api.routes.v1.pet_addons import router as petAddonRouter
from api.routes.v1.token import router as tokenRouter
from db.engine import validate_engine
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


# add health check
@app.get("/health")
async def health():
    return {"status": "ok"}


# attach routers
logger.debug("Attached profile router")
app.include_router(profileRouter)

logger.debug("Attached auth router")
app.include_router(authRouter)

logger.debug("Attached pet router")
app.include_router(petRouter)

logger.debug("Attached poll router")
app.include_router(pollRouter)

logger.debug("Attached pet addon router")
app.include_router(petAddonRouter)

logger.debug("Attached token router")
app.include_router(tokenRouter)

import exception_handler  # noqa: F401,E402 — register global exception handlers

# export to add middleware and exception handlers
__all__ = ["app"]
