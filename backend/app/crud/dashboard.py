"""
CRUD responsável pelos indicadores do Dashboard.
"""

from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.checkin import Checkin
from app.models.user import User


def get_ocupacao_atual(db: Session) -> int:
    """
    Retorna a quantidade de usuários presentes.
    """

    return (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_(None))
        .count()
    )


def get_checkins_hoje(db: Session) -> int:
    """
    Retorna a quantidade de check-ins realizados hoje.
    """

    return (
        db.query(Checkin)
        .filter(func.date(Checkin.checkin_time) == date.today())
        .count()
    )


def get_checkouts_hoje(db: Session) -> int:
    """
    Retorna a quantidade de checkouts realizados hoje.
    """

    return (
        db.query(Checkin)
        .filter(
            Checkin.checkout_time.is_not(None),
            func.date(Checkin.checkout_time) == date.today(),
        )
        .count()
    )


def get_tempo_medio_permanencia(db: Session) -> float:
    """
    Calcula o tempo médio de permanência em minutos.
    """

    checkins = (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_not(None))
        .all()
    )

    if not checkins:
        return 0.0

    total = 0

    for checkin in checkins:
        total += (
            checkin.checkout_time - checkin.checkin_time
        ).total_seconds()

    return round((total / len(checkins)) / 60, 2)


def get_ultimos_checkins(
    db: Session,
    limite: int = 10,
):
    """
    Retorna os últimos check-ins.
    """

    return (
        db.query(Checkin, User)
        .join(User)
        .order_by(Checkin.checkin_time.desc())
        .limit(limite)
        .all()
    )