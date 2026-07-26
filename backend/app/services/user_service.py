"""
Serviços relacionados ao gerenciamento de usuários.

Responsabilidades:
- Validar regras de negócio relacionadas aos usuários.
- Garantir integridade dos dados.
- Delegar a persistência para a camada CRUD.
- Registrar eventos relevantes da aplicação.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.crud.user import (
    create_user,
    delete_user,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    update_user,
)
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)


def _get_existing_user(
    db: Session,
    user_id: int,
) -> User:
    """
    Recupera um usuário existente.

    Args:
        db: Sessão ativa do banco.
        user_id: Identificador do usuário.

    Returns:
        User: Usuário encontrado.

    Raises:
        HTTPException: Caso o usuário não exista.
    """

    usuario = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if usuario is None:
        logger.warning(
            "Usuario nao encontrado | id=%s",
            user_id,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )

    return usuario


def register_user(
    db: Session,
    user_data: UserCreate,
) -> UserResponse:
    """
    Realiza o cadastro de um novo usuário.

    Args:
        db: Sessão ativa do banco.
        user_data: Dados do usuário.

    Returns:
        UserResponse: Usuário cadastrado.

    Raises:
        HTTPException: Caso o e-mail já esteja cadastrado.
    """

    usuario_existente = get_user_by_email(
        db=db,
        email=user_data.email,
    )

    if usuario_existente is not None:
        logger.warning(
            "Tentativa de cadastro com email ja existente | email=%s",
            user_data.email,
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="E-mail já cadastrado.",
        )

    usuario = create_user(
        db=db,
        user_data=user_data,
    )

    logger.info(
        "Usuario cadastrado | id=%s | email=%s",
        usuario.id,
        usuario.email,
    )

    return usuario


def list_users(
    db: Session,
) -> list[User]:
    """
    Retorna todos os usuários cadastrados.
    """

    return get_all_users(db=db)


def get_user(
    db: Session,
    user_id: int,
) -> User:
    """
    Retorna um usuário pelo identificador.
    """

    return _get_existing_user(
        db=db,
        user_id=user_id,
    )


def update_user_data(
    db: Session,
    user_id: int,
    user_data: UserUpdate,
) -> User:
    """
    Atualiza parcialmente os dados de um usuário.

    Apenas os campos enviados serão alterados.
    """

    usuario = _get_existing_user(
        db=db,
        user_id=user_id,
    )

    dados = user_data.model_dump(exclude_unset=True)

    if "email" in dados:
        usuario_existente = get_user_by_email(
            db=db,
            email=dados["email"],
        )

        if (
            usuario_existente is not None
            and usuario_existente.id != usuario.id
        ):
            logger.warning(
                "Tentativa de atualizar para email ja existente | email=%s",
                dados["email"],
            )

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado.",
            )

    for campo, valor in dados.items():
        setattr(
            usuario,
            campo,
            valor,
        )

    usuario = update_user(
        db=db,
        user=usuario,
    )

    logger.info(
        "Usuario atualizado | id=%s",
        usuario.id,
    )

    return usuario


def remove_user(
    db: Session,
    user_id: int,
) -> None:
    """
    Remove um usuário.

    Args:
        db: Sessão ativa do banco.
        user_id: Identificador do usuário.

    Raises:
        HTTPException: Caso o usuário não exista.
    """

    usuario = _get_existing_user(
        db=db,
        user_id=user_id,
    )

    delete_user(
        db=db,
        user=usuario,
    )

    logger.info(
        "Usuario removido | id=%s",
        user_id,
    )