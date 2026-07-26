from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Checkin(Base):
    """
    Representa um registro de entrada e saída de um usuário na academia.

    Cada registro corresponde a uma permanência do usuário dentro da academia.
    """

    __tablename__ = "checkins"

    # ==========================
    # Identificação
    # ==========================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ==========================
    # Relacionamento
    # ==========================

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    usuario: Mapped["User"] = relationship(
        "User",
        back_populates="checkins",
    )

    # ==========================
    # Controle de acesso
    # ==========================

    checkin_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )

    checkout_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    # ==========================
    # Representação
    # ==========================

    def __repr__(self) -> str:
        return (
            f"Checkin("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"checkin={self.checkin_time}, "
            f"checkout={self.checkout_time})"
        )