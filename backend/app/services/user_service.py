"""
Regras de negócio relacionadas aos usuários.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.logger import logger
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate


def register_user(
    db: Session,
    user_data: UserCreate,
):
    """
    Realiza o cadastro de um novo usuário.

    Args:
        db: Sessão do banco de dados.
        user_data: Dados do usuário.

    Returns:
        Usuário criado.

    Raises:
        HTTPException: Caso o e-mail já esteja cadastrado.
    """

    usuario_existente = get_user_by_email(
        db=db,
        email=user_data.email,
    )

    if usuario_existente:

        logger.warning(
            "Tentativa de cadastro com e-mail já existente | email=%s",
            user_data.email,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="E-mail já cadastrado.",
        )

    usuario = create_user(
        db=db,
        user_data=user_data,
    )

    logger.info(
        "Usuário cadastrado | id=%s | email=%s",
        usuario.id,
        usuario.email,
    )

    return usuario