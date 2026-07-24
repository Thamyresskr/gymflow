"""
Camada de acesso a dados (CRUD) para check-ins.

Responsabilidades:
- Persistir check-ins;
- Buscar check-ins;
- Atualizar check-ins.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.checkin import Checkin


def create_checkin(
    db: Session,
    checkin: Checkin,
) -> Checkin:
    """
    Salva um novo check-in no banco de dados.

    Args:
        db: Sessão do banco de dados.
        checkin: Check-in a ser persistido.

    Returns:
        Check-in salvo.
    """

    db.add(checkin)
    db.commit()
    db.refresh(checkin)

    return checkin


def get_open_checkin(
    db: Session,
    user_id: int,
) -> Checkin | None:
    """
    Retorna o check-in em aberto de um usuário.

    Args:
        db: Sessão do banco de dados.
        user_id: Identificador do usuário.

    Returns:
        Check-in em aberto ou None.
    """

    return (
        db.query(Checkin)
        .filter(
            Checkin.user_id == user_id,
            Checkin.checkout_time.is_(None),
        )
        .first()
    )


def get_checkin_by_id(
    db: Session,
    checkin_id: int,
) -> Checkin | None:
    """
    Busca um check-in pelo identificador.

    Args:
        db: Sessão do banco de dados.
        checkin_id: Identificador do check-in.

    Returns:
        Check-in encontrado ou None.
    """

    return (
        db.query(Checkin)
        .filter(Checkin.id == checkin_id)
        .first()
    )


def get_all_checkins(
    db: Session,
) -> list[Checkin]:
    """
    Retorna o histórico completo de check-ins.

    Args:
        db: Sessão do banco de dados.

    Returns:
        Lista de check-ins ordenada do mais recente para o mais antigo.
    """

    return (
        db.query(Checkin)
        .order_by(Checkin.checkin_time.desc())
        .all()
    )


def get_active_checkins(
    db: Session,
) -> list[Checkin]:
    """
    Retorna todos os check-ins ativos.

    Args:
        db: Sessão do banco de dados.

    Returns:
        Lista de check-ins sem horário de checkout.
    """

    return (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_(None))
        .order_by(Checkin.checkin_time.desc())
        .all()
    )


def update_checkin(
    db: Session,
    checkin: Checkin,
) -> Checkin:
    """
    Atualiza um check-in existente.

    Args:
        db: Sessão do banco de dados.
        checkin: Check-in atualizado.

    Returns:
        Check-in persistido.
    """

    db.commit()
    db.refresh(checkin)

    return checkin


def checkout(
    db: Session,
    checkin: Checkin,
) -> Checkin:
    """
    Finaliza um check-in registrando a data e hora do checkout.

    Args:
        db: Sessão do banco de dados.
        checkin: Check-in a ser finalizado.

    Returns:
        Check-in atualizado.
    """

    checkin.checkout_time = datetime.now(timezone.utc)

    return update_checkin(
        db=db,
        checkin=checkin,
    )