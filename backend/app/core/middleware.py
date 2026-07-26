"""
Middlewares da aplicação.
"""

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware responsável por registrar informações de todas as requisições.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())

        start_time = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        client_ip = (
            request.client.host
            if request.client
            else "desconhecido"
        )

        logger.info(
            "[%s] %s %s | %s | %d | %.2f ms",
            request_id,
            request.method,
            request.url.path,
            client_ip,
            response.status_code,
            elapsed_ms,
        )

        response.headers["X-Request-ID"] = request_id

        return response