from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import verify_password


def authenticate_user(
    db: Session,
    email: str,
    senha: str,
):
    """
    Valida usuário e senha.
    """
    usuario = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not usuario:
        return None

    if not verify_password(
        senha,
        usuario.senha_hash,
    ):
        return None

    return usuario