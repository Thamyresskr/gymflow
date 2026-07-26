"""
Schemas utilizados pelo Dashboard.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DashboardResumo(BaseModel):
    """
    Indicadores consolidados do Dashboard.
    """

    ocupacao_atual: int = Field(
        ...,
        title="Ocupação Atual",
        description="Quantidade de usuários presentes na academia no momento.",
        ge=0,
        examples=[18],
    )

    checkins_hoje: int = Field(
        ...,
        title="Check-ins Hoje",
        description="Quantidade de check-ins realizados na data atual.",
        ge=0,
        examples=[42],
    )

    checkouts_hoje: int = Field(
        ...,
        title="Check-outs Hoje",
        description="Quantidade de check-outs realizados na data atual.",
        ge=0,
        examples=[35],
    )

    tempo_medio_permanencia: float = Field(
        ...,
        title="Tempo Médio de Permanência",
        description="Tempo médio de permanência dos usuários na academia, em minutos.",
        ge=0,
        examples=[87.5],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ocupacao_atual": 18,
                "checkins_hoje": 42,
                "checkouts_hoje": 35,
                "tempo_medio_permanencia": 87.5,
            }
        }
    )


class DashboardUltimoCheckin(BaseModel):
    """
    Representa um dos últimos check-ins exibidos no Dashboard.
    """

    usuario: str = Field(
        ...,
        title="Usuário",
        description="Nome do usuário.",
        examples=["Aluno Teste"],
    )

    entrada: datetime = Field(
        ...,
        title="Entrada",
        description="Data e hora em que o usuário realizou o check-in.",
        examples=["2026-07-24T08:30:00Z"],
    )

    saida: datetime | None = Field(
        default=None,
        title="Saída",
        description=(
            "Data e hora do check-out. "
            "Será nulo enquanto o usuário permanecer na academia."
        ),
        examples=[
            "2026-07-24T09:45:00Z",
            None,
        ],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "usuario": "Aluno Teste",
                "entrada": "2026-07-24T08:30:00Z",
                "saida": "2026-07-24T09:45:00Z",
            }
        },
    )


class DashboardResponse(BaseModel):
    """
    Resposta completa do Dashboard.
    """

    resumo: DashboardResumo = Field(
        ...,
        title="Resumo",
        description="Indicadores gerais da academia.",
    )

    ultimos_checkins: list[DashboardUltimoCheckin] = Field(
        ...,
        title="Últimos Check-ins",
        description="Lista dos últimos check-ins registrados.",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "resumo": {
                    "ocupacao_atual": 18,
                    "checkins_hoje": 42,
                    "checkouts_hoje": 35,
                    "tempo_medio_permanencia": 87.5,
                },
                "ultimos_checkins": [
                    {
                        "usuario": "Aluno Teste",
                        "entrada": "2026-07-24T08:30:00Z",
                        "saida": "2026-07-24T09:45:00Z",
                    }
                ],
            }
        },
    )