import logging
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


def configure_logging(json_logs: bool = False) -> None:
    fmt = (
        '{"level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}'
        if json_logs
        else "%(levelname)s %(name)s: %(message)s"
    )
    logging.basicConfig(level=logging.INFO, format=fmt, force=True)


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        request_id = request.headers.get("x-request-id", str(uuid4()))
        token = request_id_ctx.set(request_id)
        try:
            response = await call_next(request)
            response.headers["x-request-id"] = request_id
            return response
        finally:
            request_id_ctx.reset(token)
