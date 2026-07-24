"""
Camada de acesso a dados (CRUD) para Usuários.

Responsabilidades:
- Persistir usuários
- Buscar usuários
- Atualizar usuários
- Remover usuários
"""

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import TipoUsuario, User
from app.schemas.user import UserCreate


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    """
    Busca um usuário pelo ID.
    """

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    """
    Busca um usuário pelo e-mail.
    """

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_all_users(
    db: Session,
) -> list[User]:
    """
    Retorna todos os usuários cadastrados.
    """

    return (
        db.query(User)
        .order_by(User.nome)
        .all()
    )


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """
    Cria um novo usuário.
    """

    user = User(
        nome=user_data.nome,
        email=user_data.email,
        senha_hash=hash_password(user_data.senha),
        tipo=TipoUsuario.ALUNO,
        matricula=user_data.matricula,
        telefone=user_data.telefone,
        ativo=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user: User,
) -> User:
    """
    Atualiza um usuário.
    """

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    """
    Remove um usuário.
    """

    db.delete(user)
    db.commit()