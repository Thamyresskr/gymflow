"""
CRUD de autenticação.
"""

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import verify_password
from app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    senha: str,
):
    """
    Valida usuário e senha.
    """

    logger.info("=" * 60)
    logger.info("Tentativa de login | email=%s", email)

    usuario = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if usuario is None:
        logger.warning("Usuário não encontrado.")
        logger.info("=" * 60)
        return None

    logger.info(
        "Usuário encontrado | id=%s | email=%s",
        usuario.id,
        usuario.email,
    )

    logger.info(
        "Hash armazenado: %s",
        usuario.senha_hash,
    )

    senha_valida = verify_password(
        senha,
        usuario.senha_hash,
    )

    logger.info(
        "Resultado verify_password(): %s",
        senha_valida,
    )

    logger.info("=" * 60)

    if not senha_valida:
        return None

    return usuario