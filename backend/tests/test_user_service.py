"""
Testes da camada de serviço de usuários.
"""

import pytest
from fastapi import HTTPException, status

from app.models.user import TipoUsuario, User
from app.schemas.user import UserCreate
from app.services.user_service import register_user


def test_register_user_success(db_session):
    """
    Deve cadastrar um usuário quando o e-mail não existir.
    """

    user_data = UserCreate(
        nome="João",
        email="joao@gymflow.com",
        senha="123456",
        matricula="20260010",
        telefone="11999999999",
    )

    user = register_user(db_session, user_data)

    assert user.id is not None
    assert user.email == user_data.email
    assert user.nome == user_data.nome
    assert user.tipo == TipoUsuario.ALUNO


def test_register_user_email_already_exists(db_session):
    """
    Deve impedir cadastro com e-mail já existente.
    """

    user = User(
        nome="Maria",
        email="maria@gymflow.com",
        senha_hash="123",
        tipo=TipoUsuario.ALUNO,
        matricula="20260011",
        telefone="11988888888",
        ativo=True,
    )

    db_session.add(user)
    db_session.commit()

    user_data = UserCreate(
        nome="Outra Maria",
        email="maria@gymflow.com",
        senha="123456",
        matricula="20260012",
        telefone="11977777777",
    )

    with pytest.raises(HTTPException) as exc:
        register_user(db_session, user_data)

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.detail == "E-mail já cadastrado."