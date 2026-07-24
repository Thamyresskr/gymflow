"""
Handlers globais de exceções da aplicação.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import logger
from app.schemas.error import ErrorResponse


def register_exception_handlers(app: FastAPI):
    """
    Registra todos os handlers globais da aplicação.
    """

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        """
        Trata exceções HTTP lançadas pela aplicação.
        """

        logger.warning(
            "HTTP %s | %s | %s",
            exc.status_code,
            request.method,
            request.url.path,
        )

        error = ErrorResponse(
            status=exc.status_code,
            message=exc.detail,
            path=request.url.path,
            timestamp=datetime.now(timezone.utc),
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error.model_dump(mode="json"),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        """
        Trata erros de validação do FastAPI.
        """

        logger.warning(
            "Erro de validação | %s %s",
            request.method,
            request.url.path,
        )

        error = ErrorResponse(
            status=422,
            message="Dados da requisição inválidos.",
            path=request.url.path,
            timestamp=datetime.now(timezone.utc),
        )

        response = error.model_dump(mode="json")
        response["errors"] = exc.errors()

        return JSONResponse(
            status_code=422,
            content=response,
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        """
        Trata exceções inesperadas da aplicação.
        """

        logger.exception(
            "Erro interno | %s %s",
            request.method,
            request.url.path,
        )

        error = ErrorResponse(
            status=500,
            message="Ocorreu um erro interno no servidor.",
            path=request.url.path,
            timestamp=datetime.now(timezone.utc),
        )

        return JSONResponse(
            status_code=500,
            content=error.model_dump(mode="json"),
        )