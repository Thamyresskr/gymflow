
"""
Handlers globais de exceções da aplicação.
"""

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic_core import to_jsonable_python

from app.core.exceptions import AppException
from app.core.logger import logger
from app.schemas.error import ErrorResponse


def build_error_response(
    *,
    status: int,
    message: str,
    path: str,
    code: str | None = None,
    errors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Cria uma resposta padronizada de erro.
    """

    error = ErrorResponse(
        success=False,
        status=status,
        code=code,
        message=message,
        path=path,
        timestamp=datetime.now(timezone.utc),
    )

    response = error.model_dump(
        mode="json",
        exclude_none=True,
    )

    if errors:
        response["errors"] = to_jsonable_python(errors)

    return response


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registra todos os handlers globais da aplicação.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ) -> JSONResponse:
        """
        Trata exceções personalizadas da aplicação.
        """

        logger.warning(
            "%s | %s %s",
            exc.code,
            request.method,
            request.url.path,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=build_error_response(
                status=exc.status_code,
                code=exc.code,
                message=exc.message,
                path=request.url.path,
            ),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        """
        Trata exceções HTTP.
        """

        logger.warning(
            "HTTP %s | %s %s",
            exc.status_code,
            request.method,
            request.url.path,
        )

        code = None
        message = str(exc.detail)

        if isinstance(exc.detail, dict):
            code = exc.detail.get("code")
            message = exc.detail.get("message", message)

        return JSONResponse(
            status_code=exc.status_code,
            content=build_error_response(
                status=exc.status_code,
                code=code,
                message=message,
                path=request.url.path,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """
        Trata erros de validação com detalhes compatíveis com JSON.
        """

        logger.warning(
            "VALIDATION_ERROR | %s %s",
            request.method,
            request.url.path,
        )

        # Remove o contexto interno, que pode conter objetos como
        # ValueError, e converte os valores restantes para JSON.
        validation_errors = []

        for error in exc.errors():
            validation_error = {
                key: value
                for key, value in error.items()
                if key != "ctx"
            }
            validation_errors.append(validation_error)

        validation_errors = to_jsonable_python(validation_errors)

        return JSONResponse(
            status_code=422,
            content=build_error_response(
                status=422,
                code="VALIDATION_ERROR",
                message="Dados da requisição inválidos.",
                path=request.url.path,
                errors=validation_errors,
            ),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        Trata erros inesperados.
        """

        logger.exception(
            "Erro interno | %s %s",
            request.method,
            request.url.path,
            exc_info=exc,
        )

        return JSONResponse(
            status_code=500,
            content=build_error_response(
                status=500,
                code="INTERNAL_SERVER_ERROR",
                message="Ocorreu um erro interno no servidor.",
                path=request.url.path,
            ),
        )
