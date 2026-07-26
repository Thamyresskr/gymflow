"""
Operações de acesso a dados relacionadas à autenticação.
"""

from sqlalchemy.orm import Session

from app.core.logger import logger
from app.core.security import verify_password
from app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    senha: str,
) -> User | None:
    """
    Autentica um usuário utilizando e-mail e senha.

    Localiza o usuário pelo e-mail informado e valida a senha
    utilizando o mecanismo de verificação configurado na aplicação.

    Args:
        db: Sessão ativa do banco de dados.
        email: E-mail informado pelo usuário.
        senha: Senha em texto puro.

    Returns:
        User | None: Usuário autenticado quando as credenciais são
        válidas; caso contrário, retorna ``None``.
    """

    logger.info("Tentativa de login | email=%s", email)

    usuario = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if usuario is None:
        logger.warning(
            "Usuario nao encontrado | email=%s",
            email,
        )
        return None

    logger.info(
        "Usuario encontrado | id=%s | email=%s",
        usuario.id,
        usuario.email,
    )

    senha_valida = verify_password(
        senha,
        usuario.senha_hash,
    )

    if not senha_valida:
        logger.warning(
            "Senha invalida | email=%s",
            email,
        )
        return None

    logger.info(
        "Autenticacao realizada com sucesso | usuario=%s | id=%s",
        usuario.email,
        usuario.id,
    )

    return usuario