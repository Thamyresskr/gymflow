"""
Serviços relacionados à autenticação.

Responsabilidades:
- Validar as credenciais do usuário.
- Gerar o token JWT de autenticação.
- Registrar eventos de autenticação.
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

    Valida as credenciais informadas, registra o evento de login
    e retorna um token JWT que deverá ser utilizado para autenticar
    as próximas requisições à API.

    Args:
        db: Sessão ativa do banco de dados.
        email: E-mail informado pelo usuário.
        senha: Senha informada pelo usuário.

    Returns:
        Token: Token JWT utilizado para autenticação.

    Raises:
        HTTPException: Caso as credenciais informadas sejam inválidas.
    """

    usuario = authenticate_user(
        db=db,
        email=email,
        senha=senha,
    )

    if usuario is None:
        logger.warning(
            "Tentativa de login invalida | email=%s",
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
        "Login realizado | usuario=%s | id=%s",
        usuario.email,
        usuario.id,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )