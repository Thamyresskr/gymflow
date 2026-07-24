from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.user import TipoUsuario


class UserBase(BaseModel):
    """
    Informações básicas do usuário.
    """

    nome: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    telefone: Optional[str] = None


class UserCreate(UserBase):
    """
    Cadastro de usuário.
    """

    senha: str = Field(..., min_length=6)
    matricula: Optional[str] = None


class UserLogin(BaseModel):
    """
    Dados utilizados para login.
    """

    email: EmailStr
    senha: str


class UserUpdate(BaseModel):
    """
    Atualização parcial.
    """

    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = None
    matricula: Optional[str] = None
    ativo: Optional[bool] = None


class UserResponse(UserBase):
    """
    Dados retornados pela API.
    """

    id: int
    tipo: TipoUsuario
    matricula: Optional[str]
    ativo: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )