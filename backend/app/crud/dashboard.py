"""
Camada de acesso a dados (CRUD) para os indicadores do Dashboard.

Responsabilidades:
- Consultar indicadores de ocupação.
- Consultar estatísticas de check-ins.
- Consolidar informações utilizadas pelo Dashboard.
"""

from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.checkin import Checkin
from app.models.user import User


def get_ocupacao_atual(
    db: Session,
) -> int:
    """
    Retorna a quantidade de usuários atualmente presentes.

    Considera como presentes todos os check-ins que ainda não
    possuem horário de check-out registrado.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        int: Quantidade de usuários presentes.
    """

    return (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_(None))
        .count()
    )


def get_checkins_hoje(
    db: Session,
) -> int:
    """
    Retorna a quantidade de check-ins realizados na data atual.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        int: Quantidade de check-ins realizados hoje.
    """

    return (
        db.query(Checkin)
        .filter(
            func.date(Checkin.checkin_time) == date.today(),
        )
        .count()
    )


def get_checkouts_hoje(
    db: Session,
) -> int:
    """
    Retorna a quantidade de check-outs realizados na data atual.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        int: Quantidade de check-outs realizados hoje.
    """

    return (
        db.query(Checkin)
        .filter(
            Checkin.checkout_time.is_not(None),
            func.date(Checkin.checkout_time) == date.today(),
        )
        .count()
    )


def get_tempo_medio_permanencia(
    db: Session,
) -> float:
    """
    Calcula o tempo médio de permanência em minutos.

    Apenas check-ins finalizados são considerados no cálculo.

    Args:
        db: Sessão ativa do banco de dados.

    Returns:
        float: Tempo médio de permanência em minutos.
    """

    checkins = (
        db.query(Checkin)
        .filter(Checkin.checkout_time.is_not(None))
        .all()
    )

    if not checkins:
        return 0.0

    total = 0.0

    for checkin in checkins:
        total += (
            checkin.checkout_time
            - checkin.checkin_time
        ).total_seconds()

    return round(
        (total / len(checkins)) / 60,
        2,
    )


def get_ultimos_checkins(
    db: Session,
    limite: int = 10,
) -> list[tuple[Checkin, User]]:
    """
    Retorna os últimos check-ins registrados.

    Os resultados são ordenados do mais recente para o mais antigo.

    Args:
        db: Sessão ativa do banco de dados.
        limite: Quantidade máxima de registros retornados.

    Returns:
        list[tuple[Checkin, User]]: Lista contendo o check-in e
        seu respectivo usuário.
    """

    return (
        db.query(Checkin, User)
        .join(User)
        .order_by(Checkin.checkin_time.desc())
        .limit(limite)
        .all()
    )