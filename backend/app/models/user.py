from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.checkin import Checkin


class TipoUsuario(str, Enum):
    """
    Perfis permitidos dentro da aplicação.

    O uso de Enum garante que apenas valores válidos
    possam ser atribuídos ao perfil do usuário.
    """

    ADMIN = "admin"
    PROFESSOR = "professor"
    ALUNO = "aluno"


class User(Base):
    """
    Modelo responsável por representar os usuários da aplicação.

    Cada objeto desta classe corresponde a um registro da tabela
    'users' no banco de dados.
    """

    __tablename__ = "users"

    # ==========================
    # Identificação
    # ==========================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    senha_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ==========================
    # Perfil
    # ==========================

    tipo: Mapped[TipoUsuario] = mapped_column(
        SQLEnum(TipoUsuario, name="tipo_usuario"),
        default=TipoUsuario.ALUNO,
        nullable=False,
    )

    # ==========================
    # Dados complementares
    # ==========================

    matricula: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    telefone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================
    # Auditoria
    # ==========================

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    # ==========================
    # Relacionamentos
    # ==========================

    checkins: Mapped[list["Checkin"]] = relationship(
        "Checkin",
        back_populates="usuario",
        cascade="all, delete-orphan",
    )

    # ==========================
    # Representação
    # ==========================

    def __repr__(self) -> str:
        return (
            f"User("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"email='{self.email}', "
            f"tipo='{self.tipo.value}', "
            f"ativo={self.ativo})"
        )