
import time, uuid, structlog
import structlog.contextvars as ctxv
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        idem_key   = request.headers.get("Idempotency-Key")

        ctxv.bind_contextvars(request_id=request_id, idem_key=idem_key)

        log = structlog.get_logger().bind(method=request.method, path=request.url.path)
        start = time.perf_counter()
        try:
            resp: Response = await call_next(request)
            dur_ms = int((time.perf_counter() - start) * 1000)
            log.info("http_request", status_code=resp.status_code, duration_ms=dur_ms)
            resp.headers["X-Request-ID"] = request_id
            return resp
        except Exception:
            dur_ms = int((time.perf_counter() - start) * 1000)
            log.exception("http_request_error", duration_ms=dur_ms)
            raise
        finally:
            ctxv.clear_contextvars()
