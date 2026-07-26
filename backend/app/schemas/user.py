"""
Schemas relacionados aos usuários.
"""

from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
)

from app.models.user import TipoUsuario


Telefone = Annotated[
    str,
    StringConstraints(
        pattern=r"^\d{10,11}$",
    ),
]


class UserBase(BaseModel):
    """
    Informações básicas de um usuário.
    """

    nome: str = Field(
        ...,
        title="Nome",
        description="Nome completo do usuário.",
        min_length=3,
        max_length=100,
        examples=["João da Silva"],
    )

    email: EmailStr = Field(
        ...,
        title="E-mail",
        description="Endereço de e-mail do usuário.",
        examples=["joao@email.com"],
    )

    telefone: Telefone | None = Field(
        default=None,
        title="Telefone",
        description="Telefone para contato (10 ou 11 dígitos).",
        examples=["11987654321"],
    )


class UserCreate(UserBase):
    """
    Dados necessários para o cadastro de um usuário.
    """

    senha: str = Field(
        ...,
        title="Senha",
        description="Senha do usuário. Deve possuir no mínimo 6 caracteres.",
        min_length=6,
        examples=["Senha@123"],
    )

    matricula: str | None = Field(
        default=None,
        title="Matrícula",
        description="Número de matrícula do aluno, quando aplicável.",
        examples=["202600001"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nome": "João da Silva",
                "email": "joao@email.com",
                "telefone": "11987654321",
                "senha": "Senha@123",
                "matricula": "202600001",
            }
        }
    )


class UserLogin(BaseModel):
    """
    Credenciais utilizadas para autenticação.
    """

    email: EmailStr = Field(
        ...,
        title="E-mail",
        description="E-mail utilizado no login.",
        examples=["joao@email.com"],
    )

    senha: str = Field(
        ...,
        title="Senha",
        description="Senha cadastrada do usuário.",
        examples=["Senha@123"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "joao@email.com",
                "senha": "Senha@123",
            }
        }
    )


class UserUpdateBase(BaseModel):
    """
    Campos básicos utilizados na atualização do usuário.
    Todos os campos são opcionais.
    """

    nome: str | None = Field(
        default=None,
        title="Nome",
        description="Nome completo.",
        min_length=3,
        max_length=100,
        examples=["João Pedro da Silva"],
    )

    email: EmailStr | None = Field(
        default=None,
        title="E-mail",
        description="Novo e-mail do usuário.",
        examples=["novo@email.com"],
    )

    telefone: Telefone | None = Field(
        default=None,
        title="Telefone",
        description="Telefone atualizado.",
        examples=["11999998888"],
    )


class UserUpdate(UserUpdateBase):
    """
    Dados utilizados para atualização do usuário.
    """

    matricula: str | None = Field(
        default=None,
        title="Matrícula",
        description="Nova matrícula.",
        examples=["202600001"],
    )

    ativo: bool | None = Field(
        default=None,
        title="Status",
        description="Indica se o usuário está ativo.",
        examples=[True],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "telefone": "11999998888"
            }
        }
    )


class UserPasswordUpdate(BaseModel):
    """
    Dados utilizados para alteração da senha.
    """

    senha_atual: str = Field(
        ...,
        title="Senha Atual",
        description="Senha atual do usuário.",
        min_length=6,
        examples=["Senha@123"],
    )

    nova_senha: str = Field(
        ...,
        title="Nova Senha",
        description="Nova senha do usuário.",
        min_length=6,
        examples=["NovaSenha@123"],
    )


class UserResponse(UserBase):
    """
    Dados retornados pela API após operações com usuários.
    """

    id: int = Field(
        ...,
        title="ID",
        description="Identificador único do usuário.",
        examples=[1],
    )

    tipo: TipoUsuario = Field(
        ...,
        title="Tipo",
        description="Perfil do usuário no sistema.",
        examples=["ALUNO"],
    )

    matricula: str | None = Field(
        default=None,
        title="Matrícula",
        description="Matrícula do usuário.",
        examples=["202600001"],
    )

    ativo: bool = Field(
        ...,
        title="Ativo",
        description="Indica se o usuário está ativo.",
        examples=[True],
    )

    created_at: datetime = Field(
        ...,
        title="Data de Cadastro",
        description="Data e hora em que o usuário foi criado.",
        examples=["2026-07-25T18:30:00"],
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nome": "João da Silva",
                "email": "joao@email.com",
                "telefone": "11987654321",
                "tipo": "ALUNO",
                "matricula": "202600001",
                "ativo": True,
                "created_at": "2026-07-25T18:30:00",
            }
        },
    )