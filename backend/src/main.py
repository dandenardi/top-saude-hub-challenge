from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.router import router
from .api.errors import http_error_handler

app = FastAPI(title="Catalog Orders API")
app.include_router(router, prefix="/api")
app.add_exception_handler(Exception, http_error_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)
