"""
Dependências compartilhadas da aplicação.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Fornece uma sessão do banco de dados para cada requisição.

    A sessão é encerrada automaticamente ao final da execução,
    mesmo em caso de exceção.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()