
"""
Camada de acesso a dados (CRUD) para os indicadores do Dashboard.

Responsabilidades:
- Consultar indicadores de ocupação.
- Consultar estatísticas de check-ins.
- Consolidar informações utilizadas pelo Dashboard.
"""

from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.checkin import Checkin
from app.models.user import User


# Horário de Brasília: UTC-3.
# O Brasil não utiliza horário de verão atualmente.
FUSO_BRASIL = timezone(timedelta(hours=-3))


def _intervalo_hoje_utc() -> tuple[datetime, datetime]:
    """
    Retorna o intervalo do dia atual de Brasília convertido para UTC.

    Os limites são retornados sem tzinfo para compatibilidade com
    os valores DateTime armazenados pelo SQLite.
    """

    hoje = datetime.now(FUSO_BRASIL).date()

    inicio_local = datetime.combine(
        hoje,
        time.min,
        tzinfo=FUSO_BRASIL,
    )

    amanha_local = datetime.combine(
        hoje + timedelta(days=1),
        time.min,
        tzinfo=FUSO_BRASIL,
    )

    inicio_utc = (
        inicio_local
        .astimezone(timezone.utc)
        .replace(tzinfo=None)
    )

    fim_utc = (
        amanha_local
        .astimezone(timezone.utc)
        .replace(tzinfo=None)
    )

    return inicio_utc, fim_utc


def get_ocupacao_atual(db: Session) -> int:
    """Retorna a quantidade de check-ins que continuam abertos."""

    return (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_(None))
        .count()
    )


def get_checkins_hoje(db: Session) -> int:
    """Retorna a quantidade de entradas ocorridas hoje em Brasília."""

    inicio, fim = _intervalo_hoje_utc()

    return (
        db.query(Checkin)
        .filter(
            Checkin.checkin_time >= inicio,
            Checkin.checkin_time < fim,
        )
        .count()
    )


def get_checkouts_hoje(db: Session) -> int:
    """Retorna a quantidade de saídas ocorridas hoje em Brasília."""

    inicio, fim = _intervalo_hoje_utc()

    return (
        db.query(Checkin)
        .filter(
            Checkin.checkout_time.is_not(None),
            Checkin.checkout_time >= inicio,
            Checkin.checkout_time < fim,
        )
        .count()
    )


def get_tempo_medio_permanencia(db: Session) -> float:
    """Calcula a permanência média em minutos dos check-ins finalizados."""

    checkins = (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_not(None))
        .all()
    )

    if not checkins:
        return 0.0

    total_segundos = 0.0

    for checkin in checkins:
        entrada = checkin.checkin_time
        saida = checkin.checkout_time

        # O SQLite pode devolver datetimes sem informação de fuso.
        if entrada.tzinfo is None:
            entrada = entrada.replace(tzinfo=timezone.utc)

        if saida.tzinfo is None:
            saida = saida.replace(tzinfo=timezone.utc)

        total_segundos += (saida - entrada).total_seconds()

    return round(
        total_segundos / len(checkins) / 60,
        2,
    )


def get_ultimos_checkins(
    db: Session,
    limite: int = 10,
) -> list[tuple[Checkin, User]]:
    """Retorna os últimos check-ins com seus respectivos usuários."""

    return (
        db.query(Checkin, User)
        .join(User, Checkin.user_id == User.id)
        .order_by(Checkin.checkin_time.desc())
        .limit(limite)
        .all()
    )
