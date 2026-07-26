"""
Camada de acesso a dados (CRUD) para usuários.

Responsabilidades:
- Persistir usuários.
- Consultar usuários.
- Atualizar usuários.
- Remover usuários.
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
    Busca um usuário pelo identificador.

    Args:
        db: Sessão ativa do banco de dados.
        user_id: Identificador do usuário.

    Returns:
        User | None: Usuário encontrado ou None.
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

    Args:
        db: Sessão ativa do banco de dados.
        email: Endereço de e-mail.

    Returns:
        User | None: Usuário encontrado ou None.
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

    Os registros são ordenados alfabeticamente pelo nome.
    """

    return (
        db.query(User)
        .order_by(User.nome.asc())
        .all()
    )


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """
    Cria um novo usuário.

    Args:
        db: Sessão ativa do banco de dados.
        user_data: Dados do novo usuário.

    Returns:
        User: Usuário persistido.
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

    # Gera o ID antes do commit
    db.flush()

    db.commit()
    db.refresh(user)

    return user


def update_user(
    db: Session,
    user: User,
) -> User:
    """
    Persiste alterações realizadas em um usuário.

    Args:
        db: Sessão ativa do banco de dados.
        user: Usuário atualizado.

    Returns:
        User: Usuário persistido.
    """

    db.add(user)

    db.flush()
    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    """
    Remove um usuário.

    Args:
        db: Sessão ativa do banco de dados.
        user: Usuário a ser removido.
    """

    db.delete(user)
    db.commit()