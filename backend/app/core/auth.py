"""
Módulo responsável pela autenticação da API.

Responsabilidades:
- Gerar tokens JWT
- Validar tokens JWT
- Recuperar o usuário autenticado
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.crud.user import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT",
    description="Informe suas credenciais para obter um token JWT.",
)


def unauthorized(detail: str) -> HTTPException:
    """
    Retorna uma exceção HTTP 401 padronizada.
    """

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Gera um token JWT.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict[str, Any] | None:
    """
    Decodifica um JWT.
    """

    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

    except JWTError:
        return None


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Recupera o usuário autenticado.
    """

    payload = decode_access_token(token)

    if payload is None:
        raise unauthorized("Token inválido ou expirado.")

    user_id = payload.get("id")

    if user_id is None:
        raise unauthorized("Token inválido.")

    user = get_user_by_id(
        db=db,
        user_id=user_id,
    )

    if user is None:
        raise unauthorized("Usuário não encontrado.")

    return user