"""
Configuração do banco de dados da aplicação.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings
from app.core.logger import logger

# ============================================================================
# Caminho absoluto do banco SQLite
# ============================================================================

if settings.DATABASE_URL.startswith("sqlite:///./"):
    database_file = (
        Path(__file__).resolve().parents[2] / "gymflow.db"
    )

    database_url = f"sqlite:///{database_file.as_posix()}"
else:
    database_url = settings.DATABASE_URL

logger.info("Banco de dados: %s", database_url)

# ============================================================================
# Engine
# ============================================================================

engine = create_engine(
    database_url,
    connect_args=(
        {"check_same_thread": False}
        if database_url.startswith("sqlite")
        else {}
    ),
)

# ============================================================================
# Sessão
# ============================================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ============================================================================
# Base dos modelos
# ============================================================================

Base = declarative_base()

# ============================================================================
# Dependência do FastAPI
# ============================================================================


def get_db():
    """
    Fornece uma sessão do banco de dados.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()