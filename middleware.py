import logging
from main import app
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

from os import getenv
from config import config

# configure logging
logger = logging.getLogger(__name__)

# 1. CORS Middleware configuration
# To support local running frontend apps (React, Vite, Next.js, Flutter Web, etc.),
# native mobile apps running on emulators (IP 10.0.2.2),
# physical devices on local network, and built APKs (file://, capacitor://, null origins).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        config.url,
        "https://wagfu-backend.onrender.com",
    ],
    # Regex to support any local dev host, native mobile apps, and custom webview schemes
    allow_origin_regex=r"https?://.*|capacitor://.*|chrome-extension://.*|file://.*|null",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=600,
)


# 2. Cookie to Authorization header fallback middleware
# Since built APKs and mobile apps often use the Authorization header,
# while local browser sessions use the Bearer cookie, this middleware
# copies the Bearer cookie to the Authorization header if it is missing.
@app.middleware("http")
async def extract_bearer_cookie_to_header(request: Request, call_next):
    if "authorization" not in request.headers:
        bearer_cookie = request.cookies.get("Bearer")
        if bearer_cookie:
            logger.debug("Injecting Bearer token from cookie into Authorization header")
            # Mutate the ASGI scope headers list to inject the Authorization header
            raw_headers = list(request.scope.get("headers", []))
            raw_headers.append((b"authorization", f"Bearer {bearer_cookie}".encode("latin-1")))
            request.scope["headers"] = raw_headers
            
    response = await call_next(request)
    return response


# 3. Ensure valid referer and origin header middleware
# If referer/origin is missing, null, or a custom scheme (like file:// or capacitor://)
# commonly sent by built APKs or emulators, this middleware intercepts the request
# and replaces it with a valid default HTTP/HTTPS referer (or origin).
@app.middleware("http")
async def ensure_valid_referer(request: Request, call_next):
    # Mutate scope headers dictionary
    headers_dict = {}
    for k, v in request.scope.get("headers", []):
        headers_dict[k.lower()] = v

    # Check referer
    referer = headers_dict.get(b"referer")
    if not referer or not referer.startswith(b"http"):
        default_ref = "https://wagfu-backend.onrender.com" if int(getenv("IS_CLOUD", "0")) else "http://localhost:8000"
        headers_dict[b"referer"] = default_ref.encode("latin-1")

    # Check origin
    origin = headers_dict.get(b"origin")
    if not origin or not origin.startswith(b"http"):
        default_ori = "https://wagfu-backend.onrender.com" if int(getenv("IS_CLOUD", "0")) else "http://localhost:8000"
        headers_dict[b"origin"] = default_ori.encode("latin-1")

    # Update scope headers
    request.scope["headers"] = list(headers_dict.items())

    response = await call_next(request)
    return response