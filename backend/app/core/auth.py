
"""
Módulo responsável pela autenticação e autorização da API.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_db
from app.crud.user import get_user_by_id
from app.models.user import TipoUsuario, User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    scheme_name="JWT",
    description="Informe suas credenciais para obter um token JWT.",
)


def unauthorized(detail: str) -> HTTPException:
    """
    Cria uma exceção HTTP 401 para falhas de autenticação.
    """

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Cria um token JWT com prazo de validade.
    """

    payload = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta is not None
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
    Decodifica e valida um token JWT.

    Retorna o conteúdo do token quando válido ou None
    quando o token é inválido ou expirado.
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
) -> User:
    """
    Recupera o usuário autenticado a partir do token JWT.

    Rejeita tokens inválidos, expirados, sem identificador
    de usuário, associados a usuários inexistentes ou a
    contas desativadas.
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

    if not user.ativo:
        raise unauthorized("Usuário inativo.")

    return user


def require_roles(
    *allowed_roles: str,
) -> Callable[..., User]:
    """
    Cria uma dependência que restringe o acesso por perfil.

    Exemplos:
        Depends(require_roles("ADMIN"))
        Depends(require_roles("ADMIN", "RECEPCAO"))

    A verificação do perfil é feita após a autenticação.
    """

    valid_roles = {
        role.value.upper()
        for role in TipoUsuario
    }

    normalized_roles = {
        role.strip().upper()
        for role in allowed_roles
    }

    if (
        not normalized_roles
        or not normalized_roles.issubset(valid_roles)
    ):
        raise ValueError(
            "Um ou mais perfis informados são inválidos."
        )

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        user_role = getattr(
            current_user.tipo,
            "value",
            current_user.tipo,
        )

        if str(user_role).upper() not in normalized_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    "Você não tem permissão para "
                    "realizar esta operação."
                ),
            )

        return current_user

    return role_checker
