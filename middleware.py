import logging
from main import app
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware

# configure logging
logger = logging.getLogger(__name__)

# 1. CORS Middleware configuration
# To support local running frontend apps (React, Vite, Next.js, Flutter Web, etc.),
# native mobile apps running on emulators (IP 10.0.2.2),
# physical devices on local network, and built APKs (file://, capacitor://, null origins).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://10.0.2.2:8000",
        "http://10.0.2.2:3000",
        "http://10.0.2.2:5173",
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