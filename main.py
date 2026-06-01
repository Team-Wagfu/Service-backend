"""Server Script"""

import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from api.routes.v1.profile import router as profileRouter
from api.routes.v1.auth import router as authRouter
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

# export to add middleware and exception handlers
__all__ = ["app"]
