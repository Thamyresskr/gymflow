"""
Regras de negócio relacionadas à autenticação.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import create_access_token
from app.core.logger import logger
from app.crud.auth import authenticate_user
from app.schemas.auth import Token


def login_user(
    db: Session,
    email: str,
    senha: str,
) -> Token:
    """
    Autentica um usuário e gera um token JWT.

    Args:
        db: Sessão do banco de dados.
        email: E-mail informado pelo usuário.
        senha: Senha informada pelo usuário.

    Returns:
        Token JWT de autenticação.

    Raises:
        HTTPException: Caso as credenciais sejam inválidas.
    """

    usuario = authenticate_user(
        db=db,
        email=email,
        senha=senha,
    )

    if usuario is None:
        logger.warning(
            "Tentativa de login inválida | email=%s",
            email,
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    access_token = create_access_token(
        data={
            "sub": usuario.email,
            "id": usuario.id,
        }
    )

    logger.info(
        "Login realizado | usuário=%s | id=%s",
        usuario.email,
        usuario.id,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )