"""
Handlers globais para tratamento de exceções da aplicação.
"""

from datetime import datetime

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Handler para exceções personalizadas da aplicação.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
            },
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
        },
    )