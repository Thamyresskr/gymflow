from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Modelo padrão para respostas de erro da API.
    """

    success: bool = False
    status: int
    message: str
    path: str
    timestamp: datetime