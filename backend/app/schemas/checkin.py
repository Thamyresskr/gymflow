
"""
Schemas relacionados aos check-ins.

Responsabilidades:
- Definir os contratos de resposta da API.
- Garantir que os horários retornados indiquem UTC explicitamente.
"""

from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CheckinResponse(BaseModel):
    """Dados retornados pela API após operações de check-in e check-out."""

    id: int = Field(
        ...,
        title="ID",
        description="Identificador único do registro de check-in.",
        examples=[1],
    )

    user_id: int = Field(
        ...,
        title="ID do Usuário",
        description="Identificador do usuário responsável pelo check-in.",
        examples=[5],
    )

    checkin_time: datetime = Field(
        ...,
        title="Horário do Check-in",
        description="Data e hora do check-in, em UTC.",
        examples=["2026-07-25T08:15:32Z"],
    )

    checkout_time: datetime | None = Field(
        default=None,
        title="Horário do Check-out",
        description="Data e hora do check-out, em UTC.",
        examples=["2026-07-25T09:47:10Z", None],
    )

    @field_validator("checkin_time", "checkout_time", mode="before")
    @classmethod
    def normalizar_horario_utc(cls, valor):
        """Identifica como UTC os datetimes sem fuso retornados pelo SQLite."""
        if valor is None:
            return None

        if isinstance(valor, datetime) and valor.tzinfo is None:
            return valor.replace(tzinfo=timezone.utc)

        return valor

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 5,
                "checkin_time": "2026-07-25T08:15:32Z",
                "checkout_time": "2026-07-25T09:47:10Z",
            }
        },
    )
