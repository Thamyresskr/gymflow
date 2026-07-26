"""
Testes da camada CRUD de usuários.
"""

from app.crud.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)
from app.models.user import TipoUsuario, User
from app.schemas.user import UserCreate


def criar_usuario(
    db_session,
    nome: str,
    email: str,
    matricula: str,
    telefone: str,
) -> User:
    """
    Cria um usuário para utilização nos testes.
    """

    user = User(
        nome=nome,
        email=email,
        senha_hash="123",
        tipo=TipoUsuario.ALUNO,
        matricula=matricula,
        telefone=telefone,
        ativo=True,
    )

    db_session.add(user)
    db_session.flush()
    db_session.commit()
    db_session.refresh(user)

    return user


def test_create_user(db_session):
    """
    Deve criar um novo usuário.
    """

    user_data = UserCreate(
        nome="João",
        email="joao@gymflow.com",
        senha="123456",
        matricula="20260001",
        telefone="11999999999",
    )

    user = create_user(
        db_session,
        user_data,
    )

    assert user.id is not None
    assert user.nome == user_data.nome
    assert user.email == user_data.email
    assert user.tipo == TipoUsuario.ALUNO
    assert user.ativo is True
    assert user.senha_hash != user_data.senha


def test_get_user_by_id(db_session):
    """
    Deve localizar um usuário pelo ID.
    """

    user = criar_usuario(
        db_session,
        "Maria",
        "maria@gymflow.com",
        "20260002",
        "11988888888",
    )

    result = get_user_by_id(
        db_session,
        user.id,
    )

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email


def test_get_user_by_email(db_session):
    """
    Deve localizar um usuário pelo e-mail.
    """

    user = criar_usuario(
        db_session,
        "Pedro",
        "pedro@gymflow.com",
        "20260003",
        "11977777777",
    )

    result = get_user_by_email(
        db_session,
        user.email,
    )

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email


def test_get_all_users(db_session):
    """
    Deve retornar todos os usuários cadastrados.
    """

    criar_usuario(
        db_session,
        "Ana",
        "ana@gymflow.com",
        "20260004",
        "11966666666",
    )

    criar_usuario(
        db_session,
        "Bruno",
        "bruno@gymflow.com",
        "20260005",
        "11955555555",
    )

    users = get_all_users(
        db_session,
    )

    assert len(users) == 2
    assert users[0].nome == "Ana"
    assert users[1].nome == "Bruno"


def test_update_user(db_session):
    """
    Deve atualizar um usuário existente.
    """

    user = criar_usuario(
        db_session,
        "Carlos",
        "carlos@gymflow.com",
        "20260006",
        "11944444444",
    )

    user.nome = "Carlos Silva"

    updated = update_user(
        db_session,
        user,
    )

    assert updated.nome == "Carlos Silva"
    assert updated.email == "carlos@gymflow.com"


def test_delete_user(db_session):
    """
    Deve remover um usuário do banco.
    """

    user = criar_usuario(
        db_session,
        "Fernanda",
        "fernanda@gymflow.com",
        "20260007",
        "11933333333",
    )

    user_id = user.id

    delete_user(
        db_session,
        user,
    )

    deleted = get_user_by_id(
        db_session,
        user_id,
    )

    assert deleted is None