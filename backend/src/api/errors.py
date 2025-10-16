from fastapi import Request
from fastapi.responses import JSONResponse
from ..schemas.envelope import ApiEnvelope

async def http_error_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=400, content=ApiEnvelope.err(str(exc)).model_dump())
