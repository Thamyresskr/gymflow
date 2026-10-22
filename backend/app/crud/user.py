
"""
Camada de acesso a dados (CRUD) para usuários.

Responsabilidades:
- Persistir usuários.
- Consultar usuários.
- Atualizar usuários.
- Remover usuários.
- Criar usuários com perfil definido pelo ADMIN.
"""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import TipoUsuario, User
from app.schemas.user import AdminUserCreate, UserCreate


def get_user_by_id(
    db: Session,
    user_id: int,
) -> User | None:
    """
    Busca um usuário pelo identificador.
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


def get_user_by_matricula(
    db: Session,
    matricula: str,
) -> User | None:
    """
    Busca um usuário pela matrícula.
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
    Retorna todos os usuários ordenados pelo nome.
    """
    return (
        db.query(User)
        .order_by(User.nome.asc())
        .all()
    )


def _persist_user(
    db: Session,
    user: User,
) -> User:
    """
    Persiste um usuário e desfaz a transação em caso de erro.
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


def create_user(
    db: Session,
    user_data: UserCreate,
) -> User:
    """
    Cria um usuário público com o perfil ALUNO.
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

    return _persist_user(db, user)


def create_admin_user(
    db: Session,
    user_data: AdminUserCreate,
) -> User:
    """
    Cria um usuário com o perfil informado no schema administrativo.

    A autorização do solicitante deve ser garantida pela rota
    administrativa antes de esta função ser chamada.
    """
    user = User(
        nome=user_data.nome,
        email=user_data.email,
        senha_hash=hash_password(user_data.senha),
        tipo=user_data.tipo,
        matricula=user_data.matricula,
        telefone=user_data.telefone,
        ativo=True,
    )

    return _persist_user(db, user)


def update_user(
    db: Session,
    user: User,
) -> User:
    """
    Persiste as alterações de um usuário existente.
    """
    return _persist_user(db, user)


def delete_user(
    db: Session,
    user: User,
) -> None:
    """
    Remove um usuário do banco de dados.
    """
    try:
        db.delete(user)
        db.commit()

    except IntegrityError:
        db.rollback()
        raise
