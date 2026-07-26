"""
Schemas padronizados para respostas de erro da API.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ErrorResponse(BaseModel):
    """
    Modelo padrão para respostas de erro da API.
    """

    success: bool = Field(
        default=False,
        title="Sucesso",
        description="Indica se a operação foi executada com sucesso.",
        examples=[False],
    )

    status: int = Field(
        ...,
        title="Status HTTP",
        description="Código HTTP retornado pela API.",
        ge=100,
        le=599,
        examples=[400],
    )

    code: str | None = Field(
        default=None,
        title="Código do Erro",
        description="Código interno utilizado para identificação do erro.",
        examples=["INVALID_CREDENTIALS"],
    )

    message: str = Field(
        ...,
        title="Mensagem",
        description="Mensagem descritiva do erro.",
        examples=["Credenciais inválidas."],
    )

    path: str = Field(
        ...,
        title="Endpoint",
        description="Endpoint que originou o erro.",
        examples=["/auth/login"],
    )

    timestamp: datetime = Field(
        ...,
        title="Data/Hora",
        description="Data e hora em que o erro ocorreu.",
        examples=["2026-07-25T19:30:00Z"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "status": 401,
                "code": "INVALID_CREDENTIALS",
                "message": "Credenciais inválidas.",
                "path": "/auth/login",
                "timestamp": "2026-07-25T19:30:00Z",
            }
        }
    )