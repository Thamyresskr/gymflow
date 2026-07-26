"""
Testes da camada de serviço de usuários.
"""

import pytest
from fastapi import HTTPException, status

from app.models.user import TipoUsuario, User
from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import (
    get_user,
    list_users,
    register_user,
    remove_user,
    update_user_data,
)


def criar_usuario(db_session) -> User:
    """
    Cria um usuário para utilização nos testes.
    """

    return register_user(
        db_session,
        UserCreate(
            nome="João",
            email="joao@gymflow.com",
            senha="123456",
            matricula="20260010",
            telefone="11999999999",
        ),
    )


def test_register_user_success(db_session):
    """
    Deve cadastrar um usuário quando o e-mail não existir.
    """

    user = criar_usuario(db_session)

    assert user.id is not None
    assert user.nome == "João"
    assert user.email == "joao@gymflow.com"
    assert user.tipo == TipoUsuario.ALUNO


def test_register_user_email_already_exists(db_session):
    """
    Deve impedir cadastro com e-mail duplicado.
    """

    criar_usuario(db_session)

    with pytest.raises(HTTPException) as exc:
        register_user(
            db_session,
            UserCreate(
                nome="Maria",
                email="joao@gymflow.com",
                senha="123456",
                matricula="20260011",
                telefone="11988888888",
            ),
        )

    assert exc.value.status_code == status.HTTP_409_CONFLICT
    assert exc.value.detail == "E-mail já cadastrado."


def test_list_users(db_session):
    """
    Deve listar todos os usuários cadastrados.
    """

    criar_usuario(db_session)

    users = list_users(db_session)

    assert len(users) == 1


def test_get_user_success(db_session):
    """
    Deve localizar um usuário existente.
    """

    user = criar_usuario(db_session)

    found = get_user(
        db_session,
        user.id,
    )

    assert found.id == user.id
    assert found.email == user.email


def test_get_user_not_found(db_session):
    """
    Deve lançar exceção quando o usuário não existir.
    """

    with pytest.raises(HTTPException) as exc:
        get_user(
            db_session,
            999,
        )

    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc.value.detail == "Usuário não encontrado."


def test_update_user_data(db_session):
    """
    Deve atualizar um usuário existente.
    """

    user = criar_usuario(db_session)

    updated = update_user_data(
        db_session,
        user.id,
        UserUpdate(
            nome="João Pedro",
            telefone="11911112222",
        ),
    )

    assert updated.nome == "João Pedro"
    assert updated.telefone == "11911112222"
    assert updated.email == "joao@gymflow.com"


def test_remove_user(db_session):
    """
    Deve remover um usuário existente.
    """

    user = criar_usuario(db_session)

    remove_user(
        db_session,
        user.id,
    )

    with pytest.raises(HTTPException):
        get_user(
            db_session,
            user.id,
        )