"""
Schemas utilizados pelo Dashboard.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DashboardResumo(BaseModel):
    """
    Indicadores principais do dashboard.
    """

    ocupacao_atual: int = Field(
        description="Quantidade de usuários presentes na academia.",
        json_schema_extra={"example": 18},
    )

    checkins_hoje: int = Field(
        description="Quantidade de check-ins realizados hoje.",
        json_schema_extra={"example": 42},
    )

    checkouts_hoje: int = Field(
        description="Quantidade de check-outs realizados hoje.",
        json_schema_extra={"example": 35},
    )

    tempo_medio_permanencia: float = Field(
        description="Tempo médio de permanência em minutos.",
        json_schema_extra={"example": 87.5},
    )


class DashboardUltimoCheckin(BaseModel):
    """
    Representa um registro exibido na lista dos últimos check-ins.
    """

    usuario: str = Field(
        description="Nome do usuário.",
        json_schema_extra={"example": "Aluno Teste"},
    )

    entrada: datetime = Field(
        description="Data e hora do check-in.",
        json_schema_extra={"example": "2026-07-24T08:30:00Z"},
    )

    saida: datetime | None = Field(
        default=None,
        description="Data e hora do check-out.",
        json_schema_extra={"example": "2026-07-24T09:45:00Z"},
    )

    model_config = ConfigDict(from_attributes=True)


class DashboardResponse(BaseModel):
    """
    Resposta completa do Dashboard.
    """

    resumo: DashboardResumo

    ultimos_checkins: list[DashboardUltimoCheckin] = Field(
        description="Lista dos últimos check-ins registrados.",
        json_schema_extra={
            "example": [
                {
                    "usuario": "Aluno Teste",
                    "entrada": "2026-07-24T08:30:00Z",
                    "saida": "2026-07-24T09:45:00Z",
                }
            ]
        },
    )

    model_config = ConfigDict(from_attributes=True)