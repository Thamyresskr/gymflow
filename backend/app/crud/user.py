"""
Camada de acesso a dados (CRUD) para usuários.

Responsabilidades:
- Persistir usuários.
- Consultar usuários.
- Atualizar usuários.
- Remover usuários.
"""

from sqlalchemy.exc import IntegrityError
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
        email: Endereço de e-mail do usuário.

    Returns:
        User | None: Usuário encontrado ou None.
    """
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_user_by_matricula(
    db: Session,
    matricula: str,
) -> User | None:
    """
    Busca um usuário pela matrícula.

    Args:
        db: Sessão ativa do banco de dados.
        matricula: Matrícula do usuário.

    Returns:
        User | None: Usuário encontrado ou None.
    """
    return (
        db.query(User)
        .filter(User.matricula == matricula)
        .first()
    )


def get_all_users(
    db: Session,
) -> list[User]:
    """
    Retorna todos os usuários cadastrados.

    Os registros são ordenados alfabeticamente pelo nome.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        list[User]: Lista de usuários cadastrados.
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
    Cria um novo usuário com o perfil ALUNO.

    Args:
        db: Sessão ativa do banco de dados.
        user_data: Dados necessários para criar o usuário.

    Returns:
        User: Usuário persistido no banco de dados.

    Raises:
        IntegrityError: Se houver violação de uma restrição
            de integridade do banco de dados.
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

    try:
        db.add(user)
        db.flush()
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise


def update_user(
    db: Session,
    user: User,
) -> User:
    """
    Persiste as alterações de um usuário existente.

    Args:
        db: Sessão ativa do banco de dados.
        user: Instância do usuário com os campos atualizados.

    Returns:
        User: Usuário atualizado e persistido.

    Raises:
        IntegrityError: Se houver violação de uma restrição
            de integridade do banco de dados.
    """
    try:
        db.add(user)
        db.flush()
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise


def delete_user(
    db: Session,
    user: User,
) -> None:
    """
    Remove um usuário do banco de dados.

    Args:
        db: Sessão ativa do banco de dados.
        user: Usuário que será removido.

    Raises:
        IntegrityError: Se houver violação de uma restrição
            de integridade durante a exclusão.
    """
    try:
        db.delete(user)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise
