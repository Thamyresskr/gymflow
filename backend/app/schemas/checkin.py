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
    Dados retornados pela API após operações de check-in e checkout.
    """

    id: int = Field(
        description="Identificador do check-in.",
        examples=[1],
    )

    user_id: int = Field(
        description="Identificador do usuário.",
        examples=[5],
    )

    checkin_time: datetime = Field(
        description="Data e hora em que o usuário realizou o check-in.",
    )

    checkout_time: datetime | None = Field(
        default=None,
        description=(
            "Data e hora do checkout. "
            "Permanece nulo enquanto o usuário estiver na academia."
        ),
    )

    model_config = ConfigDict(
        from_attributes=True,
    )