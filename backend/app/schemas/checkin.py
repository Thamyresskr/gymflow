"""
Schemas relacionados aos check-ins.

Responsabilidades:
- Definir os contratos de resposta da API
- Documentar os modelos exibidos no Swagger
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CheckinResponse(BaseModel):
    """
    Dados retornados pela API após operações de check-in e check-out.
    """

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
        description="Data e hora em que o usuário realizou o check-in.",
        examples=["2026-07-25T08:15:32Z"],
    )

    checkout_time: datetime | None = Field(
        default=None,
        title="Horário do Check-out",
        description=(
            "Data e hora em que o usuário realizou o check-out. "
            "Permanece nulo enquanto o usuário estiver na academia."
        ),
        examples=[
            "2026-07-25T09:47:10Z",
            None,
        ],
    )

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