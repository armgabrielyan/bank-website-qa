from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.routes import router
from app.settings import (
    ALLOW_HEADERS,
    ALLOW_ORIGINS,
    ALLOWED_HOSTS,
    DEBUG,
)

app = FastAPI(
    debug=DEBUG,
)

app.include_router(router)

app.add_middleware(GZipMiddleware, minimum_size=666)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_headers=ALLOW_HEADERS,
    allow_credentials=True,
    allow_methods=["*"],
)
