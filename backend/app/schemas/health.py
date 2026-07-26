"""
Schemas da rota de Health Check.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class HealthResponse(BaseModel):
    """
    Resposta do endpoint de Health Check.
    """

    status: str = Field(
        ...,
        title="Status",
        description="Status atual da aplicação.",
        examples=["healthy"],
    )

    version: str = Field(
        ...,
        title="Versão",
        description="Versão atual da API.",
        examples=["1.0.0"],
    )

    timestamp: datetime = Field(
        ...,
        title="Data/Hora",
        description="Momento da verificação.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2026-07-25T20:30:00Z",
            }
        }
    )