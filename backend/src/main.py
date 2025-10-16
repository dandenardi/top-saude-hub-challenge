import os
from fastapi import FastAPI
from .infrastructure.log_setup import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from .api.middlewares import RequestLogMiddleware
from .api.router import router
from .api.errors import http_error_handler

setup_logging(os.getenv("LOG_LEVEL", "INFO"))

app = FastAPI(title="Catalog Orders API")

app.add_middleware(
    
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

app.add_middleware(RequestLogMiddleware)
app.include_router(router, prefix="/api")
app.add_exception_handler(Exception, http_error_handler)
