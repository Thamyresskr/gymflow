"""
Schemas relacionados à autenticação.
"""

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    """
    Token JWT retornado após autenticação.
    """

    access_token: str = Field(
        ...,
        title="Access Token",
        description=(
            "Token JWT utilizado para autenticar as requisições "
            "protegidas da API."
        ),
        examples=[
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        ],
    )

    token_type: str = Field(
        default="bearer",
        title="Tipo do Token",
        description=(
            "Tipo do token utilizado no cabeçalho "
            "Authorization da requisição."
        ),
        examples=["bearer"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": (
                    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                ),
                "token_type": "bearer",
            }
        }
    )